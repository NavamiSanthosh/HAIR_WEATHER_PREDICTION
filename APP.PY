"""
=============================================================================
💇‍♀️ HAIR WEATHER PREDICTOR
"Your hair today. Our weather prediction tomorrow." 😂
=============================================================================
College "Useless Project" Competition Entry
Architecture:
  📸 Hair Photo Upload
         ↓
  💇‍♀️ Frizziness Detection (OpenCV Canny Edges & Texture Analysis)
         ↓
  🌧️ Predicted Rain Density
         ↓
  🌊 Flood Probability
         ↓
  ☀️ / 🚨 Weather Status (State 2: Drought | State 3: Rain)
=============================================================================
"""

import os
import streamlit as st
from PIL import Image
import numpy as np

# Import custom modules
from image_processor import analyze_hair_frizz
from hair_predictor import calculate_hair_weather_prediction
from cartoon_animator import get_boy_girl_animation_html


def render_html(html_str: str):
    """Cleanly renders HTML without markdown parsing leading spaces as code blocks."""
    cleaned = "\n".join(line.strip() for line in html_str.splitlines() if line.strip())
    st.markdown(cleaned, unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 1. STREAMLIT PAGE CONFIG & SESSION STATE
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Hair Weather Predictor 💇‍♀️🌧️",
    page_icon="💇‍♀️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Initialize Session State
if "analyzed_image" not in st.session_state:
    st.session_state["analyzed_image"] = None
if "analysis_done" not in st.session_state:
    st.session_state["analysis_done"] = False
if "uploader_key" not in st.session_state:
    st.session_state["uploader_key"] = 0


# Determine Active State & Theme Colors
active_img = st.session_state.get("analyzed_image")
analysis_done = st.session_state.get("analysis_done", False)

current_frizz = None
current_status = None
cv_res = None
pred_res = None

if active_img is not None and analysis_done:
    try:
        cv_res = analyze_hair_frizz(active_img)
        if "demo_frizz_override" in st.session_state:
            frizz_val = st.session_state["demo_frizz_override"]
        else:
            frizz_val = cv_res["frizz_score"]
        pred_res = calculate_hair_weather_prediction(frizz_val)
        current_frizz = pred_res["frizz_percentage"]
        current_status = pred_res["status_category"]
    except Exception as e:
        cv_res = None
        pred_res = None

# Color themes based on State:
# State 1 (Home): Cream (#FFF8EF), text #3B3028, accent #3A7D7C
# State 2 (Drought): Warm Sand (#F7E6C4), card #FFF4E3, text #49352A, accent #C66A3D
# State 3 (Rain): Misty Teal (#DCE8E7), card #F7F5F0, text #293735, accent #3A7D7C
if current_status == "DROUGHT" or (current_frizz is not None and current_frizz >= 50):
    theme_bg = "#F7E6C4"
    theme_card_bg = "#FFF4E3"
    theme_text = "#49352A"
    theme_accent = "#C66A3D"
    theme_border = "#C66A3D"
elif current_status is not None and current_frizz is not None:
    theme_bg = "#DCE8E7"
    theme_card_bg = "#F7F5F0"
    theme_text = "#293735"
    theme_accent = "#3A7D7C"
    theme_border = "#3A7D7C"
else:
    theme_bg = "#FFF8EF"
    theme_card_bg = "#FFFFFF"
    theme_text = "#3B3028"
    theme_accent = "#3A7D7C"
    theme_border = "#3A7D7C"


# -----------------------------------------------------------------------------
# 2. DYNAMIC THEME STYLING
# -----------------------------------------------------------------------------
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Caveat:wght@600;700&family=Patrick+Hand&family=Plus+Jakarta+Sans:wght@500;600;700;800;900&family=JetBrains+Mono:wght@600;800&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Plus Jakarta Sans', sans-serif;
    }}

    .stApp {{
        background-color: {theme_bg} !important;
        background-image: 
            radial-gradient(rgba(0,0,0,0.06) 1.1px, transparent 1.1px),
            radial-gradient(rgba(0,0,0,0.06) 1.1px, {theme_bg} 1.1px) !important;
        background-size: 26px 26px !important;
        background-position: 0 0, 13px 13px !important;
        color: {theme_text} !important;
        transition: background-color 0.5s ease;
    }}

    .block-container {{
        max-width: 780px !important;
        padding-top: 1.5rem !important;
        padding-bottom: 4rem !important;
    }}

    .hero-container {{
        text-align: center;
        padding: 16px 10px 24px 10px;
    }}

    .hero-badge {{
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: #fef08a;
        border: 2px dashed {theme_accent};
        color: {theme_text};
        padding: 6px 20px;
        border-radius: 8px;
        font-family: 'Patrick Hand', cursive;
        font-size: 1.1rem;
        font-weight: 700;
        box-shadow: 3px 3px 0px #292524;
        transform: rotate(-1deg);
        margin-bottom: 12px;
    }}

    .hero-title {{
        font-size: 2.6rem;
        font-weight: 900;
        color: {theme_text};
        margin: 0;
        line-height: 1.15;
        letter-spacing: -0.5px;
    }}

    .hero-subtitle {{
        font-family: 'Caveat', cursive;
        font-size: 1.45rem;
        color: {theme_text};
        font-weight: 700;
        margin-top: 8px;
        margin-bottom: 0;
        opacity: 0.9;
    }}

    .glass-card {{
        background: {theme_card_bg} !important;
        border: 2.5px solid {theme_border} !important;
        border-radius: 18px !important;
        padding: 24px !important;
        box-shadow: 6px 6px 0px rgba(0, 0, 0, 0.15) !important;
        margin-bottom: 24px !important;
        position: relative !important;
    }}

    .metric-grid-3 {{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 14px;
        margin-bottom: 24px;
    }}

    @media (max-width: 640px) {{
        .metric-grid-3 {{
            grid-template-columns: 1fr;
        }}
    }}

    .metric-card {{
        background: {theme_card_bg};
        border: 2.5px solid {theme_border};
        border-radius: 14px;
        padding: 18px 12px;
        text-align: center;
        box-shadow: 4px 4px 0px rgba(0,0,0,0.12);
    }}

    .metric-icon {{
        font-size: 1.8rem;
        margin-bottom: 4px;
    }}

    .metric-name {{
        font-family: 'Patrick Hand', cursive;
        font-size: 1.1rem;
        color: {theme_text};
        font-weight: 700;
        margin-bottom: 2px;
    }}

    .metric-value {{
        font-size: 2.4rem;
        font-weight: 900;
        font-family: 'JetBrains Mono', monospace;
        line-height: 1;
        margin: 6px 0;
    }}

    .status-card {{
        border-radius: 18px;
        padding: 26px 20px;
        text-align: center;
        margin-bottom: 24px;
        border: 3px solid {theme_border};
        background: {theme_card_bg};
        box-shadow: 6px 6px 0px rgba(0,0,0,0.15);
    }}

    .status-header-text {{
        font-size: 1.9rem;
        font-weight: 900;
        margin: 8px 0 10px 0;
        color: {theme_text};
    }}

    .status-desc-text {{
        font-family: 'Patrick Hand', cursive;
        font-size: 1.3rem;
        color: {theme_text};
        max-width: 580px;
        margin: 0 auto;
        line-height: 1.4;
    }}

    .frizz-meter-container {{
        background: {theme_card_bg} !important;
        border: 2.5px solid {theme_border} !important;
        border-radius: 16px !important;
        padding: 20px !important;
        text-align: center !important;
        box-shadow: 5px 5px 0px rgba(0,0,0,0.12) !important;
    }}

    .frizz-number {{
        font-size: 3.8rem;
        font-weight: 900;
        font-family: 'JetBrains Mono', monospace;
        color: {theme_text};
        line-height: 1;
        margin: 6px 0 10px 0;
    }}

    .stButton > button {{
        width: 100% !important;
        background: {theme_accent} !important;
        color: #ffffff !important;
        border: 2.5px solid #292524 !important;
        border-radius: 12px !important;
        padding: 12px 22px !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 800 !important;
        font-size: 1.1rem !important;
        box-shadow: 4px 4px 0px #292524 !important;
        transition: all 0.15s ease !important;
    }}

    .stButton > button:hover {{
        transform: translate(2px, 2px) !important;
        box-shadow: 2px 2px 0px #292524 !important;
    }}

    .stTabs [data-baseweb="tab-list"] {{
        gap: 6px !important;
        background-color: transparent !important;
        padding: 4px 0 !important;
        border-bottom: 2px solid {theme_border} !important;
    }}

    .stTabs [data-baseweb="tab"] {{
        border-radius: 8px 8px 0 0 !important;
        background: rgba(0,0,0,0.05) !important;
        border: 2px solid {theme_border} !important;
        border-bottom: none !important;
        color: {theme_text} !important;
        font-weight: 700 !important;
        font-family: 'Patrick Hand', cursive !important;
        font-size: 1.15rem !important;
        padding: 8px 18px !important;
    }}

    .stTabs [aria-selected="true"] {{
        background: {theme_card_bg} !important;
        font-weight: 900 !important;
    }}

    [data-testid="stFileUploader"] {{
        background: {theme_card_bg} !important;
        border: 2.5px dashed {theme_border} !important;
        border-radius: 14px !important;
        padding: 16px !important;
    }}

    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
