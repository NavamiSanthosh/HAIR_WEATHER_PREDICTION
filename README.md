# 💇‍♀️ HAIR WEATHER PREDICTOR
### *"Your hair today. Our weather prediction tomorrow." 😂*

> **🏆 College "Useless Project" Competition Entry**  
> Takes an uploaded photo of a person's hair, calculates the hair's **frizziness percentage** using real Computer Vision (OpenCV), and generates a completely fictional, inverted weather prediction!

---

## 🌟 The Core Concept & Mathematical Relationship

The application operates on an inverted follicular-meteorological paradox:

$$\text{Frizziness} \uparrow \quad \longrightarrow \quad \text{Rain Density} \downarrow \quad \longrightarrow \quad \text{Flood Probability} \downarrow$$
$$\text{Frizziness} \downarrow \quad \longrightarrow \quad \text{Rain Density} \uparrow \quad \longrightarrow \quad \text{Flood Probability} \uparrow$$

### Real Examples:
- 📸 **High Frizz Hair (e.g., 82% Frizz)**:
  - 🌧️ **Predicted Rain Density: 23%**
  - 🌊 **Flood Probability: 8%**
  - ☀️ **Weather Status: Probably Safe**  
  *(Satirical lore: Your electrostatic hair frizz cloud acts as a deflector shield, pushing rain clouds far away!)*
  
- 📸 **Low Frizz / Sleek Hair (e.g., 18% Frizz)**:
  - 🌧️ **Predicted Rain Density: 89%**
  - 🌊 **Flood Probability: 76%**
  - 🚨 **Weather Status: Flood Warning: Carry an Umbrella 😂**  
  *(Satirical lore: Zero friction detected! The slick aerodynamics of smooth hair create a low-pressure suction vortex that pulls storm clouds directly onto your head!)*

---

## 📱 Page Structure

1. **HEADER**:
   - `💇‍♀️ HAIR WEATHER PREDICTOR`
   - *"Your hair today. Our weather prediction tomorrow." 😂*
2. **SECTION 1: 📸 Upload Your Hair**
   - Modern drag-and-drop file uploader (supports JPG, PNG, WEBP).
   - Live stage webcam input support.
   - Quick Demo Samples (Ultra Sleek, Wavy, Wild Frizz) for instant live testing.
   - Displays the uploaded photo and real OpenCV Edge Detection Map in a clean glassmorphism card.
3. **SECTION 2: ✨ Hair Analysis**
   - Displays `💇‍♀️ Hair Frizziness: XX%` with a glowing animated progress meter.
4. **SECTION 3: 🌧️ Weather Prediction**
   - Two modern glassmorphism cards side-by-side:
     - `🌧️ Predicted Rain Density: XX%`
     - `🌊 Flood Probability: XX%`
5. **SECTION 4: 🌤️ Weather Status**
   - Visually distinct cards:
     - `☀️ Probably Safe` (Glowing emerald safe glass card)
     - `🚨 Flood Warning: Carry an Umbrella 😂` (Glowing red/amber storm warning card with snow celebration)
6. **🔄 "Analyze Another Photo" Button**:
   - One-click button to reset and test another hair photo.

---

## 🛠️ Technology Used

- **Language:** Python 3.11+
- **Frontend / Framework:** Streamlit
- **Image Processing & Computer Vision:** OpenCV (`opencv-python-headless`), Pillow, NumPy
- **Styling:** Custom CSS (Modern glassmorphism, responsive grid, soft shadows, rounded corners, gradient typography)

---

## 🚀 How to Run

### Quick 1-Click Launch (Windows)
Double-click **`run_app.bat`** in the project folder.

### From PowerShell / Terminal
```powershell
# 1. Activate the virtual environment
.\.venv\Scripts\Activate.ps1

# 2. Run the Streamlit web app
streamlit run app.py
```
Open your browser to: **`http://localhost:8501`**

---

## 🧪 Automated Verification
To run the automated verification test suite:
```powershell
.\.venv\Scripts\python.exe test_app.py
```
This tests OpenCV edge detection and mathematically verifies that:
- 82% Frizz $\rightarrow$ 23% Rain Density $\rightarrow$ 8% Flood Probability $\rightarrow$ Probably Safe
- 18% Frizz $\rightarrow$ 89% Rain Density $\rightarrow$ 76% Flood Probability $\rightarrow$ Flood Warning
