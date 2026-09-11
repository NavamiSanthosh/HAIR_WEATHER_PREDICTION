"""
=============================================================================
HAIR RAIN PREDICTOR - Image Processing Module
=============================================================================
This module handles analyzing the uploaded hair photograph.
It uses OpenCV (Computer Vision) and NumPy to detect hair edges, roughness,
and texture density to calculate a humorous yet real "Hair Frizz Score" (0-100).

Why is this cool for a college competition?
Even though predicting rain from hair is completely ridiculous, the image
processing used here is 100% REAL computer vision!
=============================================================================
"""

import cv2
import numpy as np
from PIL import Image
import io


def load_image_to_cv2(image_input):
    """
    Converts various image input formats (PIL Image, bytes, or file-like object)
    into a standard OpenCV BGR image (NumPy array).
    """
    if isinstance(image_input, Image.Image):
        # Convert PIL to RGB then to OpenCV BGR
        rgb_image = np.array(image_input.convert("RGB"))
        return cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
    elif isinstance(image_input, (bytes, bytearray)):
        # Decode byte stream
        file_bytes = np.frombuffer(image_input, dtype=np.uint8)
        return cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    elif hasattr(image_input, "read"):
        # File-like object (e.g. Streamlit UploadedFile)
        file_bytes = np.frombuffer(image_input.read(), dtype=np.uint8)
        return cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    elif isinstance(image_input, np.ndarray):
        return image_input
    else:
        raise ValueError("Unsupported image format provided to load_image_to_cv2.")


def analyze_hair_frizz(image_input):
    """
    Analyzes an uploaded photo to measure hair texture chaos and frizz level.

    Steps:
    1. Resize image to a standard processing resolution (e.g., 600px width).
    2. Convert to Grayscale.
    3. Apply Gaussian Blur to filter out camera noise.
    4. Run Canny Edge Detection to identify wild stray hairs, texture, and edges.
    5. Compute Laplacian Variance to measure high-frequency visual chaos.
    6. Calculate Edge Density = (number of edge pixels / total pixels).
    7. Map edge density into an experimental Frizz Score from 0 to 100.
    8. Generate a colorful visual 'Frizz Radar Edge Map' for the dashboard.

    Returns:
        dict: {
            'frizz_score': int (0-100),
            'frizz_category': str (funny title),
            'edge_density_pct': float,
            'texture_variance': float,
            'edge_map_pil': PIL.Image (colorful visualization of detected hair strands),
            'gray_pil': PIL.Image
        }
    """
    # 1. Load image
    bgr_img = load_image_to_cv2(image_input)
    if bgr_img is None:
        raise ValueError("Could not decode image.")

    # Resize standardizing width to 600px to keep calculation consistent regardless of camera resolution
    h, w = bgr_img.shape[:2]
    target_width = 600
    target_height = int(h * (target_width / float(w)))
    resized_bgr = cv2.resize(bgr_img, (target_width, target_height), interpolation=cv2.INTER_AREA)

    # 2. Convert to Grayscale
    gray = cv2.cvtColor(resized_bgr, cv2.COLOR_BGR2GRAY)

    # 3. Gaussian Blur to reduce random sensor noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # 4. Canny Edge Detection
    # Thresholds tuned for hair strand contours
    edges = cv2.Canny(blurred, threshold1=45, threshold2=135)

    # 5. Laplacian Variance (measure of texture roughness/focus)
    laplacian = cv2.Laplacian(gray, cv2.CV_64F)
    variance = float(laplacian.var())

    # 6. Edge Density Calculation
    # Frizzy/curly/stray hair creates far more edge pixels than smooth/straight hair
    total_pixels = edges.shape[0] * edges.shape[1]
    edge_pixels = int(np.count_nonzero(edges))
    edge_density = (edge_pixels / total_pixels) * 100.0  # percentage (typically 1% to 15%)

    # 7. Map to Experimental Frizz Score (0 - 100)
    # Typical edge density for portraits with hair ranges from 0.5% (very smooth) to 12%+ (super wild frizz)
    if edge_density <= 2.0:
        base_frizz = (edge_density / 2.0) * 22.0
    elif edge_density <= 6.0:
        base_frizz = 22.0 + ((edge_density - 2.0) / 4.0) * 33.0  # 22 to 55
    elif edge_density <= 10.0:
        base_frizz = 55.0 + ((edge_density - 6.0) / 4.0) * 25.0  # 55 to 80
    else:
        base_frizz = 80.0 + min(20.0, ((edge_density - 10.0) / 5.0) * 20.0)  # 80 to 100

    # Add a slight texture variance bonus (capped)
    variance_bonus = min(8.0, np.log1p(variance) * 0.9)

    raw_score = base_frizz + variance_bonus
    frizz_score = int(np.clip(round(raw_score), 0, 100))

    # Determine funny Frizz Category
    if frizz_score <= 25:
        frizz_category = "Teflon Silk (0% Rebellion)"
        frizz_emoji = "✨"
        frizz_desc = "Your hair is behaving with suspiciously obedient aerodynamics."
    elif frizz_score <= 50:
        frizz_category = "Mild Static Wobble"
        frizz_emoji = "⚡"
        frizz_desc = "Minor rebel strands detected. Hair is contemplating freedom."
    elif frizz_score <= 75:
        frizz_category = "Dangerously Fluffy"
        frizz_emoji = "🦁"
        frizz_desc = "Significant atmospheric antenna formation. Frizz alert active!"
    else:
        frizz_category = "Category 5 Frizz Storm"
        frizz_emoji = "🌪️"
        frizz_desc = "Gravity has completely surrendered. Hair is ready to produce lightning."

    # 8. Create a Cyber/Scientific Edge Map Visualization
    # Create an electric cyan & neon magenta hair edge overlay
    edge_colored = np.zeros_like(resized_bgr)
    # Neon cyan for hair edges: B=255, G=240, R=20
    edge_colored[edges > 0] = [255, 240, 20]

    # Blend original slightly dimmed with bright edges for a cool sci-fi HUD look
    dimmed_original = cv2.convertScaleAbs(resized_bgr, alpha=0.45, beta=0)
    overlay = cv2.add(dimmed_original, edge_colored)
    overlay_rgb = cv2.cvtColor(overlay, cv2.COLOR_BGR2RGB)
    edge_map_pil = Image.fromarray(overlay_rgb)

    return {
        "frizz_score": frizz_score,
        "frizz_category": f"{frizz_emoji} {frizz_category}",
        "frizz_desc": frizz_desc,
        "edge_density_pct": round(edge_density, 2),
        "texture_variance": round(variance, 1),
        "edge_map_pil": edge_map_pil,
        "raw_edges_pil": Image.fromarray(edges),
        "original_pil": Image.fromarray(cv2.cvtColor(resized_bgr, cv2.COLOR_BGR2RGB))
    }
