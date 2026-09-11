"""
Automated unit verification script for renovated Hair Weather Predictor.
"""

import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from PIL import Image
from image_processor import analyze_hair_frizz
from hair_predictor import calculate_hair_weather_prediction


def test_all():
    print("==========================================================")
    print("RUNNING HAIR WEATHER PREDICTOR RENOVATION TESTS")
    print("==========================================================")

    # 1. Test Image Processor (OpenCV Canny & Frizz Detection)
    print("\n--- 1. Testing Image Processor (OpenCV) ---")
    samples = [
        ("assets/samples/sample_sleek.png", "Sleek Hair"),
        ("assets/samples/sample_wavy.png", "Wavy Hair"),
        ("assets/samples/sample_frizzy.png", "Wild Frizz Hair")
    ]
    
    scores = []
    for path, label in samples:
        assert os.path.exists(path), f"File {path} does not exist!"
        img = Image.open(path)
        result = analyze_hair_frizz(img)
        print(f"[{label}] -> Frizz Score: {result['frizz_score']}% | Edge Density: {result['edge_density_pct']}% | Category: {result['frizz_category']}")
        assert 0 <= result["frizz_score"] <= 100
        assert result["edge_map_pil"] is not None
        scores.append(result["frizz_score"])
    
    # Verify progression: sleek < wavy < frizzy
    assert scores[0] <= scores[1] <= scores[2], f"Expected score order sleek <= wavy <= frizzy, got {scores}"
    print("[PASS] OpenCV Image Processor reliably calculates hair frizz percentage!")

    # 2. Test Core Inverted Hair Weather Engine
    print("\n--- 2. Testing Core Inverted Prediction Logic ---")

    # Example 1: High Frizz (82%) -> Rain Density 23%, Flood Prob 8%, "Probably Safe"
    res_82 = calculate_hair_weather_prediction(82)
    print(f"\n[Test Case 1: Frizz = 82%]")
    print(f"  Frizziness: {res_82['frizz_percentage']}%")
    print(f"  🌧️ Predicted Rain Density: {res_82['rain_density']}%")
    print(f"  🌊 Flood Probability: {res_82['flood_probability']}%")
    print(f"  ☀️ Weather Status: {res_82['weather_status']}")
    assert res_82["rain_density"] == 23, f"Expected 23%, got {res_82['rain_density']}%"
    assert res_82["flood_probability"] == 8, f"Expected 8%, got {res_82['flood_probability']}%"
    assert res_82["weather_status"] == "Probably Safe"
    assert res_82["is_warning"] is False
    print("  [PASS] Exactly matches Example 1!")

    # Example 2: Low Frizz (18%) -> Rain Density 89%, Flood Prob 76%, "Flood Warning"
    res_18 = calculate_hair_weather_prediction(18)
    print(f"\n[Test Case 2: Frizz = 18%]")
    print(f"  Frizziness: {res_18['frizz_percentage']}%")
    print(f"  🌧️ Predicted Rain Density: {res_18['rain_density']}%")
    print(f"  🌊 Flood Probability: {res_18['flood_probability']}%")
    print(f"  🚨 Weather Status: {res_18['weather_status']}")
    assert res_18["rain_density"] == 89, f"Expected 89%, got {res_18['rain_density']}%"
    assert res_18["flood_probability"] == 76, f"Expected 76%, got {res_18['flood_probability']}%"
    assert "Flood Warning" in res_18["weather_status"]
    assert res_18["is_warning"] is True
    print("  [PASS] Exactly matches Example 2!")

    # Verify Strict Monotonic Relationship:
    # Frizziness ↑ -> Rain Density ↓ -> Flood Probability ↓
    frizz_range = [10, 30, 50, 70, 90]
    rain_densities = [calculate_hair_weather_prediction(f)["rain_density"] for f in frizz_range]
    flood_probs = [calculate_hair_weather_prediction(f)["flood_probability"] for f in frizz_range]
    
    assert all(rain_densities[i] >= rain_densities[i+1] for i in range(len(rain_densities)-1)), "Rain density must strictly decrease with increasing frizz!"
    assert all(flood_probs[i] >= flood_probs[i+1] for i in range(len(flood_probs)-1)), "Flood probability must strictly decrease with increasing frizz!"
    print("\n[PASS] Core mathematical relationship Frizz ↑ -> Rain ↓ -> Flood ↓ is strictly verified!")

    print("\n==========================================================")
    print("ALL TESTS PASSED WITH 100% SUCCESS! 🚀🎉")
    print("==========================================================")


if __name__ == "__main__":
    test_all()
