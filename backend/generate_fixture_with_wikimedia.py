"""
Erstellt initial_vehicles.json mit echten Wikimedia Commons Autobildern.
Einmalig lokal ausführen, dann die generierte JSON ins Repo einchecken.

Requirements: pip install requests
Usage: python generate_fixture_with_wikimedia.py
"""

import json
import random
import time
import urllib.request
import urllib.parse

random.seed(42)

# ── Fahrzeuge ─────────────────────────────────────────────────────────────────
entries = [
    ("BMW", "320d"), ("BMW", "520d"), ("BMW", "X3 xDrive20d"), ("BMW", "M3 Competition"),
    ("BMW", "118i"), ("BMW", "X5 xDrive40i"), ("BMW", "330e"), ("BMW", "M5"),
    ("BMW", "X1 sDrive18i"), ("BMW", "740d"), ("BMW", "X6 M50d"), ("BMW", "230i Cabrio"),
    ("Mercedes-Benz", "C 200"), ("Mercedes-Benz", "E 220d"), ("Mercedes-Benz", "GLC 300"),
    ("Mercedes-Benz", "A 180"), ("Mercedes-Benz", "S 500"), ("Mercedes-Benz", "CLA 200"),
    ("Mercedes-Benz", "GLE 350"), ("Mercedes-Benz", "C 300e"), ("Mercedes-Benz", "B 200"),
    ("Mercedes-Benz", "EQC 400"), ("Mercedes-Benz", "AMG GT 63"), ("Mercedes-Benz", "GLB 200"),
    ("Audi", "A3 Sportback"), ("Audi", "A4 Avant"), ("Audi", "Q5"), ("Audi", "A6 Limousine"),
    ("Audi", "Q3"), ("Audi", "A1 Citycarver"), ("Audi", "Q7"), ("Audi", "A5 Coupé"),
    ("Audi", "e-tron 55"), ("Audi", "RS3 Sportback"), ("Audi", "TT Roadster"), ("Audi", "Q8"),
    ("Volkswagen", "Golf 8"), ("Volkswagen", "Passat Variant"), ("Volkswagen", "Tiguan"),
    ("Volkswagen", "Polo"), ("Volkswagen", "ID.4"), ("Volkswagen", "Touareg"),
    ("Volkswagen", "T-Roc"), ("Volkswagen", "Arteon"), ("Volkswagen", "ID.3"),
    ("Volkswagen", "Golf GTI"), ("Volkswagen", "T-Cross"), ("Volkswagen", "Multivan"),
    ("Porsche", "911 Carrera S"), ("Porsche", "Cayenne GTS"), ("Porsche", "Macan S"),
    ("Porsche", "Panamera 4S"), ("Porsche", "Taycan Turbo"), ("Porsche", "718 Boxster"),
    ("Porsche", "911 Targa 4"), ("Porsche", "Cayenne E-Hybrid"),
    ("Toyota", "Corolla Touring Sports"), ("Toyota", "RAV4 Hybrid"), ("Toyota", "Yaris GR"),
    ("Toyota", "C-HR Hybrid"), ("Toyota", "Camry Hybrid"), ("Toyota", "Land Cruiser"),
    ("Toyota", "Prius"), ("Toyota", "bZ4X"),
    ("Ford", "Focus ST"), ("Ford", "Kuga PHEV"), ("Ford", "Puma ST-Line"),
    ("Ford", "Mustang GT"), ("Ford", "Explorer"), ("Ford", "Galaxy"),
    ("Ford", "Fiesta"), ("Ford", "Edge"),
    ("Opel", "Astra GS-Line"), ("Opel", "Insignia Grand Sport"), ("Opel", "Mokka-e"),
    ("Opel", "Corsa-e"), ("Opel", "Grandland Hybrid"), ("Opel", "Zafira Life"),
    ("Skoda", "Octavia Combi"), ("Skoda", "Superb L&K"), ("Skoda", "Kodiaq RS"),
    ("Skoda", "Karoq Scout"), ("Skoda", "Fabia Monte Carlo"), ("Skoda", "Enyaq iV 80"),
    ("Seat", "Leon Sportstourer"), ("Seat", "Ateca FR"), ("Seat", "Ibiza FR"),
    ("Seat", "Arona"), ("Seat", "Tarraco"), ("Cupra", "Formentor VZ"),
    ("Cupra", "Born"), ("Cupra", "Ateca"),
    ("Hyundai", "Tucson Hybrid"), ("Hyundai", "i30 N"), ("Hyundai", "Ioniq 5"),
    ("Hyundai", "Kona Electric"), ("Hyundai", "Santa Fe"),
    ("Kia", "Sportage GT-Line"), ("Kia", "EV6"), ("Kia", "Stinger GT"),
    ("Kia", "Niro Hybrid"), ("Kia", "Sorento"),
    ("Mazda", "CX-5"), ("Mazda", "MX-5"), ("Mazda", "3 Skyactiv-X"),
]
random.shuffle(entries)
entries = entries[:100]

