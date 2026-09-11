"""
Helper script to generate demo hair images for the college presentation.
Creates 3 sample profiles:
1. Sleek & Smooth (Low Frizz)
2. Casual Wavy (Medium Frizz)
3. Wild Frizz Storm (High Frizz / Chaos)
"""

import os
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter


def generate_sample_images(output_dir="assets/samples"):
    os.makedirs(output_dir, exist_ok=True)
    width, height = 500, 500

    # 1. Sleek Smooth Hair (Minimal edges, smooth gradients)
    sleek_img = Image.new("RGB", (width, height), color=(240, 242, 245))
    draw_sleek = ImageDraw.Draw(sleek_img)
    # Head silhouette
    draw_sleek.ellipse([170, 160, 330, 380], fill=(225, 195, 170), outline=(200, 170, 145), width=2)
    # Sleek straight hair curtain
    for x in range(130, 370, 4):
        draw_sleek.line([(x, 110), (x, 420)], fill=(35, 25, 20), width=3)
    sleek_img = sleek_img.filter(ImageFilter.GaussianBlur(1))
    sleek_path = os.path.join(output_dir, "sample_sleek.png")
    sleek_img.save(sleek_path)

    # 2. Wavy / Medium Texture Hair
    wavy_img = Image.new("RGB", (width, height), color=(240, 242, 245))
    draw_wavy = ImageDraw.Draw(wavy_img)
    draw_wavy.ellipse([170, 160, 330, 380], fill=(225, 195, 170), outline=(200, 170, 145), width=2)
    for x in range(120, 380, 5):
        points = []
        phase = (x % 30) * 0.2
        for y in range(110, 430, 10):
            offset_x = int(math.sin(y * 0.05 + phase) * 16)
            points.append((x + offset_x, y))
        draw_wavy.line(points, fill=(45, 30, 20), width=3)
    wavy_path = os.path.join(output_dir, "sample_wavy.png")
    wavy_img.save(wavy_path)

    # 3. Wild Frizz Storm (Intense fractal edge chaos)
    frizz_img = Image.new("RGB", (width, height), color=(240, 242, 245))
    draw_frizz = ImageDraw.Draw(frizz_img)
    draw_frizz.ellipse([170, 160, 330, 380], fill=(225, 195, 170), outline=(200, 170, 145), width=2)
    np.random.seed(42)
    for _ in range(350):
        start_x = np.random.randint(110, 390)
        start_y = np.random.randint(90, 250)
        points = [(start_x, start_y)]
        curr_x, curr_y = start_x, start_y
        for _ in range(18):
            curr_x += np.random.randint(-12, 13)
            curr_y += np.random.randint(8, 20)
            points.append((curr_x, curr_y))
        color_val = np.random.randint(20, 55)
        draw_frizz.line(points, fill=(color_val, color_val // 2, 10), width=np.random.randint(1, 3))
    frizz_path = os.path.join(output_dir, "sample_frizzy.png")
    frizz_img.save(frizz_path)

    print(f"Demo sample hair images generated in: {output_dir}")


if __name__ == "__main__":
    generate_sample_images()
