import streamlit as st
import pandas as pd
import pickle


# PAGE CONFIG
st.set_page_config(
    page_title="Bike Demand Prediction",
    page_icon="🚲",
    layout="centered"
)


# CUSTOM CSS
st.markdown("""
<style>

/* Main Background */
.stApp {
    background-color: #EDDCC6;
}

/* Title */
h1 {
    color: #BF4646;
}

/* Paragraph */
p {
    color: #5A4A42;
}

/* Result Card Base */
.result-card {
    padding: 25px;
    border-radius: 16px;
    text-align: center;
    box-shadow: 0 6px 18px rgba(0,0,0,0.08);
    margin-top: 20px;
    transition: 0.3s ease;
}

/* LOW */
.low {
    background-color: #FFF4EA;
    color: #5A4A42;
}

/* MEDIUM */
.medium {
    background-color: #7EACB5;
    color: white;
}

/* HIGH */
.high {
    background-color: #BF4646;
    color: white;
}

/* VERY HIGH */
.vhigh {
    background-color: #8E2F2F;
    color: white;
}

/* Metric Styling */
.metric-label {
    font-size: 14px;
    opacity: 0.85;
}

.metric-value {
    font-size: 34px;
    font-weight: 700;
}

</style>
""", unsafe_allow_html=True)


# LOAD MODEL
@st.cache_resource
def load_artifact():
    with open("XGB_Tuned.sav", "rb") as f:
        return pickle.load(f)

artifact = load_artifact()
model = artifact["model"]
low_th = artifact["low_threshold"]     # Q1
high_th = artifact["high_threshold"]   # Q3
upper_bound = artifact["upper_bound"]  # Q3 + 1.5*IQR


# HEADER
st.title("🚲 Bike Rental Demand Prediction")
st.write("Real-time prediction based on weather & time conditions.\n\n⚠️ **Note:** Demand categories (Low, Medium, High) are calibrated on 2011–2012 data and may not fully reflect current demand patterns.")
st.divider()


# INPUT SECTION
col1, col2 = st.columns(2)

with col1:
    day_mapping = {
        "Sunday": 0, "Monday": 1, "Tuesday": 2,
        "Wednesday": 3, "Thursday": 4,
        "Friday": 5, "Saturday": 6
    }
    day_label = st.selectbox("📅Day of Week", list(day_mapping.keys()))
    day_of_week = day_mapping[day_label]

    season_mapping = {
        "Spring": 1, "Summer": 2,
        "Fall": 3, "Winter": 4
    }
    season_label = st.selectbox("🍂Season", list(season_mapping.keys()))
    season = season_mapping[season_label]

    holiday_label = st.selectbox("🏖️Holiday", ["No", "Yes"])
    holiday = 1 if holiday_label == "Yes" else 0

with col2:
    temp = st.slider("🌡️Temperature", 0.0, 1.0, 0.5)
    hum = st.slider("🌫️Humidity", 0.0, 1.0, 0.5)
    hr = st.slider("🕗Hour", 0, 23, 12)

    weather_mapping = {
        "Clear / Few Clouds": 1,
        "Mist / Cloudy": 2,
        "Light Snow / Rain": 3,
        "Heavy Rain / Snow": 4
    }
    weather_label = st.selectbox("🌞Weather Situation", list(weather_mapping.keys()))
    weathersit = weather_mapping[weather_label]


# AUTO PREDICTION
input_data = pd.DataFrame([{
    "hr": hr,
    "temp": temp,
    "day_of_week": day_of_week,
    "hum": hum,
    "season": season,
    "weathersit": weathersit,
    "holiday": holiday
}])

prediction = model.predict(input_data)[0]
prediction = max(0, int(round(prediction)))


# CATEGORIZATION
if prediction <= low_th:
    category = "Low Demand"
    css_class = "low"
elif prediction <= high_th:
    category = "Medium Demand"
    css_class = "medium"
elif prediction <= upper_bound:
    category = "High Demand"
    css_class = "high"
else:
    category = "Very High Demand"
    css_class = "vhigh"


# RESULT DISPLAY
st.markdown(f"""
<div class="result-card {css_class}">
    <div class="metric-label">Predicted Rentals</div>
    <div class="metric-value">{prediction}</div>
    <br>
    <div class="metric-label">Demand Category</div>
    <div class="metric-value">{category}</div>
</div>
""", unsafe_allow_html=True)