# ── Wikimedia-Suchanfragen pro Modell ─────────────────────────────────────────
WIKI_QUERIES = {
    ("BMW", "320d"):                "BMW 320d F30",
    ("BMW", "520d"):                "BMW 520d F10",
    ("BMW", "X3 xDrive20d"):       "BMW X3 F25",
    ("BMW", "M3 Competition"):      "BMW M3 F80",
    ("BMW", "118i"):                "BMW 118i F40",
    ("BMW", "X5 xDrive40i"):       "BMW X5 G05",
    ("BMW", "330e"):                "BMW 330e G20",
    ("BMW", "M5"):                  "BMW M5 F90",
    ("BMW", "X1 sDrive18i"):       "BMW X1 F48",
    ("BMW", "740d"):                "BMW 740d G11",
    ("BMW", "X6 M50d"):            "BMW X6 G06",
    ("BMW", "230i Cabrio"):         "BMW 230i F23",
    ("Mercedes-Benz", "C 200"):     "Mercedes-Benz C200 W206",
    ("Mercedes-Benz", "E 220d"):    "Mercedes-Benz E220d W213",
    ("Mercedes-Benz", "GLC 300"):   "Mercedes-Benz GLC X253",
    ("Mercedes-Benz", "A 180"):     "Mercedes-Benz A180 W177",
    ("Mercedes-Benz", "S 500"):     "Mercedes-Benz S500 W223",
    ("Mercedes-Benz", "CLA 200"):   "Mercedes-Benz CLA C118",
    ("Mercedes-Benz", "GLE 350"):   "Mercedes-Benz GLE W167",
    ("Mercedes-Benz", "C 300e"):    "Mercedes-Benz C300e W206",
    ("Mercedes-Benz", "B 200"):     "Mercedes-Benz B200 W247",
    ("Mercedes-Benz", "EQC 400"):   "Mercedes-Benz EQC N293",
    ("Mercedes-Benz", "AMG GT 63"): "Mercedes-AMG GT63",
    ("Mercedes-Benz", "GLB 200"):   "Mercedes-Benz GLB X247",
    ("Audi", "A3 Sportback"):       "Audi A3 Sportback 8Y",
    ("Audi", "A4 Avant"):           "Audi A4 Avant B9",
    ("Audi", "Q5"):                 "Audi Q5 80A",
    ("Audi", "A6 Limousine"):       "Audi A6 C8",
    ("Audi", "Q3"):                 "Audi Q3 F3",
    ("Audi", "A1 Citycarver"):      "Audi A1 Citycarver GB",
    ("Audi", "Q7"):                 "Audi Q7 4M",
    ("Audi", "A5 Coupé"):          "Audi A5 Coupe F5",
    ("Audi", "e-tron 55"):          "Audi e-tron GE",
    ("Audi", "RS3 Sportback"):      "Audi RS3 Sportback 8Y",
    ("Audi", "TT Roadster"):        "Audi TT Roadster FV",
    ("Audi", "Q8"):                 "Audi Q8 4M",
    ("Volkswagen", "Golf 8"):       "Volkswagen Golf VIII",
    ("Volkswagen", "Passat Variant"): "Volkswagen Passat Variant B8",
    ("Volkswagen", "Tiguan"):       "Volkswagen Tiguan II",
    ("Volkswagen", "Polo"):         "Volkswagen Polo AW",
    ("Volkswagen", "ID.4"):         "Volkswagen ID.4",
    ("Volkswagen", "Touareg"):      "Volkswagen Touareg CR",
    ("Volkswagen", "T-Roc"):        "Volkswagen T-Roc",
    ("Volkswagen", "Arteon"):       "Volkswagen Arteon",
    ("Volkswagen", "ID.3"):         "Volkswagen ID.3",
    ("Volkswagen", "Golf GTI"):     "Volkswagen Golf GTI VIII",
    ("Volkswagen", "T-Cross"):      "Volkswagen T-Cross",
    ("Volkswagen", "Multivan"):     "Volkswagen Multivan T6",
    ("Porsche", "911 Carrera S"):   "Porsche 911 Carrera 992",
    ("Porsche", "Cayenne GTS"):     "Porsche Cayenne GTS",
    ("Porsche", "Macan S"):         "Porsche Macan 95B",
    ("Porsche", "Panamera 4S"):     "Porsche Panamera 971",
    ("Porsche", "Taycan Turbo"):    "Porsche Taycan",
    ("Porsche", "718 Boxster"):     "Porsche 718 Boxster 982",
    ("Porsche", "911 Targa 4"):     "Porsche 911 Targa 992",
    ("Porsche", "Cayenne E-Hybrid"): "Porsche Cayenne E-Hybrid",
    ("Toyota", "Corolla Touring Sports"): "Toyota Corolla Touring Sports E210",
    ("Toyota", "RAV4 Hybrid"):      "Toyota RAV4 Hybrid XA50",
    ("Toyota", "Yaris GR"):         "Toyota GR Yaris",
    ("Toyota", "C-HR Hybrid"):      "Toyota C-HR",
    ("Toyota", "Camry Hybrid"):     "Toyota Camry XV70",
    ("Toyota", "Land Cruiser"):     "Toyota Land Cruiser J300",
    ("Toyota", "Prius"):            "Toyota Prius XW60",
    ("Toyota", "bZ4X"):             "Toyota bZ4X",
    ("Ford", "Focus ST"):           "Ford Focus ST Mk4",
    ("Ford", "Kuga PHEV"):          "Ford Kuga PHEV",
    ("Ford", "Puma ST-Line"):       "Ford Puma ST-Line",
    ("Ford", "Mustang GT"):         "Ford Mustang S550",
    ("Ford", "Explorer"):           "Ford Explorer U625",
    ("Ford", "Galaxy"):             "Ford Galaxy Mk3",
    ("Ford", "Fiesta"):             "Ford Fiesta MK8",
    ("Ford", "Edge"):               "Ford Edge",
    ("Opel", "Astra GS-Line"):      "Opel Astra L",
    ("Opel", "Insignia Grand Sport"): "Opel Insignia B Grand Sport",
    ("Opel", "Mokka-e"):            "Opel Mokka B",
    ("Opel", "Corsa-e"):            "Opel Corsa F",
    ("Opel", "Grandland Hybrid"):   "Opel Grandland X",
    ("Opel", "Zafira Life"):        "Opel Zafira Life",
    ("Skoda", "Octavia Combi"):     "Skoda Octavia IV Combi",
    ("Skoda", "Superb L&K"):        "Skoda Superb III",
    ("Skoda", "Kodiaq RS"):         "Skoda Kodiaq RS",
    ("Skoda", "Karoq Scout"):       "Skoda Karoq",
    ("Skoda", "Fabia Monte Carlo"): "Skoda Fabia IV",
    ("Skoda", "Enyaq iV 80"):       "Skoda Enyaq",
    ("Seat", "Leon Sportstourer"):  "SEAT Leon IV Sportstourer",
    ("Seat", "Ateca FR"):           "SEAT Ateca",
    ("Seat", "Ibiza FR"):           "SEAT Ibiza V",
    ("Seat", "Arona"):              "SEAT Arona",
    ("Seat", "Tarraco"):            "SEAT Tarraco",
    ("Cupra", "Formentor VZ"):      "CUPRA Formentor",
    ("Cupra", "Born"):              "CUPRA Born",
    ("Cupra", "Ateca"):             "CUPRA Ateca",
    ("Hyundai", "Tucson Hybrid"):   "Hyundai Tucson NX4",
    ("Hyundai", "i30 N"):           "Hyundai i30 N",
    ("Hyundai", "Ioniq 5"):         "Hyundai IONIQ 5",
    ("Hyundai", "Kona Electric"):   "Hyundai Kona Electric",
    ("Hyundai", "Santa Fe"):        "Hyundai Santa Fe TM",
    ("Kia", "Sportage GT-Line"):    "Kia Sportage NQ5",
    ("Kia", "EV6"):                 "Kia EV6",
    ("Kia", "Stinger GT"):          "Kia Stinger GT",
    ("Kia", "Niro Hybrid"):         "Kia Niro HEV DE2",
    ("Kia", "Sorento"):             "Kia Sorento MQ4",
    ("Mazda", "CX-5"):              "Mazda CX-5 KF",
    ("Mazda", "MX-5"):              "Mazda MX-5 ND",
    ("Mazda", "3 Skyactiv-X"):      "Mazda3 BP",
}

