import streamlit as st
import pandas as pd
import pickle
from sklearn.preprocessing import LabelEncoder
import time
import base64

# Page configuration
st.set_page_config(
    page_title="Insight",
    page_icon=r"C:\Users\hp\OneDrive\Desktop\movie_info_project\app\CLAP.avif",  # Using an emoji for cross-platform compatibility
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Function to encode image to Base64
def get_base64_image(image_path):
    """Encodes a local image file to a Base64 string."""
    try:
        with open(image_path, "rb") as img_file:
            b64_string = base64.b64encode(img_file.read()).decode()
        return b64_string
    except FileNotFoundError:
        st.error(f"Error: The image file was not found at {image_path}. Please check the file path.")
        return None

# Path to the background image
# NOTE: The path is now passed to the function, and the function handles the file opening.
background_image_path = r"C:\Users\hp\OneDrive\Desktop\movie_info_project\app\movie_template.jpg"
b64_string = get_base64_image(background_image_path)

# Custom CSS with background image and liquid design
if b64_string:
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

        .stApp {{
            background-image: url("data:image/jpg;base64,{b64_string}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            background-repeat: no-repeat;
        }}
        .stApp::before {{
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.85) 0%, rgba(118, 75, 162, 0.85) 100%);
            z-index: -1;
            pointer-events: none;
        }}
        .main {{
            font-family: 'Poppins', sans-serif;
            min-height: 100vh;
            position: relative;
        }}
        .main-header {{
            background: linear-gradient(45deg, rgba(102, 126, 234, 0.95), rgba(118, 75, 162, 0.95));
            backdrop-filter: blur(10px);
            padding: 2rem;
            border-radius: 25px;
            margin-bottom: 2rem;
            box-shadow: 0 15px 35px rgba(0,0,0,0.3), 0 5px 15px rgba(0,0,0,0.2);
            border: 1px solid rgba(255, 255, 255, 0.2);
            animation: slideDown 0.8s ease-out;
        }}
        .main-header h1 {{
            color: white;
            font-size: 3rem;
            font-weight: 700;
            text-align: center;
            margin: 0;
            text-shadow: 3px 3px 6px rgba(0,0,0,0.4);
            background: linear-gradient(45deg, #ffffff, #e2e8f0);
            background-clip: text;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .main-header p {{
            color: rgba(255,255,255,0.95);
            font-size: 1.2rem;
            text-align: center;
            margin: 0.5rem 0 0 0;
            font-weight: 300;
            text-shadow: 1px 1px 3px rgba(0,0,0,0.3);
        }}
        .liquid-column {{
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
            backdrop-filter: blur(15px);
            border-radius: 20px;
            padding: 1.5rem;
            margin: 0.5rem;
            border: 1px solid rgba(255, 255, 255, 0.2);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
            animation: liquidFloat 6s ease-in-out infinite;
        }}
        .liquid-column:hover {{
            transform: translateY(-5px);
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.15), rgba(255, 255, 255, 0.08));
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
        }}
        .liquid-column:nth-child(odd) {{
            animation-delay: -3s;
        }}
        @keyframes liquidFloat {{
            0%, 100% {{ transform: translateY(0px) rotate(0deg); }}
            25% {{ transform: translateY(-10px) rotate(1deg); }}
            50% {{ transform: translateY(5px) rotate(0deg); }}
            75% {{ transform: translateY(-5px) rotate(-1deg); }}
        }}
        .movie-details {{
            background: linear-gradient(45deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 1.5rem;
            margin: 1rem 0;
            border: 1px solid rgba(255, 255, 255, 0.3);
            animation: shimmer 3s ease-in-out infinite;
        }}
        @keyframes shimmer {{
            0%, 100% {{ background-position: -200% center; }}
            50% {{ background-position: 200% center; }}
        }}
        .stButton > button {{
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            border: none;
            border-radius: 25px;
            padding: 0.75rem 2rem;
            font-size: 1.1rem;
            font-weight: 600;
            transition: all 0.4s ease;
            box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
            width: 100%;
            position: relative;
            overflow: hidden;
        }}
        .stButton > button:before {{
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            transition: left 0.5s ease;
        }}
        .stButton > button:hover:before {{
            left: 100%;
        }}
        .stButton > button:hover {{
            background: linear-gradient(45deg, #5a67d8, #6b46c1);
            transform: translateY(-3px) scale(1.02);
            box-shadow: 0 12px 30px rgba(102, 126, 234, 0.6);
        }}
        .prediction-box {{
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.95), rgba(118, 75, 162, 0.95));
            backdrop-filter: blur(20px);
            color: white;
            padding: 2rem;
            border-radius: 20px;
            text-align: center;
            border: 2px solid rgba(255, 255, 255, 0.3);
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
            animation: bounceIn 0.8s ease-out, pulse 2s infinite;
            position: relative;
            overflow: hidden;
        }}
        .prediction-box::before {{
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: conic-gradient(from 0deg, transparent, rgba(255,255,255,0.1), transparent);
            animation: rotate 4s linear infinite;
        }}
        .prediction-box h3 {{
            position: relative;
            z-index: 1;
            margin: 0;
        }}
        @keyframes rotate {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
        @keyframes slideDown {{
            from {{ transform: translateY(-100px); opacity: 0; }}
            to {{ transform: translateY(0); opacity: 1; }}
        }}
        @keyframes bounceIn {{
            0% {{ transform: scale(0.3); opacity: 0; }}
            50% {{ transform: scale(1.05); }}
            70% {{ transform: scale(0.9); }}
            100% {{ transform: scale(1); opacity: 1; }}
        }}
        @keyframes pulse {{
            0%, 100% {{ box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2); }}
            50% {{ box-shadow: 0 15px 35px rgba(102, 126, 234, 0.4); }}
        }}
        .stMarkdown, .stText, p, span {{
            color: #ffffff !important;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
            font-weight: 500;
        }}
        .stSelectbox > div > div > div {{
            background: rgba(0, 0, 0, 0.9) !important;
            backdrop-filter: blur(10px);
            border-radius: 10px;
            border: 1px solid rgba(255, 255, 255, 0.3);
        }}
        .stApp > div > div > div > div > h2 {{
            color: white !important;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
            background: linear-gradient(45deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
            backdrop-filter: blur(10px);
            padding: 1rem;
            border-radius: 15px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            margin: 1rem 0;
        }}
        .footer {{
            background: linear-gradient(45deg, rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 0.1));
            backdrop-filter: blur(10px);
            border-radius: 15px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            margin-top: 2rem;
        }}
    </style>
    """, unsafe_allow_html=True)

# Load model and data
@st.cache_resource
def load_model_and_data():
    try:
        with open(r'C:\Users\hp\OneDrive\Desktop\movie_info_project\app\model.pkl', 'rb') as file:
            model = pickle.load(file)
        
        df = pd.read_csv(r'C:\Users\hp\OneDrive\Desktop\movie_info_project\data\movies_cleaned.csv')
        
        encoders = {}
        for col in ["genre", "director", "writer", "star"]:
            le = LabelEncoder()
            df[col + '_encoded'] = le.fit_transform(df[col].astype(str))
            encoders[col] = le
            
        return model, df, encoders
    except Exception as e:
        st.error(f"Error loading model or data: {str(e)}")
        return None, None, None

# Main header
st.markdown("""
<div class="main-header">
    <h1>MOVIE RATING PREDICTOR</h1>
    <p>Advanced Movie Rating Prediction System</p>
</div>
""", unsafe_allow_html=True)

# Load resources
model, df, encoders = load_model_and_data()
if model is None or df is None:
    st.stop()

# Movie Prediction Interface
st.subheader("Search Existing Movie")
movie_names = df['name'].unique()
selected_movie = st.selectbox(
    "Select a movie from dataset",
    [""] + list(movie_names),
    key="movie_select"
)

if st.button("Predict Rating", key="predict_existing"):
    if selected_movie:
        with st.spinner("Analyzing movie..."):
            time.sleep(1)
            movie_data = df[df['name'] == selected_movie].iloc[0]
            
            features = [[
                movie_data['genre_encoded'],
                movie_data['director_encoded'],
                movie_data['writer_encoded'],
                movie_data['star_encoded'],
                movie_data['year']
            ]]
            
            prediction = model.predict(features)[0]
            
            st.markdown(f"<h2 style='color: white; text-align: center;'>Movie: {selected_movie}</h2>", unsafe_allow_html=True)
            
            # Liquid design columns
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown(f"""
                <div class="liquid-column">
                    <p><strong>Genre:</strong> {movie_data['genre']}</p>
                    <p><strong>Director:</strong> {movie_data['director']}</p>
                    <p><strong>Year:</strong> {movie_data['year']}</p>
                </div>
                """, unsafe_allow_html=True)
                
            with col_b:
                st.markdown(f"""
                <div class="liquid-column">
                    <p><strong>Writer:</strong> {movie_data['writer']}</p>
                    <p><strong>Star:</strong> {movie_data['star']}</p>
                    <p><strong>Actual Rating:</strong> {movie_data.get('rating', 'N/A')}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Prediction result with enhanced animation
            st.markdown(f"""
            <div class="prediction-box">
                <h3>Predicted Rating Category: {prediction}</h3>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("Please select a movie first.")

# Enhanced Footer
st.markdown("""
<div class="footer" style="text-align: center; padding: 2rem; color: rgba(255,255,255,0.9);">
    <p>INSIGHT - Powered by Machine Learning | Built with Streamlit BY SHIBIL </p>
</div>
""", unsafe_allow_html=True)
