from collections import defaultdict
import streamlit as st
import google.generativeai as genai
from datetime import datetime

# Zodiac sign determination based on birthdate
def get_zodiac_sign(birthdate):
    month = birthdate.month
    day = birthdate.day
    if (month == 3 and day >= 21) or (month == 4 and day <= 19):
        return "Aries"
    elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
        return "Taurus"
    elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
        return "Gemini"
    elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
        return "Cancer"
    elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
        return "Leo"
    elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
        return "Virgo"
    elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
        return "Libra"
    elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
        return "Scorpio"
    elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
        return "Sagittarius"
    elif (month == 12 and day >= 22) or (month == 1 and day <= 19):
        return "Capricorn"
    elif (month == 1 and day >= 20) or (month == 2 and day <= 18):
        return "Aquarius"
    else:
        return "Pisces"

# Initialize session state
if 'horoscopes' not in st.session_state:
    st.session_state.horoscopes = []
if 'votes' not in st.session_state:
    st.session_state.votes = defaultdict(int)  # Default value for votes is 0

# Configure Google Gemini API (Move inside function to prevent context errors)
GOOGLE_API_KEY = "AIzaSyCvqJlGoqY8Va6oJuz9c-VvG1ivVVdRSaQ"

# Initialize Gemini Model
@st.cache_resource
def get_gemini_model():
    genai.configure(api_key=GOOGLE_API_KEY)
    return genai.GenerativeModel('gemini-1.5-pro')

model = get_gemini_model()

# Function to generate horoscope with zodiac sign
@st.cache_data
def generate_horoscope(name, birthdate, zodiac_sign):
    """Generate a personalized horoscope."""
    try:
        # Create a personalized prompt using the user's name, birthdate, and zodiac sign
        prompt = f"""
        Create a short, mystical horoscope (2-3 sentences) for {name}, born on {birthdate}. 
        Their zodiac sign is {zodiac_sign}. 
        The horoscope should provide guidance, fortune, or insight and reflect astrological wisdom. 
        - The tone should be positive and reflective.
        - It should connect with themes like fate, future, or personal growth.
        - Suitable for general audiences.
        
        Example:
        "The stars align in your favor today, offering you a chance to find clarity in your decisions. Take the time to reflect, and the answers will come to you."
        
        Make it insightful, positive, and mystical.
        """
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error generating horoscope: {str(e)}"

# Function to add horoscope to session state
def add_horoscope(horoscope_text):
    st.session_state.horoscopes.append({
        'horoscope': horoscope_text,
        'votes': 0,
        'timestamp': datetime.now().isoformat()
    })

# UI Header
st.title("🔮 Horoscope Generator")
st.write("Get your personalized daily horoscope! Enter your name and birthdate to discover what the stars have in store for you.")

# Take user input for name and birthdate
name = st.text_input("Enter your name")
birthdate = st.date_input("Enter your birthdate")

# Determine zodiac sign
if birthdate:
    zodiac_sign = get_zodiac_sign(birthdate)
    st.write(f"Your Zodiac Sign: {zodiac_sign}")

# Button to generate horoscope
if st.button("Generate Horoscope"):
    if name and birthdate:
        with st.spinner("Crafting your personalized horoscope..."):
            horoscope = generate_horoscope(name, birthdate, zodiac_sign)
            add_horoscope(horoscope)
    else:
        st.warning("Please provide both your name and birthdate.")

# Display generated horoscopes
st.subheader("Your Horoscopes")
if st.session_state.horoscopes:
    sorted_horoscopes = sorted(st.session_state.horoscopes, key=lambda x: (-x['votes'], x['timestamp']))

    for idx, horoscope in enumerate(sorted_horoscopes):
        with st.container():
            st.write(f"Horoscope: {horoscope['horoscope']}")
            col1, col2 = st.columns([1, 8])
            with col1:
                if st.button("⬆ Upvote", key=f"vote_{idx}"):
                    st.session_state.votes[idx] += 1  # Increment vote count for the horoscope
            with col2:
                st.write(f"Votes: {st.session_state.votes[idx]}")  # Display the vote count
            st.markdown("---")
else:
    st.write("No horoscopes generated yet! Be the first to generate one.")
