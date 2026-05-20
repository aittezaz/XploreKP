import json
from pathlib import Path

from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
DATA_DIR = Path(__file__).parent / "data"

CATEGORIES = [
    {"name": "Restaurants", "slug": "restaurants"},
    {"name": "Hospitals", "slug": "hospitals"},
    {"name": "Petrol Pumps", "slug": "petrol-pumps"},
    {"name": "Shopping Malls", "slug": "shopping-malls"},
    {"name": "Pharmacies", "slug": "pharmacies"},
    {"name": "Wedding Halls", "slug": "wedding-halls"},
    {"name": "Hotels", "slug": "hotels"},
    {"name": "Tourist Spots", "slug": "tourist-spots"},
    {"name": "Workshops", "slug": "workshops"},
    {"name": "Banks and ATMs", "slug": "banks-and-atms"},
]

CITY_ALIASES = {
    "mardan": "mardan",
    "peshawar": "peshawar",
    "swabi": "swabi",
    "sawabi": "swabi",
}

CITIES = {
    "mardan": {
        "name": "Mardan",
        "file": "mardan_places.json",
        "center": [34.1986, 72.0404],
        "tagline": "Explore food, health, travel, shopping, and daily services across Mardan.",
    },
    "peshawar": {
        "name": "Peshawar",
        "file": "peshawar_places.json",
        "center": [34.0151, 71.5249],
        "tagline": "Explore useful places across Peshawar, from Saddar and University Road to Hayatabad.",
    },
    "swabi": {
        "name": "Swabi",
        "file": "swabi_places.json",
        "center": [34.1241, 72.4698],
        "tagline": "Find useful places around Swabi, Topi, and nearby busy areas.",
    },
}

STARTER_PLACES = {
    "swabi": {
        "restaurants": [
            {"name": "Swabi Food Point", "address": "Main Bazaar, Swabi", "lat": 34.1219, "lng": 72.4709, "source": "Starter data"},
            {"name": "Topi Taste House", "address": "Topi Road, Swabi", "lat": 34.0706, "lng": 72.6218, "source": "Starter data"},
            {"name": "City Grill Swabi", "address": "Jehangira Road, Swabi", "lat": 34.1278, "lng": 72.4635, "source": "Starter data"},
        ],
        "hospitals": [
            {"name": "Swabi Medical Center", "address": "Mardan Road, Swabi", "lat": 34.1234, "lng": 72.4736, "source": "Starter data"},
            {"name": "City Care Clinic", "address": "Main Bazaar, Swabi", "lat": 34.1198, "lng": 72.4681, "source": "Starter data"},
            {"name": "Topi Health Clinic", "address": "Topi, Swabi", "lat": 34.0716, "lng": 72.6228, "source": "Starter data"},
        ],
        "petrol-pumps": [
            {"name": "Swabi Fuel Station", "address": "Mardan Road, Swabi", "lat": 34.1301, "lng": 72.4592, "source": "Starter data"},
            {"name": "City Petrol Pump", "address": "Jehangira Road, Swabi", "lat": 34.1172, "lng": 72.4766, "source": "Starter data"},
            {"name": "Green Fuel Swabi", "address": "Topi Road, Swabi", "lat": 34.1055, "lng": 72.5124, "source": "Starter data"},
        ],
        "shopping-malls": [
            {"name": "Swabi Shopping Plaza", "address": "Main Bazaar, Swabi", "lat": 34.1211, "lng": 72.4701, "source": "Starter data"},
            {"name": "Family Shopping Center", "address": "Mardan Road, Swabi", "lat": 34.1263, "lng": 72.4664, "source": "Starter data"},
            {"name": "Topi Market Center", "address": "Topi, Swabi", "lat": 34.0699, "lng": 72.6234, "source": "Starter data"},
        ],
        "pharmacies": [
            {"name": "Care Pharmacy", "address": "Main Bazaar, Swabi", "lat": 34.1214, "lng": 72.4714, "source": "Starter data"},
            {"name": "Shaheen Medical Store", "address": "Mardan Road, Swabi", "lat": 34.1252, "lng": 72.4677, "source": "Starter data"},
            {"name": "Health Plus Pharmacy", "address": "Topi Road, Swabi", "lat": 34.1089, "lng": 72.5056, "source": "Starter data"},
        ],
        "wedding-halls": [
            {"name": "Royal Wedding Hall", "address": "Jehangira Road, Swabi", "lat": 34.1168, "lng": 72.4781, "source": "Starter data"},
            {"name": "Pearl Marquee", "address": "Mardan Road, Swabi", "lat": 34.1321, "lng": 72.4551, "source": "Starter data"},
            {"name": "Swabi Event Complex", "address": "Topi Road, Swabi", "lat": 34.1016, "lng": 72.5208, "source": "Starter data"},
        ],
        "hotels": [
            {"name": "Swabi City Hotel", "address": "Main Bazaar, Swabi", "lat": 34.1205, "lng": 72.4696, "source": "Starter data"},
            {"name": "Green Palace Hotel", "address": "Mardan Road, Swabi", "lat": 34.1281, "lng": 72.4623, "source": "Starter data"},
            {"name": "Comfort Inn Swabi", "address": "Jehangira Road, Swabi", "lat": 34.1149, "lng": 72.4804, "source": "Starter data"},
        ],
        "tourist-spots": [
            {"name": "Swabi View Point", "address": "Swabi", "lat": 34.1328, "lng": 72.4851, "source": "Starter data"},
            {"name": "Topi Riverside Area", "address": "Topi, Swabi", "lat": 34.0692, "lng": 72.6298, "source": "Starter data"},
            {"name": "Gadoon Route View", "address": "Gadoon Road, Swabi", "lat": 34.2039, "lng": 72.6402, "source": "Starter data"},
        ],
        "workshops": [
            {"name": "Auto Care Workshop", "address": "Mardan Road, Swabi", "lat": 34.1273, "lng": 72.4648, "source": "Starter data"},
            {"name": "Swabi Motors Workshop", "address": "Jehangira Road, Swabi", "lat": 34.1162, "lng": 72.4772, "source": "Starter data"},
            {"name": "Quick Fix Garage", "address": "Topi Road, Swabi", "lat": 34.1104, "lng": 72.5015, "source": "Starter data"},
        ],
        "banks-and-atms": [
            {"name": "City Bank ATM", "address": "Main Bazaar, Swabi", "lat": 34.1218, "lng": 72.4703, "source": "Starter data"},
            {"name": "Swabi Cash Point", "address": "Mardan Road, Swabi", "lat": 34.1266, "lng": 72.4661, "source": "Starter data"},
            {"name": "Family ATM Center", "address": "Topi Road, Swabi", "lat": 34.1094, "lng": 72.5082, "source": "Starter data"},
        ],
    }
}


