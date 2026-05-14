import json
from pathlib import Path

from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
DATA_DIR = Path(__file__).parent / "data"
PLACES_FILE = DATA_DIR / "mardan_places.json"

MARDAN_CATEGORIES = [
    {"name": "Restaurants", "slug": "restaurants"},
    {"name": "Hospitals", "slug": "hospitals"},
    {"name": "Petrol Pumps", "slug": "petrol-pumps"},
    {"name": "Shopping Malls", "slug": "shopping-malls"},
    {"name": "Pharmacies", "slug": "pharmacies"},
    {"name": "Wedding Halls", "slug": "wedding-halls"},
    {"name": "Hotels", "slug": "hotels"},
    {"name": "Tourist Spots", "slug": "tourist-spotss"},
    {"name": "Workshops", "slug": "workshops"},
    {"name": "Banks and ATMs", "slug": "banks-and-atms"},
]

MARDAN_PLACES = {
    "restaurants": [
        {"name": "Mardan Food Point", "address": "Bank Road, Mardan", "lat": 34.1989, "lng": 72.0452},
        {"name": "Takht Bhai Taste House", "address": "Nowshera Road, Mardan", "lat": 34.1937, "lng": 72.0525},
        {"name": "City Grill Mardan", "address": "Par Hoti, Mardan", "lat": 34.2045, "lng": 72.0368},
    ],
    "hospitals": [
        {"name": "Mardan Medical Center", "address": "Mall Road, Mardan", "lat": 34.2012, "lng": 72.0475},
        {"name": "City Care Hospital", "address": "Sheikh Maltoon Town, Mardan", "lat": 34.1868, "lng": 72.0641},
        {"name": "Life Line Clinic", "address": "Pakistan Chowk, Mardan", "lat": 34.1975, "lng": 72.0401},
    ],
    "petrol-pumps": [
        {"name": "Mardan Fuel Station", "address": "Charsadda Road, Mardan", "lat": 34.2071, "lng": 72.0493},
        {"name": "City Petrol Pump", "address": "Nowshera Road, Mardan", "lat": 34.1908, "lng": 72.0549},
        {"name": "Green Fuel Mardan", "address": "Katlang Road, Mardan", "lat": 34.2142, "lng": 72.0394},
    ],
    "shopping-malls": [
        {"name": "Mardan Shopping Plaza", "address": "Bank Road, Mardan", "lat": 34.1996, "lng": 72.0447},
        {"name": "City Mall Mardan", "address": "College Chowk, Mardan", "lat": 34.1941, "lng": 72.0469},
        {"name": "Family Shopping Center", "address": "Par Hoti, Mardan", "lat": 34.2059, "lng": 72.0357},
    ],
    "pharmacies": [
        {"name": "Care Pharmacy", "address": "Bank Road, Mardan", "lat": 34.1984, "lng": 72.0458},
        {"name": "Shaheen Medical Store", "address": "Pakistan Chowk, Mardan", "lat": 34.1969, "lng": 72.0413},
        {"name": "City Pharmacy", "address": "Sheikh Maltoon Town, Mardan", "lat": 34.1875, "lng": 72.0628},
        {"name": "Health Plus Pharmacy", "address": "Nowshera Road, Mardan", "lat": 34.1915, "lng": 72.0535},
    ],
    "wedding-halls": [
        {"name": "Royal Wedding Hall", "address": "Nowshera Road, Mardan", "lat": 34.1903, "lng": 72.0564},
        {"name": "Pearl Marquee", "address": "Sheikh Maltoon Town, Mardan", "lat": 34.1849, "lng": 72.0662},
        {"name": "Mardan Event Complex", "address": "Katlang Road, Mardan", "lat": 34.2117, "lng": 72.0405},
    ],
    "hotels": [
        {"name": "Mardan City Hotel", "address": "Bank Road, Mardan", "lat": 34.1992, "lng": 72.0442},
        {"name": "Green Palace Hotel", "address": "Mall Road, Mardan", "lat": 34.2017, "lng": 72.0482},
        {"name": "Comfort Inn Mardan", "address": "Sheikh Maltoon Town, Mardan", "lat": 34.1858, "lng": 72.0636},
    ],
    "tourist-spots": [
        {"name": "Mardan Museum Area", "address": "Mardan City", "lat": 34.2008, "lng": 72.0464},
        {"name": "Takht-i-Bahi View Route", "address": "Takht Bhai Road", "lat": 34.2877, "lng": 71.9469},
        {"name": "Park View Point", "address": "Sheikh Maltoon Town, Mardan", "lat": 34.1861, "lng": 72.0653},
    ],
    "workshops": [
        {"name": "Auto Care Workshop", "address": "Nowshera Road, Mardan", "lat": 34.1924, "lng": 72.0551},
        {"name": "Mardan Motors Workshop", "address": "Charsadda Road, Mardan", "lat": 34.2068, "lng": 72.0508},
        {"name": "Quick Fix Garage", "address": "Par Hoti, Mardan", "lat": 34.2052, "lng": 72.0376},
    ],
    "banks-and-atms": [
        {"name": "City Bank ATM", "address": "Bank Road, Mardan", "lat": 34.1988, "lng": 72.0449},
        {"name": "Mardan Cash Point", "address": "Pakistan Chowk, Mardan", "lat": 34.1972, "lng": 72.0406},
        {"name": "Family ATM Center", "address": "Sheikh Maltoon Town, Mardan", "lat": 34.1863, "lng": 72.0644},
    ],
}