</style>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 3. HEADER
# -----------------------------------------------------------------------------
st.markdown(f"""
<div class="hero-container">
    <div class="hero-badge">Hair Weather Predictor</div>
    <h1 class="hero-title">Hair Weather PREDICTOR</h1>
    <p class="hero-subtitle">Upload your hair photo and let us predict the weather based on your hair frizziness!</p>
</div>
""", unsafe_allow_html=True)


# Render Dual-Side Character Environment (Girl on Left, Boy on Right)
render_html(get_boy_girl_animation_html(current_status, current_frizz))


# -----------------------------------------------------------------------------
# 4. MAIN CONTENT WORKFLOW
# -----------------------------------------------------------------------------

# STATE 1: Home / Upload Section (When no analysis done yet)
if not analysis_done or active_img is None:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div style="font-weight: 800; font-size: 1.15rem; margin-bottom: 12px; text-align: center;">📸 Upload Hair Photo</div>', unsafe_allow_html=True)

    tab_upload, tab_camera, tab_samples = st.tabs(["📁 Upload Photo", "📷 Live Camera", "🧪 Quick Demo Samples"])

    with tab_upload:
        u_key = f"uploader_{st.session_state.get('uploader_key', 0)}"
        uploaded_file = st.file_uploader(
            "Drag & drop your photo here",
            type=["jpg", "jpeg", "png", "webp"],
            key=u_key,
            label_visibility="visible"
        )
        if uploaded_file is not None:
            st.session_state["analyzed_image"] = uploaded_file

    with tab_camera:
        cam_photo = st.camera_input("Take a quick photo of your hair:")
        if cam_photo is not None:
            st.session_state["analyzed_image"] = cam_photo

    with tab_samples:
        st.caption("Quick sample presets for live presentation:")
        sample_col1, sample_col2, sample_col3 = st.columns(3)
        with sample_col1:
            if st.button("✨ Sleek Hair\n(18% Frizz)", use_container_width=True, key="btn_sample_sleek"):
                sample_path = "assets/samples/sample_sleek.png"
                if os.path.exists(sample_path):
                    st.session_state["analyzed_image"] = Image.open(sample_path)
                    st.session_state["demo_frizz_override"] = 18
                    st.session_state["analysis_done"] = True
                    st.rerun()
        with sample_col2:
            if st.button("🦁 Wavy Hair\n(52% Frizz)", use_container_width=True, key="btn_sample_wavy"):
                sample_path = "assets/samples/sample_wavy.png"
                if os.path.exists(sample_path):
                    st.session_state["analyzed_image"] = Image.open(sample_path)
                    st.session_state["demo_frizz_override"] = 52
                    st.session_state["analysis_done"] = True
                    st.rerun()
        with sample_col3:
            if st.button("🌪️ Wild Frizz\n(82% Frizz)", use_container_width=True, key="btn_sample_frizzy"):
                sample_path = "assets/samples/sample_frizzy.png"
                if os.path.exists(sample_path):
                    st.session_state["analyzed_image"] = Image.open(sample_path)
                    st.session_state["demo_frizz_override"] = 82
                    st.session_state["analysis_done"] = True
                    st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    # Action Button to launch analysis
    if st.session_state.get("analyzed_image") is not None:
        if st.button("🔍 Analyze Hair", use_container_width=True, key="btn_analyze_launch"):
            st.session_state["analysis_done"] = True
            st.rerun()