def normalize_city(city_value):
    city_slug = city_value.strip().lower().replace(" ", "-")
    return CITY_ALIASES.get(city_slug)


def city_file(city_slug):
    return DATA_DIR / CITIES[city_slug]["file"]


def load_places(city_slug):
    places_file = city_file(city_slug)

    if not places_file.exists():
        starter_places = STARTER_PLACES.get(city_slug, {})
        try:
            save_places(city_slug, starter_places)
        except OSError:
            pass
        return starter_places

    with places_file.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_places(city_slug, places):
    DATA_DIR.mkdir(exist_ok=True)

    with city_file(city_slug).open("w", encoding="utf-8") as file:
        json.dump(places, file, indent=4, ensure_ascii=False)


def find_category(category_slug):
    return next(
        (item for item in CATEGORIES if item["slug"] == category_slug),
        None
    )


@app.route("/")
def home():
    return render_template("index.html", cities=CITIES)


@app.route("/search")
def search():
    city_slug = normalize_city(request.args.get("city", ""))

    if city_slug:
        return redirect(url_for("city_home", city_slug=city_slug))

    return render_template("coming.html", city=request.args.get("city", "").strip())


@app.route("/<city_slug>")
def city_home(city_slug):
    city_slug = normalize_city(city_slug) or city_slug

    if city_slug not in CITIES:
        return render_template("coming.html", city=city_slug), 404

    places = load_places(city_slug)
    categories = [
        {**category, "count": len(places.get(category["slug"], []))}
        for category in CATEGORIES
    ]
    return render_template(
        "mardan.html",
        city=CITIES[city_slug],
        city_slug=city_slug,
        categories=categories
    )


@app.route("/<city_slug>/add", methods=["GET", "POST"])
def add_place(city_slug):
    city_slug = normalize_city(city_slug) or city_slug

    if city_slug not in CITIES:
        return render_template("coming.html", city=city_slug), 404

    selected_category = request.args.get("category", "pharmacies")
    error = ""

    if request.method == "POST":
        category_slug = request.form.get("category", "").strip()
        name = request.form.get("name", "").strip()
        address = request.form.get("address", "").strip()
        lat = request.form.get("lat", "").strip()
        lng = request.form.get("lng", "").strip()

        if category_slug and name and address and lat and lng:
            places = load_places(city_slug)
            places.setdefault(category_slug, []).append({
                "name": name,
                "address": address,
                "lat": float(lat),
                "lng": float(lng),
                "source": "Added manually",
            })
            try:
                save_places(city_slug, places)
            except OSError:
                error = (
                    "This live server cannot save files permanently. "
                    "For permanent online additions, connect a database later."
                )
            else:
                return redirect(url_for(
                    "city_category",
                    city_slug=city_slug,
                    category_slug=category_slug
                ))

        elif not error:
            error = "Please fill all fields and select a map location."

        selected_category = category_slug or selected_category

    return render_template(
        "add_place.html",
        city=CITIES[city_slug],
        city_slug=city_slug,
        categories=CATEGORIES,
        selected_category=selected_category,
        error=error
    )


@app.route("/<city_slug>/<category_slug>")
def city_category(city_slug, category_slug):
    city_slug = normalize_city(city_slug) or city_slug

    if city_slug not in CITIES:
        return render_template("coming.html", city=city_slug), 404

    category = find_category(category_slug)

    if category is None:
        category = {"name": category_slug.replace("-", " ").title()}

    places = load_places(city_slug).get(category_slug, [])

    return render_template(
        "category_coming.html",
        city=CITIES[city_slug],
        city_slug=city_slug,
        category=category["name"],
        category_slug=category_slug,
        places=places,
        place_count=len(places)
    )


if __name__ == "__main__":
    app.run(debug=True)
