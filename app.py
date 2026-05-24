import json
from pathlib import Path

from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
DATA_DIR = Path(__file__).parent / "data"
GUIDES_FILE = DATA_DIR / "guides.json"

OWNER_GUIDE = {
    "name": "XploreKP",
    "phone": "+92 300 0000000",
    "area": "Available across KP",
    "note": "Main contact",
    "source": "Owner",
}

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
    "abbottabad": "abbottabad",
    "abottabad": "abbottabad",
    "balakot": "balakot",
    "bannu": "bannu",
    "batagram": "battagram",
    "battagram": "battagram",
    "bunair": "buner",
    "buner": "buner",
    "bunir": "buner",
    "charsadda": "charsadda",
    "chakdara": "chakdara",
    "chitral": "lower-chitral",
    "chitral-lower": "lower-chitral",
    "chitral-upper": "upper-chitral",
    "dera-ismail-khan": "dera-ismail-khan",
    "di-khan": "dera-ismail-khan",
    "dikhan": "dera-ismail-khan",
    "dir": "lower-dir",
    "dir-lower": "lower-dir",
    "dir-upper": "upper-dir",
    "hangu": "hangu",
    "haripur": "haripur",
    "kaghan": "kaghan",
    "kalam": "kalam",
    "karak": "karak",
    "kohat": "kohat",
    "lakki-marwat": "lakki-marwat",
    "lower-chitral": "lower-chitral",
    "lower-dir": "lower-dir",
    "malakand": "malakand",
    "mardan": "mardan",
    "mansehra": "mansehra",
    "mingora": "swat",
    "naran": "naran",
    "nowshera": "nowshera",
    "peshawar": "peshawar",
    "shogran": "shogran",
    "swabi": "swabi",
    "sawabi": "swabi",
    "swat": "swat",
    "tank": "tank",
    "upper-chitral": "upper-chitral",
    "upper-dir": "upper-dir",
}

