import streamlit as st
import numpy as np
import joblib
import pandas as pd

# Load model files
model = joblib.load("model/sleep_model.pkl")
scaler = joblib.load("model/scaler.pkl")
le_bmi = joblib.load("model/le_bmi.pkl")
le_target = joblib.load("model/le_target.pkl")

st.set_page_config(page_title="Sleep Quality Predictor", page_icon="🌙")

# Custom CSS for styling
st.markdown("""
<style>
    :root { color-scheme: light; }
    [data-testid="stAppViewContainer"] { background-color: #f7fcff !important; color: #1f1f1f !important; }
    [data-testid="stToolbar"], [data-testid="stHeader"] { background-color: #ffffff !important; }
    [data-testid="stSidebar"] { background: linear-gradient(180deg, #dff6ff 0%, #eaf9ff 100%) !important; color: #0f4c81 !important; }
    h1, h2, h3, h4, h5, h6 { color: #0b4f77 !important; font-weight: 800 !important; }
    .css-1d391kg, .css-1k81p5n, .css-1y4p8pa { background-color: #ffffff !important; border: 1px solid #a1d4fa !important; box-shadow: 0 4px 20px rgba(0,0,0,.05) !important; }
    input, select, textarea { background-color: #ffffff !important; color: #111827 !important; border: 1px solid #0c6dc7 !important; }
    .stSlider>div>div>div { background: linear-gradient(90deg, #ff4d4d, #2d9cdb) !important; }
    button[kind="primary"], .stButton>button { background-color: #0a84ff !important; color: #ffffff !important; border-radius: 12px !important; font-size: 16px !important; padding: 10px 20px !important; border: 0 !important; }
    button[kind="primary"]:hover, .stButton>button:hover { background-color: #0066cc !important; }
    .stAlert { border-left: 6px solid #0077cc !important; }
</style>
""", unsafe_allow_html=True)

# Add gradient section header with emojis
st.markdown("""
<div style='padding: 0.8rem 1rem; border-radius: 14px; background: linear-gradient(135deg, #7ed6ff 0%, #1e90ff 100%); margin-bottom: 1rem;'>
  <h1 style='margin: 0; color: white; text-shadow: 0 2px 10px rgba(0,0,0,0.2);'>🌙 Sleep Quality Predictor</h1>
  <p style='margin: 0.2rem 0 0; color: #dbeeff; font-size:1.1rem;'>A smart, full-color dashboard to monitor and improve your sleep</p>
</div>
""", unsafe_allow_html=True)


st.title("🌙 Sleep Quality Predictor")
st.markdown("### A smart way to monitor and improve your sleep")

# --- INPUTS ---
st.write("#### Sleep Duration (hours)")
sleep = st.number_input("", 1.0, 12.0, 7.0, format="%.2f", help="Enter your average hours of sleep per night (1.0–12.0)")

st.write("#### Physical Activity (mins/day)")
activity = st.number_input("", 0, 120, 30, help="Enter your daily active minutes (0–120)")

st.write("#### Stress Level")
stress = st.slider("", 0, 10, 5, help="0 = Very low stress, 10 = Very high stress")

st.write("#### Heart Rate (bpm)")
heart = st.number_input("", 50, 110, 70, help="Enter your resting heart rate in beats per minute (50–110)")

st.write("#### Daily Steps")
steps = st.number_input("", 0, 20000, 7000, help="Enter approximate steps per day")

st.write("#### BMI Category")
bmi = st.selectbox("", ["Normal", "Normal Weight", "Obese", "Overweight"], help="Select the BMI category that fits you")

# --- PREDICT BUTTON ---
if st.button("🔍 Predict Sleep Quality"):
    try:
        bmi_encoded = le_bmi.transform([bmi])[0]

        features = ["Sleep Duration", "Physical Activity Level", "Stress Level", "Heart Rate", "Daily Steps", "BMI Category"]
        features_df = pd.DataFrame([[sleep, activity, stress, heart, steps, bmi_encoded]], columns=features)

        features_scaled = scaler.transform(features_df)

        pred = model.predict(features_scaled)[0]
        label = le_target.inverse_transform([pred])[0]

        # --- FINAL LOGIC (ALL INPUTS USED) ---
        if stress >= 8:
            label = "Poor"

        elif bmi == "Obese":
            label = "Poor"

        elif activity < 20 and sleep < 6:
            label = "Poor"

        elif sleep >= 7 and stress <= 4:
            label = "Good"

        else:
            label = "Average"

        # Display result with colors
        if label == "Good":
            st.success(f"🌟 Your predicted sleep quality is: **{label}**")
            st.markdown("Great job! Keep up the healthy habits.")
        elif label == "Average":
            st.warning(f"⚠️ Your predicted sleep quality is: **{label}**")
            st.markdown("Consider improving your sleep routine.")
        else:
            st.error(f"😴 Your predicted sleep quality is: **{label}**")
            st.markdown("Time to focus on better sleep habits!")
    except Exception as e:
        st.error(f"An error occurred during prediction: {str(e)}")
        st.markdown("Please check your inputs or try again.")

    # --- DISPLAY RESULT ---
    color = {"Good": "🟢", "Average": "🟡", "Poor": "🔴"}[label]
    st.subheader(f"Predicted Sleep Quality: {color} {label}")

    # --- SMART SUGGESTIONS ---
    st.markdown("### 💡 Personalized Suggestions")

    # Sleep
    if sleep < 6:
        st.write("😴 Increase your sleep duration to at least 7 hours")
    elif sleep > 9:
        st.write("⏰ Too much sleep may reduce efficiency, maintain 7–9 hours")

    # Stress
    if stress >= 8:
        st.write("🧘 High stress detected! Try meditation or deep breathing")
    elif stress >= 5:
        st.write("📉 Moderate stress — consider relaxation techniques")

    # Activity
    if activity < 20:
        st.write("🏃 Increase physical activity for better sleep")
    elif activity > 60:
        st.write("💪 Great activity level! Keep it up")

    # BMI
    if bmi == "Obese":
        st.write("⚖️ High BMI can affect sleep — focus on healthy diet & exercise")
    elif bmi == "Overweight":
        st.write("📊 Try maintaining a balanced lifestyle to improve sleep")

    # Steps
    if steps < 5000:
        st.write("🚶 Increase daily steps for better health and sleep")

    # Heart Rate
    if heart > 90:
        st.write("❤️ High heart rate — consider relaxation and health check")

    # Combined warnings
    if stress >= 8 and sleep < 6:
        st.write("⚠️ High stress + low sleep → major impact on sleep")

    if activity < 20 and steps < 4000:
        st.write("⚠️ Low activity lifestyle affecting sleep quality")

    # Final feedback
    if label == "Good":
        st.success("✅ Your lifestyle is supporting good sleep!")
    elif label == "Average":
        st.info("📈 Small improvements can make your sleep better")
    else:
        st.error("⚠️ Focus on improving your lifestyle habits!")