def load_places():
    if not PLACES_FILE.exists():
        try:
            save_places(MARDAN_PLACES)
        except OSError:
            pass
        return MARDAN_PLACES

    with PLACES_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)

def save_places(places):
    DATA_DIR.mkdir(exist_ok=True)

    with PLACES_FILE.open("w", encoding="utf-8") as file:
        json.dump(places, file, indent=4)

def find_category(category_slug):
    return next(
        (item for item in MARDAN_CATEGORIES if item["slug"] == category_slug),
        None
    )

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/mardan")
def mardan():
    places = load_places()
    categories = [
        {**category, "count": len(places.get(category["slug"], []))}
        for category in MARDAN_CATEGORIES
    ]
    return render_template("mardan.html", categories=categories)

@app.route("/mardan/add", methods=["GET", "POST"])
def add_place():
    selected_category = request.args.get("category", "pharmacies")
    error = ""

    if request.method == "POST":
        category_slug = request.form.get("category", "").strip()
        name = request.form.get("name", "").strip()
        address = request.form.get("address", "").strip()
        lat = request.form.get("lat", "").strip()
        lng = request.form.get("lng", "").strip()

        if category_slug and name and address and lat and lng:
            places = load_places()
            places.setdefault(category_slug, []).append({
                "name": name,
                "address": address,
                "lat": float(lat),
                "lng": float(lng),
                "source": "Added manually",
            })
            try:
                save_places(places)
            except OSError:
                error = (
                    "This live server cannot save files permanently. "
                    "For permanent online additions, connect a database later."
                )
            else:
                return redirect(url_for("mardan_category", category_slug=category_slug))

        elif not error:
            error = "Please fill all fields and select a map location."

        selected_category = category_slug or selected_category

    return render_template(
        "add_place.html",
        categories=MARDAN_CATEGORIES,
        selected_category=selected_category,
        error=error
    )

@app.route("/search")
def search():
    city = request.args.get("city", "").strip().lower()

    if city == "mardan":
        return mardan()
    else:
        return render_template("coming.html", city=city)

@app.route("/mardan/<category_slug>")
def mardan_category(category_slug):
    category = find_category(category_slug)

    if category is None:
        category = {"name": category_slug.replace("-", " ").title()}

    places = load_places().get(category_slug, [])

    return render_template(
        "category_coming.html",
        category=category["name"],
        category_slug=category_slug,
        places=places,
        place_count=len(places)
    )

if __name__ == "__main__":
    app.run(debug=True)
