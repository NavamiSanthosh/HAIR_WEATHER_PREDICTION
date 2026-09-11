"""
=============================================================================
💇‍♀️➡️🌧️ REALISTIC AVATAR CHARACTER ENVIRONMENT (BASE64 IMAGE ENGINE)
=============================================================================
Layout:
   [LEFT DOCK: 👧 GIRL AVATAR]   [CENTER: MAIN UI]   [RIGHT DOCK: 👦 BOY AVATAR]

Renders realistic avatar characters for Girl (Left) and Boy (Right):
- State 1 (Home - Before Upload): Normal avatars with NO badge comments above their heads.
- State 2 (Drought): Frizzy hair realistic avatars + Drought result badges.
- State 3 (Rain): Smooth hair realistic avatars + Rain result badges.

100% self-contained with base64 embedded assets & smooth CSS keyframe animations.
=============================================================================
"""

import os
import base64


def _load_base64(path: str) -> str:
    """Reads image file and returns base64 Data URI string."""
    if os.path.exists(path):
        with open(path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")
            ext = "png" if path.endswith(".png") else "jpeg"
            return f"data:image/{ext};base64,{encoded}"
    return ""


def get_boy_girl_animation_html(status_category: str = None, frizz_percentage: int = None) -> str:
    """
    Renders realistic 3D avatar characters:
    - Left Dock: 👧 Girl Avatar
    - Right Dock: 👦 Boy Avatar
    Hides top badge comments in Home state (before hair upload).
    """
    if status_category is None or frizz_percentage is None:
        state = "HOME"
        frizz_val = 0
    elif status_category == "DROUGHT" or frizz_percentage >= 50:
        state = "DROUGHT"
        frizz_val = frizz_percentage
    else:
        state = "RAIN"
        frizz_val = frizz_percentage

    # Base paths
    assets_dir = os.path.join(os.path.dirname(__file__), "assets", "avatars")
    
    girl_smooth_b64 = _load_base64(os.path.join(assets_dir, "girl_smooth.jpg"))
    boy_smooth_b64 = _load_base64(os.path.join(assets_dir, "boy_smooth.jpg"))
    girl_frizzy_b64 = _load_base64(os.path.join(assets_dir, "girl_frizzy.jpg"))
    boy_frizzy_b64 = _load_base64(os.path.join(assets_dir, "boy_frizzy.jpg"))

    # Determine active images & badges
    if state == "DROUGHT":
        girl_img = girl_frizzy_b64 if girl_frizzy_b64 else girl_smooth_b64
        boy_img = boy_frizzy_b64 if boy_frizzy_b64 else boy_smooth_b64
        frame_class = "drought-avatar-frame"
        badge_class = "badge-drought-style"
        left_badge_html = f'<div class="side-label-badge {badge_class}">💇‍♀️ GIRL • FRIZZY ({frizz_val}%) ☀️</div>'
        right_badge_html = f'<div class="side-label-badge {badge_class}">👦 BOY • FRIZZY ({frizz_val}%) ☀️</div>'
    elif state == "RAIN":
        girl_img = girl_smooth_b64
        boy_img = boy_smooth_b64
        frame_class = "rain-avatar-frame"
        badge_class = "badge-rain-style"
        left_badge_html = f'<div class="side-label-badge {badge_class}">💇‍♀️ GIRL • SMOOTH ({frizz_val}%) 🌧️</div>'
        right_badge_html = f'<div class="side-label-badge {badge_class}">👦 BOY • SMOOTH ({frizz_val}%) 🌧️</div>'
    else: # HOME State (Before Upload) - Cancel badges above head!
        girl_img = girl_smooth_b64
        boy_img = boy_smooth_b64
        frame_class = "home-avatar-frame"
        left_badge_html = ""
        right_badge_html = ""

    raw_html = f"""
<style>
@keyframes avatarBreathing {{
  0%, 100% {{ transform: translateY(0) scale(1); }}
  50% {{ transform: translateY(-6px) scale(1.015); }}
}}

@keyframes badgeGlow {{
  0%, 100% {{ transform: translateX(-50%) scale(1); }}
  50% {{ transform: translateX(-50%) scale(1.03); }}
}}

.character-dock {{
  position: fixed;
  bottom: 16px;
  z-index: 999;
  pointer-events: none;
  transition: all 0.4s ease-in-out;
  animation: avatarBreathing 4.0s ease-in-out infinite;
}}

.dock-left-side {{
  left: 20px;
}}
.dock-right-side {{
  right: 20px;
}}

.avatar-card-container {{
  position: relative;
  width: 210px;
  border-radius: 22px;
  overflow: hidden;
  background: #ffffff;
  transition: all 0.4s ease;
}}

.drought-avatar-frame {{
  border: 3.5px solid #c66a3d !important;
  box-shadow: 0 14px 36px rgba(198, 106, 61, 0.4), 6px 6px 0px #49352a !important;
}}

.rain-avatar-frame {{
  border: 3.5px solid #3a7d7c !important;
  box-shadow: 0 14px 36px rgba(58, 125, 124, 0.4), 6px 6px 0px #293735 !important;
}}

.home-avatar-frame {{
  border: 3.5px solid #3a7d7c !important;
  box-shadow: 0 12px 28px rgba(0, 0, 0, 0.12), 5px 5px 0px #292524 !important;
}}

.avatar-img {{
  width: 100%;
  height: 270px;
  object-fit: cover;
  object-position: center top;
  display: block;
  transition: transform 0.4s ease;
}}

.side-label-badge {{
  position: absolute;
  top: -18px;
  left: 50%;
  transform: translateX(-50%);
  padding: 5px 14px;
  border-radius: 12px;
  font-family: 'Patrick Hand', cursive, sans-serif;
  font-size: 1.05rem;
  font-weight: 700;
  white-space: nowrap;
  box-shadow: 3px 3px 0px #292524;
  z-index: 20;
  animation: badgeGlow 3.5s ease-in-out infinite;
}}

.badge-drought-style {{
  background: #fff4e3;
  border: 2px solid #c66a3d;
  color: #49352a;
}}
.badge-rain-style {{
  background: #f7f5f0;
  border: 2px solid #3a7d7c;
  color: #293735;
}}

@media (max-width: 1340px) {{
  .avatar-card-container {{ width: 175px; }}
  .avatar-img {{ height: 220px; }}
  .dock-left-side {{ left: 8px; }}
  .dock-right-side {{ right: 8px; }}
}}

@media (max-width: 1060px) {{
  .character-dock {{ display: none; }}
}}
</style>

<!-- 👈 LEFT DOCK: 👧 GIRL AVATAR -->
<div class="character-dock dock-left-side">
  {left_badge_html}
  <div class="avatar-card-container {frame_class}">
    <img src="{girl_img}" class="avatar-img" alt="Girl Avatar" />
  </div>
</div>

<!-- 👉 RIGHT DOCK: 👦 BOY AVATAR -->
<div class="character-dock dock-right-side">
  <div class="side-label-badge-wrapper">
    {right_badge_html}
  </div>
  <div class="avatar-card-container {frame_class}">
    <img src="{boy_img}" class="avatar-img" alt="Boy Avatar" />
  </div>
</div>
"""

    clean_lines = [line.strip() for line in raw_html.splitlines() if line.strip()]
    return "\n".join(clean_lines)
