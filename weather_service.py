"""
=============================================================================
HAIR RAIN PREDICTOR - Real Weather Service Module
=============================================================================
This module fetches REAL-TIME meteorological data for any city worldwide
using the free, open Open-Meteo API (no API key required!).

Data extracted:
- Temperature (°C)
- Relative Humidity (%) -> Key factor for hair frizz!
- Rain / Precipitation Probability (%)
- Wind Speed (km/h) -> Key factor for hair aerodynamic integrity!
- Weather Condition Text & Emojis

Also includes an offline fallback system so your college presentation
never breaks even if the campus Wi-Fi drops!
=============================================================================
"""

import requests
from typing import Dict, Any


# WMO Weather interpretation codes (WW)
WMO_WEATHER_CODES = {
    0: ("Clear sky ☀️", "Sunny and crisp. Hair has no external moisture threats."),
    1: ("Mainly clear 🌤️", "Slight cloud cover. Safe atmospheric conditions."),
    2: ("Partly cloudy ⛅", "Mild cloudiness. Atmospheric suspense is building."),
    3: ("Overcast ☁️", "Heavy cloud lid. Ambient moisture is lurking."),
    45: ("Foggy 🌫️", "Suspended water droplets everywhere. High frizz danger!"),
    48: ("Depositing rime fog 🌫️", "Extreme moisture contact hazard."),
    51: ("Light drizzle 🌦️", "Hair fibers are absorbing airborne mist."),
    53: ("Moderate drizzle 🌧️", "Noticeable water particles making contact."),
    55: ("Dense drizzle 🌧️", "Pre-rain state confirmed. Hair structure weakening."),
    61: ("Slight rain 🌧️", "Active rainfall. Hair umbrella protocol recommended."),
    63: ("Moderate rain 🌧️🌧️", "Direct liquid collision in progress."),
    65: ("Heavy rain ⛈️", "Full downpour. Extreme hair emergency."),
    71: ("Slight snow 🌨️", "Frozen precipitation detected."),
    73: ("Moderate snow ❄️", "Snow flakes landing on hair canopy."),
    75: ("Heavy snow ❄️❄️", "Sub-zero hair freezing potential."),
    80: ("Rain showers 🌦️", "Intermittent downpour threats."),
    81: ("Moderate showers 🌧️", "Sudden atmospheric attacks."),
    82: ("Violent rain showers ⛈️", "Atmospheric violence. Seek shelter."),
    95: ("Thunderstorm ⚡", "Lightning and rain. Maximum hair chaos guaranteed!"),
    96: ("Thunderstorm with hail ⚡", "Hail + electricity. Hair stands no chance."),
    99: ("Severe thunderstorm ⚡🌪️", "Apocalyptic hair weather.")
}


# Pre-configured backup cities in case the user has no internet connection
OFFLINE_PRESETS = {
    "London": {
        "city": "London, United Kingdom",
        "temperature": 16.5,
        "humidity": 84,
        "rain_probability": 78,
        "wind_speed": 18.2,
        "weather_code": 61,
        "weather_title": "Drizzle & Rain 🌧️",
        "weather_lore": "Classic British moisture. Prime hair inflation environment.",
        "is_simulated": True
    },
    "Mumbai": {
        "city": "Mumbai, India",
        "temperature": 31.0,
        "humidity": 92,
        "rain_probability": 85,
        "wind_speed": 22.5,
        "weather_code": 81,
        "weather_lore": "Tropical steam bath. Hair will expand by 300%.",
        "is_simulated": True
    },
    "New York": {
        "city": "New York, USA",
        "temperature": 22.0,
        "humidity": 55,
        "rain_probability": 25,
        "wind_speed": 14.0,
        "weather_code": 2,
        "weather_lore": "Breezy urban atmosphere. Hair remains moderately manageable.",
        "is_simulated": True
    },
    "Tokyo": {
        "city": "Tokyo, Japan",
        "temperature": 24.5,
        "humidity": 68,
        "rain_probability": 40,
        "wind_speed": 11.0,
        "weather_code": 3,
        "weather_lore": "Temperate overcast. Moderate electrostatic tension in the air.",
        "is_simulated": True
    },
    "Cairo (Desert)": {
        "city": "Cairo, Egypt",
        "temperature": 38.0,
        "humidity": 18,
        "rain_probability": 0,
        "wind_speed": 15.0,
        "weather_code": 0,
        "weather_lore": "Bone dry desert air. Hair is crisp and completely rain-proof.",
        "is_simulated": True
    }
}


def get_weather_for_city(city_name: str) -> Dict[str, Any]:
    """
    Fetches real-time weather data for any given city name using Open-Meteo.
    If the network fails or city is not found, gracefully falls back to simulated data.
    """
    cleaned_city = city_name.strip()
    if not cleaned_city:
        cleaned_city = "London"

    # Step 1: Geocoding (Convert city name to Latitude and Longitude)
    try:
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={cleaned_city}&count=1&language=en&format=json"
        geo_resp = requests.get(geo_url, timeout=5)
        geo_data = geo_resp.json()

        if not geo_data.get("results"):
            # City not found, use fallback
            fallback = OFFLINE_PRESETS.get(cleaned_city, OFFLINE_PRESETS["London"]).copy()
            fallback["warning"] = f"City '{cleaned_city}' not found in global atlas. Using simulated data."
            return fallback

        best_match = geo_data["results"][0]
        lat = best_match["latitude"]
        lon = best_match["longitude"]
        resolved_name = f"{best_match.get('name')}, {best_match.get('country', '')}"

        # Step 2: Fetch Live Meteorological Measurements
        weather_url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}&"
            f"current=temperature_2m,relative_humidity_2m,precipitation,weather_code,wind_speed_10m&"
            f"hourly=precipitation_probability&forecast_days=1"
        )
        weather_resp = requests.get(weather_url, timeout=5)
        weather_data = weather_resp.json()

        current = weather_data.get("current", {})
        hourly = weather_data.get("hourly", {})

        temperature = float(current.get("temperature_2m", 20.0))
        humidity = int(current.get("relative_humidity_2m", 50))
        wind_speed = float(current.get("wind_speed_10m", 10.0))
        weather_code = int(current.get("weather_code", 0))

        # Determine rain probability for the next few hours
        rain_probs = hourly.get("precipitation_probability", [0])
        # Look at the peak probability in the current forecast window
        rain_probability = int(max(rain_probs[:6])) if rain_probs else int(current.get("precipitation", 0) > 0) * 80

        wmo_info = WMO_WEATHER_CODES.get(weather_code, ("Variable Conditions 🌤️", "Atmospheric status uncertain."))

        return {
            "city": resolved_name,
            "latitude": lat,
            "longitude": lon,
            "temperature": round(temperature, 1),
            "humidity": humidity,
            "rain_probability": rain_probability,
            "wind_speed": round(wind_speed, 1),
            "weather_code": weather_code,
            "weather_title": wmo_info[0],
            "weather_lore": wmo_info[1],
            "is_simulated": False
        }

    except Exception as e:
        # Graceful fallback in case of internet outage or API issues
        preset_key = "London"
        for key in OFFLINE_PRESETS:
            if key.lower() in cleaned_city.lower():
                preset_key = key
                break
        fallback = OFFLINE_PRESETS[preset_key].copy()
        fallback["warning"] = f"Network unavailable ({str(e)}). Running in Offline College Presentation Mode."
        return fallback