CITIES = {
    "abbottabad": {
        "name": "Abbottabad",
        "file": "abbottabad_places.json",
        "center": [34.1688, 73.2215],
        "tagline": "Explore Abbottabad, Jinnahabad, Supply, Mandian, and nearby hill routes.",
    },
    "balakot": {
        "name": "Balakot",
        "file": "balakot_places.json",
        "center": [34.5473, 73.3516],
        "tagline": "Find useful stops around Balakot, the Kaghan Valley gateway, and riverside travel routes.",
    },
    "bannu": {
        "name": "Bannu",
        "file": "bannu_places.json",
        "center": [32.9861, 70.6042],
        "tagline": "Explore food, hospitals, markets, hotels, and daily services across Bannu.",
    },
    "battagram": {
        "name": "Battagram",
        "file": "battagram_places.json",
        "center": [34.6772, 73.0233],
        "tagline": "Find places around Battagram city, main bazaars, and Karakoram Highway stops.",
    },
    "buner": {
        "name": "Buner",
        "file": "buner_places.json",
        "center": [34.3943, 72.6151],
        "tagline": "Explore useful places around Buner, Daggar, Pir Baba, and nearby scenic areas.",
    },
    "charsadda": {
        "name": "Charsadda",
        "file": "charsadda_places.json",
        "center": [34.1482, 71.7406],
        "tagline": "Find restaurants, hospitals, markets, and travel stops across Charsadda and Tangi.",
    },
    "chakdara": {
        "name": "Chakdara",
        "file": "chakdara_places.json",
        "center": [34.6507, 72.0318],
        "tagline": "Explore Chakdara, Malakand University, Swat Road stops, and nearby services.",
    },
    "kalam": {
        "name": "Kalam",
        "file": "kalam_places.json",
        "center": [35.4902, 72.5889],
        "tagline": "Explore hotels, food spots, tourist points, and travel services in Kalam Valley.",
    },
    "karak": {
        "name": "Karak",
        "file": "karak_places.json",
        "center": [33.1163, 71.0935],
        "tagline": "Find daily services, food, health, banks, and highway stops around Karak.",
    },
    "kohat": {
        "name": "Kohat",
        "file": "kohat_places.json",
        "center": [33.5869, 71.4429],
        "tagline": "Explore Kohat city, bazaars, hospitals, hotels, and travel services.",
    },
    "lower-chitral": {
        "name": "Lower Chitral",
        "file": "lower_chitral_places.json",
        "center": [35.8518, 71.7864],
        "tagline": "Discover useful places around Chitral city, airports, hotels, and tourist routes.",
    },
    "upper-chitral": {
        "name": "Upper Chitral",
        "file": "upper_chitral_places.json",
        "center": [36.2136, 72.1792],
        "tagline": "Explore Booni, Mastuj, and Upper Chitral travel stops, hotels, and services.",
    },
    "dera-ismail-khan": {
        "name": "Dera Ismail Khan",
        "file": "dera_ismail_khan_places.json",
        "center": [31.8327, 70.9024],
        "tagline": "Find food, hospitals, markets, hotels, banks, and travel services in D.I. Khan.",
    },
    "hangu": {
        "name": "Hangu",
        "file": "hangu_places.json",
        "center": [33.5317, 71.0595],
        "tagline": "Explore useful places around Hangu city, bazaars, and travel routes.",
    },
    "haripur": {
        "name": "Haripur",
        "file": "haripur_places.json",
        "center": [33.9946, 72.9106],
        "tagline": "Find places across Haripur, Hattar, Khanpur, and nearby travel areas.",
    },
    "kaghan": {
        "name": "Kaghan",
        "file": "kaghan_places.json",
        "center": [34.7796, 73.5207],
        "tagline": "Explore hotels, restaurants, tourist stops, and services in Kaghan Valley.",
    },
    "lakki-marwat": {
        "name": "Lakki Marwat",
        "file": "lakki_marwat_places.json",
        "center": [32.6079, 70.9114],
        "tagline": "Find everyday services, food, health, banks, and transport stops around Lakki Marwat.",
    },
    "lower-dir": {
        "name": "Lower Dir",
        "file": "lower_dir_places.json",
        "center": [34.9161, 71.8097],
        "tagline": "Explore Timergara, Chakdara Road, hospitals, markets, and travel services in Lower Dir.",
    },
    "malakand": {
        "name": "Malakand",
        "file": "malakand_places.json",
        "center": [34.5656, 71.9304],
        "tagline": "Find useful places around Batkhela, Dargai, and Malakand travel routes.",
    },
    "mardan": {
        "name": "Mardan",
        "file": "mardan_places.json",
        "center": [34.1986, 72.0404],
        "tagline": "Explore food, health, travel, shopping, and daily services across Mardan.",
    },
    "mansehra": {
        "name": "Mansehra",
        "file": "mansehra_places.json",
        "center": [34.3339, 73.2011],
        "tagline": "Explore Mansehra city, Shinkiari, tourist routes, hotels, and daily services.",
    },
    "naran": {
        "name": "Naran",
        "file": "naran_places.json",
        "center": [34.9093, 73.6507],
        "tagline": "Find popular hotels, restaurants, tourist points, and travel services in Naran.",
    },
    "nowshera": {
        "name": "Nowshera",
        "file": "nowshera_places.json",
        "center": [34.0159, 71.9812],
        "tagline": "Explore Nowshera, Risalpur, Akora Khattak, and busy GT Road service areas.",
    },
    "peshawar": {
        "name": "Peshawar",
        "file": "peshawar_places.json",
        "center": [34.0151, 71.5249],
        "tagline": "Explore useful places across Peshawar, from Saddar and University Road to Hayatabad.",
    },
    "shogran": {
        "name": "Shogran",
        "file": "shogran_places.json",
        "center": [34.6271, 73.4747],
        "tagline": "Explore hotels, food, jeep routes, and tourist spots around Shogran and Siri Paye.",
    },
    "swabi": {
        "name": "Swabi",
        "file": "swabi_places.json",
        "center": [34.1241, 72.4698],
        "tagline": "Find useful places around Swabi, Topi, and nearby busy areas.",
    },
    "swat": {
        "name": "Swat",
        "file": "swat_places.json",
        "center": [34.7717, 72.3602],
        "tagline": "Explore Mingora, Saidu Sharif, Fizagat, Malam Jabba Road, and Swat Valley services.",
    },
    "tank": {
        "name": "Tank",
        "file": "tank_places.json",
        "center": [32.2167, 70.3833],
        "tagline": "Find daily services, food, health, banks, and travel stops around Tank.",
    },
    "upper-dir": {
        "name": "Upper Dir",
        "file": "upper_dir_places.json",
        "center": [35.2074, 71.8756],
        "tagline": "Explore Dir city, Kumrat route services, hotels, food, and travel stops.",
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

POPULAR_PLACE_GROUPS = {
    "abbottabad": ["Ilyasi Mosque", "Shimla Hill", "Lady Garden Public Park", "Thandiani Road"],
    "balakot": ["Kunhar River View", "Balakot Bazaar", "Kaghan Road", "Garhi Habibullah Road"],
    "bannu": ["Bannu Bazaar", "Mandew Park", "Bannu Township", "Kohat Road"],
    "battagram": ["Battagram Bazaar", "Karakoram Highway View", "Allai Road", "District Courts Area"],
    "buner": ["Pir Baba", "Daggar Bazaar", "Elum Mountain View", "Jowar Road"],
    "charsadda": ["Rajjar Bazaar", "Tangi Bazaar", "Khyali River Area", "Charsadda Museum Area"],
    "chakdara": ["Chakdara Fort", "University of Malakand", "Swat River Bridge", "Chakdara Bazaar"],
    "kalam": ["Kalam Bazaar", "Ushu Forest", "Mahodand Lake Road", "Matiltan Waterfall Road"],
    "karak": ["Karak Bazaar", "Karak Fort Area", "Indus Highway", "Sabirabad Road"],
    "kohat": ["Kohat Bazaar", "KDA Kohat", "Tanda Dam", "Kohat Tunnel Road"],
    "lower-chitral": ["Chitral Fort", "Shahi Masjid Chitral", "Chitral Bazaar", "Birmoghlasht Road"],
    "upper-chitral": ["Booni Bazaar", "Qaqlasht Meadows", "Mastuj Road", "Torkhow Road"],
    "dera-ismail-khan": ["D.I. Khan Bazaar", "Indus River View", "Tank Adda", "Circular Road"],
    "hangu": ["Hangu Bazaar", "Doaba Road", "Thall Road", "District Courts Area"],
    "haripur": ["Khanpur Dam", "Haripur Bazaar", "Hattar Road", "Sarai Saleh"],
    "kaghan": ["Kaghan Bazaar", "Kunhar River View", "Shogran Road", "Naran Road"],
    "lakki-marwat": ["Lakki Bazaar", "Gambila River Area", "Bannu Road", "Naurang Road"],
    "lower-dir": ["Timergara Bazaar", "Balambat", "Panjkora River View", "Chakdara Road"],
    "malakand": ["Batkhela Bazaar", "Dargai Bazaar", "Malakand Pass", "Jabban Road"],
    "mansehra": ["Mansehra Bazaar", "Shinkiari", "Karakoram Highway", "Lulusar-Dudipatsar Route Office Area"],
    "naran": ["Naran Bazaar", "Saif-ul-Malook Lake Road", "Kunhar River View", "Babusar Road"],
    "nowshera": ["Nowshera Cantt", "Risalpur", "Akora Khattak", "GT Road"],
    "shogran": ["Shogran Bazaar", "Siri Paye Meadows", "Kiwai Waterfall", "Jeep Track Point"],
    "swat": ["Fizagat Park", "Saidu Sharif", "Mingora Bazaar", "Malam Jabba Road"],
    "tank": ["Tank Bazaar", "D.I. Khan Road", "Waziristan Road", "District Courts Area"],
    "upper-dir": ["Dir Bazaar", "Kumrat Valley Road", "Sheringal", "Lowari Tunnel Road"],
}

STARTER_CATEGORY_TEMPLATES = {
    "restaurants": ("{area} Food Point", "{area}, {city}", 0.0020, 0.0020),
    "hospitals": ("{city} Medical Center", "Main Road, {city}", 0.0030, -0.0015),
    "petrol-pumps": ("{city} Fuel Station", "Main Road, {city}", -0.0020, 0.0030),
    "shopping-malls": ("{area} Market", "{area}, {city}", -0.0010, -0.0020),
    "pharmacies": ("Care Pharmacy {city}", "Main Bazaar, {city}", 0.0015, -0.0025),
    "wedding-halls": ("Royal Marquee {city}", "Main Road, {city}", -0.0030, 0.0015),
    "hotels": ("{city} View Hotel", "Near Main Bazaar, {city}", 0.0028, 0.0007),
    "workshops": ("Auto Care Workshop {city}", "Transport Adda, {city}", -0.0025, -0.0010),
    "banks-and-atms": ("{city} Bank ATM", "Main Bazaar, {city}", 0.0008, 0.0018),
}


def starter_place(name, address, lat, lng):
    return {
        "name": name,
        "address": address,
        "lat": round(lat, 6),
        "lng": round(lng, 6),
        "phone": "",
        "website": "",
        "opening_hours": "",
        "source": "Starter data",
    }


def generated_starter_places(city_slug):
    if city_slug in STARTER_PLACES:
        return STARTER_PLACES[city_slug]

    city = CITIES[city_slug]
    city_name = city["name"]
    center_lat, center_lng = city["center"]
    popular_areas = POPULAR_PLACE_GROUPS.get(city_slug, [city_name])
    places = {}

    for index, spot_name in enumerate(popular_areas[:4]):
        places.setdefault("tourist-spots", []).append(
            starter_place(
                spot_name,
                f"{spot_name}, {city_name}",
                center_lat + (index * 0.006),
                center_lng - (index * 0.004),
            )
        )

    for index, (category_slug, template) in enumerate(STARTER_CATEGORY_TEMPLATES.items()):
        name_template, address_template, lat_offset, lng_offset = template
        area = popular_areas[index % len(popular_areas)]
        places[category_slug] = [
            starter_place(
                name_template.format(area=area, city=city_name),
                address_template.format(area=area, city=city_name),
                center_lat + lat_offset,
                center_lng + lng_offset,
            )
        ]

    return places


def merge_starter_places(city_slug, places):
    starter_places = generated_starter_places(city_slug)
    changed = False

    for category_slug, starter_items in starter_places.items():
        if not places.get(category_slug):
            places[category_slug] = starter_items
            changed = True

    return places, changed


def normalize_city(city_value):
    city_slug = city_value.strip().lower().replace(" ", "-")
    return CITY_ALIASES.get(city_slug)


def city_file(city_slug):
    return DATA_DIR / CITIES[city_slug]["file"]


def load_guides():
    if not GUIDES_FILE.exists():
        return {}

    with GUIDES_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_guides(guides):
    DATA_DIR.mkdir(exist_ok=True)

    with GUIDES_FILE.open("w", encoding="utf-8") as file:
        json.dump(guides, file, indent=4, ensure_ascii=False)


def phone_digits(phone):
    return "".join(character for character in phone if character.isdigit())


def guide_with_links(guide):
    phone = guide.get("phone", "")
    digits = phone_digits(phone)
    guide = {**guide}
    guide["call_url"] = f"tel:{phone}"
    guide["whatsapp_url"] = f"https://wa.me/{digits}" if digits else ""
    return guide


def city_guides(city_slug):
    city_name = CITIES[city_slug]["name"]
    owner_guide = {
        **OWNER_GUIDE,
        "name": f"{city_name} Local Guide",
        "area": city_name,
        "note": f"Main local guide contact for {city_name}",
    }
    guides = load_guides().get(city_slug, [])
    return [guide_with_links(owner_guide), *(guide_with_links(guide) for guide in guides)]


def load_places(city_slug):
    places_file = city_file(city_slug)

    if not places_file.exists():
        starter_places = generated_starter_places(city_slug)
        try:
            save_places(city_slug, starter_places)
        except OSError:
            pass
        return starter_places

    with places_file.open("r", encoding="utf-8") as file:
        places = json.load(file)

    merged_places, changed = merge_starter_places(city_slug, places)
    if changed:
        try:
            save_places(city_slug, merged_places)
        except OSError:
            pass

    return merged_places


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
        categories=categories,
        guides=city_guides(city_slug),
        guide_error="",
        guide_success=""
    )


@app.route("/<city_slug>/guides/add", methods=["POST"])
def add_guide(city_slug):
    city_slug = normalize_city(city_slug) or city_slug

    if city_slug not in CITIES:
        return render_template("coming.html", city=city_slug), 404

    name = request.form.get("name", "").strip()
    phone = request.form.get("phone", "").strip()
    area = request.form.get("area", "").strip()
    note = request.form.get("note", "").strip()
    guide_error = ""
    guide_success = ""

    if name and phone:
        guides = load_guides()
        guides.setdefault(city_slug, []).append({
            "name": name,
            "phone": phone,
            "area": area or CITIES[city_slug]["name"],
            "note": note,
            "source": "Registered guide",
        })

        try:
            save_guides(guides)
        except OSError:
            guide_error = (
                "This live server cannot save guide registrations permanently. "
                "For permanent online registrations, connect a database later."
            )
        else:
            guide_success = "Guide registered successfully."
    else:
        guide_error = "Please enter at least your name and phone number."

    places = load_places(city_slug)
    categories = [
        {**category, "count": len(places.get(category["slug"], []))}
        for category in CATEGORIES
    ]
    return render_template(
        "mardan.html",
        city=CITIES[city_slug],
        city_slug=city_slug,
        categories=categories,
        guides=city_guides(city_slug),
        guide_error=guide_error,
        guide_success=guide_success
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
    app.run(debug=True, use_reloader=False)
