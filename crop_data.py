# crop_data.py
# Shared crop database for GrowBot

CROPS = {
    "cassava": {
        "tip": "Plant at start of rainy season, doesn't need much water.",
        "soil": "Well-drained sandy loam",
        "spacing": "1m between rows, 1m between plants"
    },
    "rice": {
        "tip": "Needs a lot of water, plant in lowland areas.",
        "soil": "Heavy clay or clay loam",
        "spacing": "20cm between rows, 20cm between plants"
    },
    "yam": {
        "tip": "Needs deep loose soil, plant before rainy season.",
        "soil": "Deep, loose, well-drained soil",
        "spacing": "1m between mounds/ridges"
    },
    "beans": {
        "tip": "Needs moderate water, plant at start of rainy season.",
        "soil": "Well-drained loamy soil",
        "spacing": "60cm between rows, 20cm between plants"
    },
    "maize": {
        "tip": "Needs consistent water, plant at start of rainy season.",
        "soil": "Well-drained loamy soil",
        "spacing": "75cm between rows, 25cm between plants"
    },
    "sorghum": {
        "tip": "Drought-resistant, plant at start of rainy season.",
        "soil": "Well-drained loam or sandy loam",
        "spacing": "60cm between rows, 20cm between plants"
    },
    "millet": {
        "tip": "Grows well in dry conditions, plant at start of rainy season.",
        "soil": "Sandy loam or light soil",
        "spacing": "50cm between rows, 15cm between plants"
    },
    "groundnut": {
        "tip": "Plant at start of rainy season, harvest in 4-5 months.",
        "soil": "Light sandy loam, well-drained",
        "spacing": "60cm between rows, 20cm between plants"
    },
    "cocoyam": {
        "tip": "Plant at start of rainy season, prefers shade.",
        "soil": "Well-drained loamy soil",
        "spacing": "1m between rows, 80cm between plants"
    },
    "plantain": {
        "tip": "Plant at start of rainy season, needs consistent water.",
        "soil": "Deep, rich loamy soil",
        "spacing": "3m between rows, 3m between plants"
    },
    "okra": {
        "tip": "Plant at start of rainy season, harvest in 2-3 months.",
        "soil": "Well-drained sandy loam",
        "spacing": "60cm between rows, 30cm between plants"
    },
    "tomato": {
        "tip": "Plant at start of rainy season, stake for support.",
        "soil": "Well-drained loamy soil, rich in organic matter",
        "spacing": "90cm between rows, 45cm between plants"
    }
}

def get_crop_advice(crop):
    """Returns formatted advice for a crop, or a fallback message."""
    crop = crop.lower().strip()
    if crop in CROPS:
        info = CROPS[crop]
        return (
            f"\nAdvice for {crop.title()}:\n"
            f"- Tip: {info['tip']}\n"
            f"- Soil: {info['soil']}\n"
            f"- Spacing: {info['spacing']}"
        )
    return "\nWe don't have specific advice for that crop yet."

def get_crop_list():
    """Returns a comma-separated list of available crops."""
    return ", ".join(sorted(CROPS.keys()))