# ── Wikimedia User-Agent (Pflicht laut https://meta.wikimedia.org/wiki/User-Agent_policy)
WIKIMEDIA_UA = (
    "FixtureGenerator/1.0 "
    "(https://github.com/yourname/yourproject; yourmail@example.com) "
    "Python-urllib/3.x"
)


def search_wikimedia(query, num_images=3, thumb_width=500):
    """Sucht Bilder auf Wikimedia Commons und gibt direkte Bild-URLs zurück.

    thumb_width muss ein Wert aus den offiziellen Wikimedia-Thumbnail-Stufen sein:
    20, 40, 60, 120, 250, 330, 500, 960, 1280, 1920, 3840
    Andere Werte werden von der API auf die nächste Stufe aufgerundet;
    beim direkten URL-Zugriff (Hotlinking) gibt es sonst einen 404/403.
    Siehe: https://w.wiki/GHai
    """
    params = {
        "action": "query",
        "generator": "search",
        "gsrsearch": f"filetype:bitmap {query} car",
        "gsrnamespace": "6",
        "prop": "imageinfo",
        "iiprop": "url",
        "iiurlwidth": str(thumb_width),   # Standard-Stufe verwenden
        "gsrlimit": str(num_images * 3),  # mehr holen, dann filtern
        "format": "json",
    }
    url = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(params)

    req = urllib.request.Request(
        url,
        headers={
            # Wikimedia blockt Anfragen ohne gültigen User-Agent mit 403
            "User-Agent": WIKIMEDIA_UA,
            "Accept": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
        pages = data.get("query", {}).get("pages", {})
        urls = []
        for page in pages.values():
            info = page.get("imageinfo", [{}])[0]
            img_url = info.get("thumburl") or info.get("url", "")
            # Nur echte Bildformate, keine SVG/PNG-Logos
            if img_url and any(img_url.lower().endswith(ext) for ext in [".jpg", ".jpeg", ".png"]):
                urls.append(img_url)
            if len(urls) >= num_images:
                break
        return urls
    except Exception as e:
        print(f"  Fehler bei '{query}': {e}")
        return []


# ── Fahrzeugdaten ─────────────────────────────────────────────────────────────
farben = ["Schwarz", "Weiß", "Silber", "Grau", "Blau", "Rot", "Grün", "Braun", "Beige", "Orange"]
ausstattungs_pool = [
    "Navi", "Klimaanlage", "Klimaautomatik", "Sitzheizung", "Lenkradheizung",
    "LED-Scheinwerfer", "Tempomat", "Adaptiver Tempomat", "Einparkhilfe hinten",
    "Einparkhilfe vorne", "Rückfahrkamera", "Apple CarPlay", "Android Auto",
    "Bluetooth", "DAB+ Radio", "Ledersitze", "Schiebedach", "Panoramadach",
    "Alufelgen", "Anhängerkupplung", "Spurhalteassistent", "Totwinkelassistent",
    "Notbremsassistent", "Head-Up-Display", "Ambientebeleuchtung", "Keyless Entry",
    "Elektrische Heckklappe", "360°-Kamera", "USB-Anschluss", "Matrix-LED",
    "Winterpaket", "Dachreling", "Memorysitze", "Elektrische Sitze", "ABS", "ESP",
]
beschreibungen = [
    "Gepflegtes Fahrzeug aus erster Hand. Nichtraucher, kein Unfallschaden.",
    "Sehr gut erhaltenes Fahrzeug mit lückenloser Servicehistorie.",
    "Scheckheftgepflegt beim Vertragshändler. Sofort fahrbereit.",
    "Traumhafter Zustand, wie neu. Alle Extras vorhanden.",
    "Familienauto in einwandfreiem Zustand. HU neu.",
    "Sportliches Fahrzeug mit vielen Extras. Nur an Selbstabholer.",
    "Technisch und optisch einwandfrei. Kein Rost.",
    "Toller Allrounder für Stadt und Autobahn. Niedrige Betriebskosten.",
    "Sparsames Fahrzeug in top Zustand. Tüv neu.",
    "Elegante Limousine mit vollständiger Ausstattung.",
]
electric_kw = ["e-tron", "ID.", "Taycan", "EQC", "Ioniq", "EV6", "Kona Electric", "Born", "Enyaq", "bZ4X", "Mokka-e", "Corsa-e"]
plugin_kw   = ["330e", "C 300e", "Kuga PHEV", "Grandland Hybrid", "Cayenne E-Hybrid", "RAV4 Hybrid", "C-HR Hybrid", "Prius", "Camry Hybrid", "Tucson Hybrid", "Niro Hybrid"]

FALLBACK_URLS = {
    "BMW":           "https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/BMW_3_Series_Sedan_%28F30%29_%E2%80%93_Frontansicht%2C_3._M%C3%A4rz_2012%2C_D%C3%BCsseldorf.jpg/960px-BMW_3_Series_Sedan_%28F30%29_%E2%80%93_Frontansicht%2C_3._M%C3%A4rz_2012%2C_D%C3%BCsseldorf.jpg",
    "Mercedes-Benz": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1f/2019_Mercedes-Benz_C-Class_%28W205%29_C_200_sedan_%282019-10-18%29_01.jpg/960px-2019_Mercedes-Benz_C-Class_%28W205%29_C_200_sedan_%282019-10-18%29_01.jpg",
    "Audi":          "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7d/2020_Audi_A4_%28B9%29_2.0_TDI_Avant_S_tronic.jpg/960px-2020_Audi_A4_%28B9%29_2.0_TDI_Avant_S_tronic.jpg",
    "Volkswagen":    "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/2020_Volkswagen_Golf_Style_2.0_TDI.jpg/960px-2020_Volkswagen_Golf_Style_2.0_TDI.jpg",
    "Porsche":       "https://upload.wikimedia.org/wikipedia/commons/thumb/1/18/Porsche_911_Carrera_4S_%28992%29%2C_IAA_2019%2C_Munich_%281X7A0309%29.jpg/960px-Porsche_911_Carrera_4S_%28992%29%2C_IAA_2019%2C_Munich_%281X7A0309%29.jpg",
    "Toyota":        "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9b/2019_Toyota_RAV4_XLE_AWD_%28facelift%2C_silver%29%2C_front_8.28.19.jpg/960px-2019_Toyota_RAV4_XLE_AWD_%28facelift%2C_silver%29%2C_front_8.28.19.jpg",
    "Ford":          "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/2022_Ford_Focus_ST_Facelift_in_Lucid_Red%2C_front_8.17.22.jpg/960px-2022_Ford_Focus_ST_Facelift_in_Lucid_Red%2C_front_8.17.22.jpg",
    "Opel":          "https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/2022_Opel_Astra_L_1.2_Turbo_GS_Line_in_Rubyrot%2C_front_8.20.22.jpg/960px-2022_Opel_Astra_L_1.2_Turbo_GS_Line_in_Rubyrot%2C_front_8.20.22.jpg",
    "Skoda":         "https://upload.wikimedia.org/wikipedia/commons/thumb/0/08/2021_Skoda_Octavia_IV_1.5_TSI_Combi_in_Race_Blue%2C_front_8.27.21.jpg/960px-2021_Skoda_Octavia_IV_1.5_TSI_Combi_in_Race_Blue%2C_front_8.27.21.jpg",
    "Seat":          "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/2020_SEAT_Leon_FR_1.5_TSI_in_Magnetic_Grey%2C_front_9.2.20.jpg/960px-2020_SEAT_Leon_FR_1.5_TSI_in_Magnetic_Grey%2C_front_9.2.20.jpg",
    "Cupra":         "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e8/2021_Cupra_Formentor_1.4_e-Hybrid_DSG_in_Petrol_Blue%2C_front_9.15.21.jpg/960px-2021_Cupra_Formentor_1.4_e-Hybrid_DSG_in_Petrol_Blue%2C_front_9.15.21.jpg",
    "Hyundai":       "https://upload.wikimedia.org/wikipedia/commons/thumb/1/10/2022_Hyundai_Tucson_1.6_T-GDi_MHEV_in_Phantom_Black%2C_front_8.10.22.jpg/960px-2022_Hyundai_Tucson_1.6_T-GDi_MHEV_in_Phantom_Black%2C_front_8.10.22.jpg",
    "Kia":           "https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/2022_Kia_Sportage_1.6_T-GDi_MHEV_in_Snow_White_Pearl%2C_front_9.21.22.jpg/960px-2022_Kia_Sportage_1.6_T-GDi_MHEV_in_Snow_White_Pearl%2C_front_9.21.22.jpg",
    "Mazda":         "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/2019_Mazda_CX-5_Sport_Nav%2B_2.0_Front.jpg/960px-2019_Mazda_CX-5_Sport_Nav%2B_2.0_Front.jpg",
}

# ── Hauptprogramm ─────────────────────────────────────────────────────────────
records, image_records, ph_records = [], [], []
vid, iid, pid = 1, 1, 1

url_cache = {}

for brand, model in entries:
    key = (brand, model)
    query = WIKI_QUERIES.get(key, f"{brand} {model}")

    print(f"[{vid}/100] {brand} {model} → suche '{query}' ...")

    if query not in url_cache:
        # 960px = nächste Standard-Stufe nach 500px (20,40,60,120,250,330,500,960,…)
        urls = search_wikimedia(query, num_images=3, thumb_width=960)
        if not urls:
            urls = [FALLBACK_URLS.get(brand, "https://picsum.photos/seed/1/800/600")]
        url_cache[query] = urls
        time.sleep(0.5)  # Rate-Limit: mind. 0.5 s zwischen Anfragen empfohlen
    else:
        urls = url_cache[query]

    year    = random.randint(2015, 2024)
    mileage = random.randint(0, 180000)
    price   = round(
        random.uniform(25000, 120000) if brand in ["Porsche", "BMW", "Mercedes-Benz"]
        else random.uniform(15000, 75000) if brand in ["Audi", "Volkswagen", "Cupra"]
        else random.uniform(8000, 45000), 2
    )

    if any(k in model for k in electric_kw):  kraftstoff = "elektro"
    elif any(k in model for k in plugin_kw):  kraftstoff = "plug_in"
    else: kraftstoff = random.choice(["benzin", "diesel", "benzin", "diesel", "hybrid"])

    getriebe = "automatik" if brand in ["Porsche", "Mercedes-Benz"] else random.choice(["manuell", "automatik", "halbautomatik"])
    month = str(random.randint(1, 12)).zfill(2)

    records.append({"model": "vehicles.vehicle", "pk": vid, "fields": {
        "brand": brand, "model": model, "year": year, "mileage": mileage,
        "price": str(price),
        "status": random.choices(["available", "reserved", "sold"], weights=[70, 15, 15])[0],
        "kraftstoff": kraftstoff, "getriebe": getriebe,
        "leistung": random.choice([90, 110, 130, 150, 163, 190, 204, 245, 306, 333, 400, 450, 510]),
        "farbe": random.choice(farben),
        "ez": f"{month}/{year}",
        "hu": f"{str(random.randint(1,12)).zfill(2)}/{random.randint(2025, 2027)}",
        "tueren": random.choice([2, 3, 4, 5]),
        "beschreibung": random.choice(beschreibungen),
        "ausstattung": random.sample(ausstattungs_pool, random.randint(5, 15)),
    }})

    for img_url in urls:
        image_records.append({"model": "vehicles.vehicleimage", "pk": iid, "fields": {
            "vehicle": vid,
            "image_url": img_url,
            "uploaded_at": f"{year}-{month}-01T10:00:00Z",
        }})
        iid += 1

    cur = price
    for i in range(random.randint(2, 3)):
        old = round(cur * random.uniform(1.03, 1.10), 2)
        ph_records.append({"model": "vehicles.pricehistory", "pk": pid, "fields": {
            "vehicle": vid, "price": str(old),
            "recorded_at": f"{max(2019, year - i)}-0{random.randint(1, 9)}-01",
            "note": "Preisanpassung",
        }})
        pid += 1
        cur = old

    vid += 1

fixture = records + image_records + ph_records
out = "vehicles/fixtures/initial_vehicles.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(fixture, f, ensure_ascii=False, indent=2)

print(f"\nFertig! {len(records)} Fahrzeuge, {len(image_records)} Bilder, {len(ph_records)} Preisverläufe")
print(f"→ {out}")