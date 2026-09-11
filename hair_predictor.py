"""
=============================================================================
💇‍♀️➡️🌧️ HAIR WEATHER PREDICTOR - Core Prediction Engine
=============================================================================
Core Mathematical Symmetrical Relationship:
  - High Frizz (Frizz ↑)  →  Rain Density ↓  →  Flood Prob ↓  →  🌵 Drought Prob ↑
  - Low Frizz  (Frizz ↓)  →  Rain Density ↑  →  Flood Prob ↑  →  🌵 Drought Prob ↓

Exact Target Points:
  - Frizz: 82% → Rain Density: 23% → Flood Prob: 8%  → Drought Prob: 76%
               → 🌵 DROUGHT WARNING: Hydrate Now, Your Hair Drank The Clouds! 😂
  - Frizz: 18% → Rain Density: 89% → Flood Prob: 76% → Drought Prob: 6%
               → 🚨 Flood Warning: Carry an Umbrella 😂
=============================================================================
"""

from typing import Dict, Any


def calculate_hair_weather_prediction(frizz_percentage: int) -> Dict[str, Any]:
    """
    Calculates the fictional weather prediction purely from the hair's frizziness level,
    including both Flood Probability (for sleek hair) and Drought Probability (for frizzy hair).

    Args:
        frizz_percentage (int): Measured hair frizziness from 0 to 100.

    Returns:
        dict containing rain_density, flood_probability, drought_probability,
        and funny weather status commands.
    """
    # Ensure frizz is bounded between 0 and 100
    frizz = max(0, min(100, int(frizz_percentage)))

    # 1. Calculate Predicted Rain Density (%)
    # Inverted linear relationship: Frizz ↑ -> Rain ↓
    # Passes through (82 -> 23%) and (18 -> 89%)
    raw_rain_density = 107.5 - (1.03 * frizz)
    rain_density = int(round(max(0, min(100, raw_rain_density))))

    # 2. Calculate Flood Probability (%)
    # Low Frizz -> High Rain -> High Flood Probability
    # Passes through (23% Rain -> 8% Flood) and (89% Rain -> 76% Flood)
    raw_flood_prob = (0.0077 * (rain_density ** 2)) + (0.17 * rain_density)
    flood_probability = int(round(max(0, min(100, raw_flood_prob))))

    # 3. Calculate Drought Probability (%)
    # High Frizz -> Absorbs all atmospheric moisture -> High Drought Probability!
    # Symmetrical to Flood Probability:
    # At 82% Frizz -> ~76% Drought
    # At 18% Frizz -> ~6% Drought
    raw_drought_prob = (0.0077 * (frizz ** 2)) + (0.17 * frizz)
    drought_probability = int(round(max(0, min(100, raw_drought_prob))))

    # 4. Funny Command Weather Status Determination
    if frizz >= 60:
        # High Frizz -> Extreme Drought Alert
        is_warning = True
        status_category = "DROUGHT"
        weather_status = "🌵 DROUGHT WARNING: Hydrate Now, Your Hair Drank The Clouds! 😂"
        status_icon = "🌵"
        status_subtitle = (
            "CRITICAL DEHYDRATION ALERT: Your excessive hair frizz has acted as an industrial "
            "moisture sponge. All clouds in a 10-mile radius have been vaporized. Bring a water bottle!"
        )
        status_class = "status-drought"

    elif frizz >= 40:
        # Moderate Frizz -> Atmospheric Suspense
        is_warning = False
        status_category = "MODERATE"
        weather_status = "🌤️ CLIMATE SUSPENSE: Your Hair is Negotiating With The Sky 🤨"
        status_icon = "🌤️"
        status_subtitle = (
            "Semi-frizzy state detected. The atmosphere cannot decide whether to trigger "
            "a localized downpour or turn into the Sahara Desert. Avoid sudden head movements."
        )
        status_class = "status-moderate"

    else:
        # Low Frizz (Sleek Hair) -> Catastrophic Flood Warning
        is_warning = True
        status_category = "FLOOD"
        weather_status = "🚨 Flood Warning: Carry an Umbrella 😂"
        status_icon = "🚨"
        status_subtitle = (
            "CATASTROPHIC FOLLICLE SMOOTHNESS: Your hair is dangerously sleek! "
            "Its zero-resistance aerodynamics have created a low-pressure vortex that is suctioning "
            "an entire monsoon directly above your head! Carry an umbrella or grab a lifejacket!"
        )
        status_class = "status-warning"

    return {
        "frizz_percentage": frizz,
        "rain_density": rain_density,
        "flood_probability": flood_probability,
        "drought_probability": drought_probability,
        "is_warning": is_warning,
        "status_category": status_category,
        "weather_status": weather_status,
        "status_icon": status_icon,
        "status_subtitle": status_subtitle,
        "status_class": status_class
    }
