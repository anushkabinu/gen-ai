import streamlit as st
from gtts import gTTS
from io import BytesIO
import os
from dotenv import load_dotenv
from google import genai  # Correct Gemini SDK import

# -----------------------
# Load API Key from .env
# -----------------------
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    st.error("❌ GOOGLE_API_KEY not found! Add it in a .env file.")
    st.stop()

# Initialize Gemini client
client = genai.Client(api_key=API_KEY)

# -----------------------
# Streamlit Page Config
# -----------------------
st.set_page_config(page_title="🧚 AI Storytelling Dashboard", layout="wide")
st.markdown("""
<div style="background-color:#f0f8ff;padding:15px;border-radius:15px">
<h1 style="color:#ff69b4;text-align:center;">🧚 Multilingual AI Storytelling</h1>
<p style="color:#555;font-size:16px;text-align:center;">Generate magical stories with AI — choose theme, language, and audience!</p>
</div>
""", unsafe_allow_html=True)

# -----------------------
# Sidebar Inputs
# -----------------------
st.sidebar.header("📌 Story Preferences")
story_type = st.sidebar.selectbox(
    "Choose Story Type 📝",
    ["Adventure 🗺️", "Friendship 🤝", "Animals 🐾", "Moral 📚", "Magic ✨", "Custom Prompt 🖊️"]
)

language = st.sidebar.selectbox("Select Language 🌐", ["English", "Hindi", "Kannada", "Tamil", "Malayalam"])
audience = st.sidebar.radio("Audience 👨‍👩‍👧‍👦", ["Children", "Parents", "Teachers"])

with st.sidebar.expander("Custom Story Prompt ✍️"):
    custom_prompt = st.text_area("Write your own story idea here (optional)")

generate_button = st.sidebar.button("✨ Generate Story")

# -----------------------
# Language Mapping for gTTS
# -----------------------
lang_map = {
    "English": "en",
    "Hindi": "hi",
    "Kannada": "kn",
    "Tamil": "ta",
    "Malayalam": "ml"
}

# -----------------------
# Generate Story
# -----------------------
if generate_button:
    if story_type != "Custom Prompt 🖊️" and custom_prompt.strip() == "":
        prompt = f"Write a short {story_type.split()[0].lower()} story in {language} for {audience.lower()}."
    elif custom_prompt.strip() != "":
        prompt = custom_prompt
    else:
        st.warning("Please select a story type or enter a custom prompt!")
        st.stop()

    st.info("✨ Generating story... please wait!")

    try:
        # Gemini AI Story Generation
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt
        )
        story = response.text.strip()

        # Generate Audio using gTTS (Multilingual)
        tts = gTTS(story, lang=lang_map.get(language, "en"))
        audio_bytes = BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)

        # Layout
        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader("📖 Generated Story")
            st.write(story)
            st.download_button("💾 Download Story", data=story, file_name=f"{language}_story.txt")

        with col2:
            st.subheader("🔊 Audio Narration")
            st.audio(audio_bytes, format="audio/mp3")

        st.subheader("🎨 Story Illustration")
        st.image("https://via.placeholder.com/400x300.png?text=AI+Story+Illustration", caption="AI-generated illustration (placeholder)")

        st.success("🎉 Story generation complete!")

    except Exception as e:
        st.error(f"Error: {e}")