# STATE 2 / STATE 3: Results Displayed (After Analysis)
else:
    if cv_res and pred_res:
        frizz_pct = pred_res["frizz_percentage"]
        status_cat = pred_res["status_category"]
        is_drought = (status_cat == "DROUGHT") or (frizz_pct >= 50)

        # Photo Preview Card
        st.markdown('<div class="glass-card" style="text-align: center;">', unsafe_allow_html=True)
        img_col1, img_col2 = st.columns(2, gap="medium")
        with img_col1:
            st.image(cv_res["original_pil"], caption="📸 Input Hair Photo", use_container_width=True)
        with img_col2:
            st.image(cv_res["edge_map_pil"], caption=f"🔬 Canny Edge Map ({cv_res['edge_density_pct']}%)", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Hair Frizziness Meter
        frizz_badge = "HIGH" if is_drought else "LOW"
        frizz_badge_bg = "#C66A3D" if is_drought else "#3A7D7C"

        render_html(f"""
<div class="glass-card frizz-meter-container">
    <div style="font-size: 1.15rem; font-weight: 800; text-transform: uppercase; letter-spacing: 1px;">
        💇‍♀️ Hair Frizziness
    </div>
    <div class="frizz-number">{frizz_pct}%</div>
    <div>
        <span style="background: {frizz_badge_bg}; color: #ffffff; padding: 4px 16px; border-radius: 20px; font-weight: 900; font-size: 0.95rem;">
            {frizz_badge} FRIZZINESS
        </span>
    </div>
</div>
""")

        # 3-Column Metrics Grid
        rain_val = pred_res["rain_density"]
        flood_val = pred_res["flood_probability"]
        drought_val = pred_res["drought_probability"]

        render_html(f"""
<div class="metric-grid-3">
    <div class="metric-card">
        <div class="metric-icon">🌧️</div>
        <div class="metric-name">Rain Density</div>
        <div class="metric-value">{rain_val}%</div>
    </div>
    <div class="metric-card">
        <div class="metric-icon">🌊</div>
        <div class="metric-name">Flood Probability</div>
        <div class="metric-value">{flood_val}%</div>
    </div>
    <div class="metric-card">
        <div class="metric-icon">🌵</div>
        <div class="metric-name">Drought Risk</div>
        <div class="metric-value">{drought_val}%</div>
    </div>
</div>
""")

        # Weather Status Card
        if is_drought:
            status_title = "Dry / Drought Chances"
            status_desc = "High hair frizz absorbs atmospheric moisture, indicating extreme dry weather and drought conditions ahead!"
            status_icon = "☀️"
            st.balloons()
        else:
            status_title = "Rain Likely / Higher Chances"
            status_desc = "Smooth low-frizz hair means high atmospheric moisture content and imminent rainfall!"
            status_icon = "🌧️"
            st.snow()

        render_html(f"""
<div class="status-card">
    <div style="font-size: 3.2rem; margin-bottom: 6px;">{status_icon}</div>
    <div class="status-header-text">{status_title}</div>
    <div class="status-desc-text">{status_desc}</div>
</div>
""")

        # Analyze Another Image Button
        st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
        if st.button("🔄 Analyze Another Image", use_container_width=True, key="btn_analyze_another"):
            st.session_state["analyzed_image"] = None
            st.session_state["analysis_done"] = False
            if "demo_frizz_override" in st.session_state:
                del st.session_state["demo_frizz_override"]
            st.session_state["uploader_key"] = st.session_state.get("uploader_key", 0) + 1
            st.rerun()


