import sys
sys.stdout.reconfigure(encoding="utf-8")
from hair_predictor import calculate_hair_weather_prediction

cases = [
    ("Wild Frizz (82%)", 82),
    ("Wavy Hair (52%)", 52),
    ("Sleek Hair (18%)", 18),
]
for label, frizz in cases:
    p = calculate_hair_weather_prediction(frizz)
    print(f"\n[{label}]")
    print(f"  Rain Density:       {p['rain_density']}%")
    print(f"  Flood Probability:  {p['flood_probability']}%")
    print(f"  Drought Probability:{p['drought_probability']}%")
    print(f"  Status Category:    {p['status_category']}")
    print(f"  Weather Status:     {p['weather_status']}")
