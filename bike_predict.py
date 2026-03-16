import streamlit as st
import pandas as pd
import pickle
import os

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

# HEADER
st.title("🚲 Bike Rental Demand Prediction")
st.write("Real-time prediction based on weather & time conditions.")
st.divider()

# LOAD MODEL DENGAN ERROR HANDLING
@st.cache_resource
def load_artifact():
    model_path = "XGB_Tuned.sav"
    
    # Cek apakah file ada
    if not os.path.exists(model_path):
        st.error(f"❌ File model '{model_path}' tidak ditemukan!")
        st.write("📁 **File yang ada di direktori:**")
        files = os.listdir('.')
        for f in files:
            # Tampilkan ukuran file untuk .sav
            if f.endswith('.sav'):
                size = os.path.getsize(f) / (1024*1024)  # Convert ke MB
                st.write(f"- {f} ({size:.2f} MB)")
            else:
                st.write(f"- {f}")
        return None
    
    # Load file
    try:
        with open(model_path, "rb") as f:
            artifact = pickle.load(f)
        st.success("✅ Model berhasil diload!")
        return artifact
    except Exception as e:
        st.error(f"❌ Error loading model: {str(e)}")
        return None

# Load artifact
artifact = load_artifact()

# Hentikan jika model gagal load
if artifact is None:
    st.stop()

# Ekstrak model dan thresholds dengan validasi
try:
    # Cek apakah artifact berbentuk dictionary
    if isinstance(artifact, dict):
        model = artifact.get("model")
        low_th = artifact.get("low_threshold", 200)
        high_th = artifact.get("high_threshold", 450)
        upper_bound = artifact.get("upper_bound", 800)
        
        # Tampilkan info model (bisa di-expand)
        with st.expander("📊 Info Model"):
            st.write("**Tipe Model:**", type(model).__name__)
            st.write("**Threshold Values:**")
            st.write(f"- Low Threshold (Q1): {low_th:.2f}")
            st.write(f"- High Threshold (Q3): {high_th:.2f}")
            st.write(f"- Upper Bound: {upper_bound:.2f}")
    else:
        # Jika model langsung (bukan dictionary)
        model = artifact
        # Threshold default (sesuaikan dengan data Anda)
        low_th = 200
        high_th = 450
        upper_bound = 800
        st.info("ℹ️ Menggunakan threshold default karena model tidak menyertakan threshold values")
        
except Exception as e:
    st.error(f"❌ Error extracting model: {str(e)}")
    st.stop()

# INPUT SECTION
col1, col2 = st.columns(2)

with col1:
    day_mapping = {
        "Sunday": 0, "Monday": 1, "Tuesday": 2,
        "Wednesday": 3, "Thursday": 4,
        "Friday": 5, "Saturday": 6
    }
    day_label = st.selectbox("📅 Day of Week", list(day_mapping.keys()))
    day_of_week = day_mapping[day_label]

    season_mapping = {
        "Spring": 1, "Summer": 2,
        "Fall": 3, "Winter": 4
    }
    season_label = st.selectbox("🍂 Season", list(season_mapping.keys()))
    season = season_mapping[season_label]

    holiday_label = st.selectbox("🏖️ Holiday", ["No", "Yes"])
    holiday = 1 if holiday_label == "Yes" else 0

with col2:
    temp = st.slider("🌡️ Temperature", 0.0, 1.0, 0.5, 0.01)
    hum = st.slider("🌫️ Humidity", 0.0, 1.0, 0.5, 0.01)
    hr = st.slider("🕗 Hour", 0, 23, 12)

    weather_mapping = {
        "Clear / Few Clouds": 1,
        "Mist / Cloudy": 2,
        "Light Snow / Rain": 3,
        "Heavy Rain / Snow": 4
    }
    weather_label = st.selectbox("🌞 Weather Situation", list(weather_mapping.keys()))
    weathersit = weather_mapping[weather_label]

# Tombol prediksi
if st.button("🔮 Prediksi Demand", type="primary", use_container_width=True):
    with st.spinner("Menghitung prediksi..."):
        try:
            # Buat dataframe input
            input_data = pd.DataFrame([{
                "hr": hr,
                "temp": temp,
                "day_of_week": day_of_week,
                "hum": hum,
                "season": season,
                "weathersit": weathersit,
                "holiday": holiday
            }])
            
            # Prediksi
            prediction = model.predict(input_data)[0]
            prediction = max(0, int(round(prediction)))
            
            # Kategorisasi
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
            
            # Tampilkan hasil
            st.markdown(f"""
            <div class="result-card {css_class}">
                <div class="metric-label">Predicted Rentals</div>
                <div class="metric-value">{prediction}</div>
                <br>
                <div class="metric-label">Demand Category</div>
                <div class="metric-value">{category}</div>
            </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"❌ Error dalam prediksi: {str(e)}")

# Footer
st.divider()
st.caption("⚠️ Note: Demand categories are calibrated on 2011–2012 data and may not fully reflect current demand patterns.")
