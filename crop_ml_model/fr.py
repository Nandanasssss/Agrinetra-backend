import joblib
import pandas as pd

# -------------------------------------------------
# Load crop-wise average NPK requirement
# (created once during training)
# -------------------------------------------------
crop_npk = joblib.load("crop_npk_requirements.pkl")

# -------------------------------------------------
# Crop-specific allowed fertilizers
# (agronomy-based rules)
# -------------------------------------------------
CROP_FERTILIZER_RULES = {
    "Pulses": ["DAP", "MOP"],          # nitrogen fixing
    "Paddy": ["Urea", "DAP"],
    "Oil seeds": ["DAP", "MOP"],
    "Sugarcane": ["Urea", "MOP"],
    "Barley": ["Urea", "DAP"],
    "Tobacco": ["Urea", "DAP", "MOP"],
    "Ground Nuts": ["DAP", "MOP"],
    "Cotton": ["Urea", "DAP", "MOP"],
    "Millets": ["DAP"],
    "Maize": ["Urea", "DAP", "MOP"]
}

# -------------------------------------------------
# Fertilizer recommendation function
# -------------------------------------------------
def recommend_fertilizer(crop, soil_N, soil_P, soil_K):
    """
    Returns fertilizer recommendation based on:
    - soil NPK
    - crop NPK requirement
    - crop-specific fertilizer rules
    """

    if crop not in crop_npk.index:
        return ["General NPK"]

    required = crop_npk.loc[crop]
    fertilizers = []

    # 15% tolerance margin (realistic agriculture)
    margin = 0.85

    # Nitrogen
    if soil_N < required["Nitrogen"] * margin:
        if "Urea" in CROP_FERTILIZER_RULES.get(crop, []):
            fertilizers.append("Urea (Nitrogen)")

    # Phosphorous
    if soil_P < required["Phosphorous"] * margin:
        if "DAP" in CROP_FERTILIZER_RULES.get(crop, []):
            fertilizers.append("DAP (Phosphorous)")

    # Potassium
    if soil_K < required["Potassium"] * margin:
        if "MOP" in CROP_FERTILIZER_RULES.get(crop, []):
            fertilizers.append("MOP (Potassium)")

    if not fertilizers:
        return ["No fertilizer required"]

    return fertilizers
