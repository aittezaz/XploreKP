import json
import re
import urllib.parse
import urllib.request
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PLACES_FILE = PROJECT_ROOT / "data" / "mardan_places.json"

# Covers Mardan city and nearby useful areas. Widen this if you want more of the district.
BBOX = "34.1500,71.9000,34.3300,72.1600"
OVERPASS_URL = "https://overpass-api.de/api/interpreter"

CATEGORIES = {
    "restaurants": [
        'nwr["amenity"~"^(restaurant|fast_food|cafe)$"]({bbox});',
    ],
    "hospitals": [
        'nwr["amenity"~"^(hospital|clinic|doctors|dentist)$"]({bbox});',
        'nwr["healthcare"]({bbox});',
    ],
    "petrol-pumps": [
        'nwr["amenity"="fuel"]({bbox});',
    ],
    "shopping-malls": [
        'nwr["shop"="mall"]({bbox});',
        'nwr["building"="retail"]({bbox});',
        'nwr["name"~"(Mall|Plaza|Market|Shopping|Center|Centre)", i]({bbox});',
    ],
    "pharmacies": [
        'nwr["amenity"="pharmacy"]({bbox});',
        'nwr["healthcare"="pharmacy"]({bbox});',
        'nwr["name"~"(Pharmacy|Medical|Medicine|Medicos|Chemist)", i]({bbox});',
    ],
    "wedding-halls": [
        'nwr["amenity"="events_venue"]({bbox});',
        'nwr["name"~"(Wedding|Marquee|Banquet|Marriage|Shadi|Shaadi|Hall)", i]({bbox});',
    ],
    "hotels": [
        'nwr["tourism"~"^(hotel|guest_house|motel|hostel)$"]({bbox});',
        'nwr["name"~"(Hotel|Guest House|Inn|Lodge)", i]({bbox});',
    ],
    "tourist-spots": [
        'nwr["tourism"~"^(attraction|museum|viewpoint|picnic_site)$"]({bbox});',
        'nwr["historic"]({bbox});',
        'nwr["leisure"="park"]({bbox});',
    ],
    "workshops": [
        'nwr["shop"~"^(car_repair|tyres|car_parts|motorcycle_repair)$"]({bbox});',
        'nwr["name"~"(Workshop|Garage|Autos|Motors|Mechanic|Tyre|Tire)", i]({bbox});',
    ],
    "banks-and-atms": [
        'nwr["amenity"~"^(bank|atm)$"]({bbox});',
    ],
}

NAME_FILTERS = {
    "shopping-malls": re.compile(r"(mall|plaza|market|shopping|center|centre)", re.I),
    "pharmacies": re.compile(r"(pharmacy|medical|medicine|medicos|chemist)", re.I),
    "wedding-halls": re.compile(r"\b(wedding|marquee|banquet|marriage|shadi|shaadi|hall)\b", re.I),
    "hotels": re.compile(r"(hotel|guest house|inn|lodge)", re.I),
    "workshops": re.compile(r"(workshop|garage|autos|motors|mechanic|tyre|tire)", re.I),
}

def load_existing_places():
    if not PLACES_FILE.exists():
        return {}

    with PLACES_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)

def save_places(places):
    PLACES_FILE.parent.mkdir(exist_ok=True)

    with PLACES_FILE.open("w", encoding="utf-8") as file:
        json.dump(places, file, indent=4, ensure_ascii=False)

def build_query(parts):
    body = "\n".join(part.format(bbox=BBOX) for part in parts)
    return f"""
[out:json][timeout:80];
(
{body}
);
out center tags;
"""

def fetch_elements(parts):
    query = build_query(parts)
    data = urllib.parse.urlencode({"data": query}).encode("utf-8")
    request = urllib.request.Request(
        OVERPASS_URL,
        data=data,
        headers={"User-Agent": "XploreKP student project importer"},
    )

    with urllib.request.urlopen(request, timeout=100) as response:
        payload = json.loads(response.read().decode("utf-8"))

    return payload.get("elements", [])

def compact_address(tags):
    pieces = [
        tags.get("addr:housename"),
        tags.get("addr:street"),
        tags.get("addr:place"),
        tags.get("addr:suburb"),
        tags.get("addr:city"),
    ]
    address = ", ".join(piece for piece in pieces if piece)

    return address or tags.get("description") or "Mardan"

def element_location(element):
    lat = element.get("lat") or element.get("center", {}).get("lat")
    lng = element.get("lon") or element.get("center", {}).get("lon")

    if lat is None or lng is None:
        return None

    return float(lat), float(lng)

def normalize_website(value):
    if not value:
        return ""

    if value.startswith(("http://", "https://")):
        return value

    return f"https://{value}"

def osm_url(element):
    osm_type = element["type"]
    osm_id = element["id"]
    return f"https://www.openstreetmap.org/{osm_type}/{osm_id}"

def place_from_element(element):
    tags = element.get("tags", {})
    name = tags.get("name") or tags.get("operator") or tags.get("brand")
    location = element_location(element)

    if not name or location is None:
        return None

    lat, lng = location

    return {
        "name": name.strip(),
        "address": compact_address(tags),
        "lat": lat,
        "lng": lng,
        "phone": tags.get("phone") or tags.get("contact:phone") or "",
        "website": normalize_website(tags.get("website") or tags.get("contact:website") or ""),
        "opening_hours": tags.get("opening_hours") or "",
        "source": "OpenStreetMap",
        "osm_type": element["type"],
        "osm_id": element["id"],
        "osm_url": osm_url(element),
    }

def category_allows_place(category_slug, place):
    name = place["name"]
    pattern = NAME_FILTERS.get(category_slug)

    if pattern is None:
        return True

    return bool(pattern.search(name))

def place_key(place):
    if place.get("osm_id") and place.get("osm_type"):
        return f"osm:{place['osm_type']}:{place['osm_id']}"

    normalized_name = re.sub(r"[^a-z0-9]+", "", place["name"].lower())
    return f"manual:{normalized_name}:{round(float(place['lat']), 5)}:{round(float(place['lng']), 5)}"

def merge_places(existing, imported):
    merged = list(existing)
    seen = {place_key(place) for place in merged}

    for place in imported:
        key = place_key(place)
        if key in seen:
            continue
        seen.add(key)
        merged.append(place)

    return sorted(merged, key=lambda item: item["name"].lower())

def main():
    places = load_existing_places()
    summary = {}

    for category_slug, query_parts in CATEGORIES.items():
        elements = fetch_elements(query_parts)
        imported = [
            place
            for place in (place_from_element(element) for element in elements)
            if place and category_allows_place(category_slug, place)
        ]
        places[category_slug] = merge_places(places.get(category_slug, []), imported)
        summary[category_slug] = {
            "fetched": len(elements),
            "usable": len(imported),
            "saved_total": len(places[category_slug]),
        }

    save_places(places)

    print(json.dumps(summary, indent=4))
    print(f"Saved {PLACES_FILE}")

if __name__ == "__main__":
    main()
