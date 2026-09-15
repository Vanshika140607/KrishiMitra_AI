import os
import re
from pathlib import Path

import streamlit as st
from PIL import Image, ImageOps

from utils.speech_to_text import speech_to_text
from rag.answer_generator import generate_answer


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="KrishiMitra AI",
    page_icon="🌾",
    layout="centered"
)


# ============================================================
# SESSION STATE
# ============================================================

if "voice_question" not in st.session_state:
    st.session_state.voice_question = None

if "answer" not in st.session_state:
    st.session_state.answer = None

if "last_question" not in st.session_state:
    st.session_state.last_question = None


# ============================================================
# IMAGE PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

HERO_IMAGE_PATH = (
    BASE_DIR / "assets" / "agriculture_hero.png"
)


# ============================================================
# CREATE WIDE HERO IMAGE
# ============================================================

def create_hero_banner(image_path):

    image = Image.open(image_path).convert("RGB")

    # Wide and short banner
    banner_width = 1400
    banner_height = 380

    # Crop the image without distortion
    image = ImageOps.fit(
        image,
        (banner_width, banner_height),
        method=Image.Resampling.LANCZOS,
        centering=(0.50, 0.40)
    )

    return image


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
<style>

    /* ----------------------------------------------------
       APPLICATION BACKGROUND
       ---------------------------------------------------- */

    .stApp {
        background-color: #f5f9f3;
    }


    /* ----------------------------------------------------
       MAIN CONTAINER
       ---------------------------------------------------- */

    .main .block-container {
        max-width: 900px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }


    /* ----------------------------------------------------
       SECTION HEADINGS
       ---------------------------------------------------- */

    h2 {
        color: #1b5e20 !important;
        font-size: 22px !important;
        font-weight: 750 !important;
    }


    /* ----------------------------------------------------
       TEXT INPUT
       ---------------------------------------------------- */

    div[data-testid="stTextInput"] input {

        border-radius: 12px;

        border: 1px solid #c9d9c7;

        min-height: 48px;

        font-size: 15px;
    }

    div[data-testid="stTextInput"] input:focus {

        border-color: #2e7d32;

        box-shadow:
            0 0 0 1px #2e7d32;
    }


    /* ----------------------------------------------------
       SELECT BOX
       ---------------------------------------------------- */

    div[data-baseweb="select"] > div {

        border-radius: 12px;

        border: 1px solid #c9d9c7;
    }


    /* ----------------------------------------------------
       PRIMARY BUTTON
       ---------------------------------------------------- */

    button[kind="primary"] {

        background-color: #2e7d32 !important;

        color: white !important;

        border: none !important;

        border-radius: 12px !important;

        min-height: 50px !important;

        font-size: 16px !important;

        font-weight: 700 !important;
    }


    button[kind="primary"]:hover {

        background-color: #1b5e20 !important;

        color: white !important;
    }


    /* ----------------------------------------------------
       AUDIO INPUT
       ---------------------------------------------------- */

    div[data-testid="stAudioInput"] {
        border-radius: 14px;
    }


    /* ----------------------------------------------------
       HERO IMAGE
       ---------------------------------------------------- */

    div[data-testid="stImage"] img {

        border-radius: 18px;

        width: 100%;

        box-shadow:
            0 8px 25px rgba(27, 94, 32, 0.15);
    }


    /* ----------------------------------------------------
       FOOTER
       ---------------------------------------------------- */

    .footer-text {

        text-align: center;

        color: #7a857b;

        font-size: 13px;

        margin-top: 35px;
    }

</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# HERO IMAGE
# ============================================================

if HERO_IMAGE_PATH.exists():

    hero_banner = create_hero_banner(
        HERO_IMAGE_PATH
    )

    st.image(
        hero_banner,
        use_container_width=True
    )

else:

    st.error(
        "❌ Agriculture hero image not found."
    )

    st.code(
        str(HERO_IMAGE_PATH)
    )


# ============================================================
# SMART AGRICULTURAL GUIDANCE
# ============================================================

with st.container(border=True):

    st.markdown(
        "### 🌱 Smart Agricultural Guidance"
    )

    st.write(
        "Ask agriculture-related questions in English, "
        "Hindi, or Marathi. You can type your question "
        "or use the microphone."
    )


# ============================================================
# LANGUAGE SELECTION
# ============================================================

st.markdown(
    "## 🌐 Choose Your Language"
)

st.caption(
    "Select the language in which you want to ask your "
    "question and receive the answer."
)

language = st.selectbox(
    "Language",
    [
        "English",
        "Hindi",
        "Marathi"
    ],
    label_visibility="collapsed"
)


# ============================================================
# QUESTION PLACEHOLDERS
# ============================================================

PLACEHOLDERS = {

    "English":
        "Example: What are the recommendations for rice cultivation in Maharashtra?",

    "Hindi":
        "उदाहरण: महाराष्ट्र में धान की खेती के लिए क्या सिफारिशें हैं?",

    "Marathi":
        "उदाहरण: महाराष्ट्रात भात लागवडीसाठी काय शिफारशी आहेत?"
}


# ============================================================
# ASK QUESTION USING TEXT
# ============================================================

st.markdown(
    "## ⌨️ Ask Your Question"
)

st.caption(
    "Type your agriculture-related question below."
)

typed_question = st.text_input(
    "Agriculture Question",
    placeholder=PLACEHOLDERS[language],
    label_visibility="collapsed"
)


# ============================================================
# ASK QUESTION USING VOICE
# ============================================================

st.markdown(
    "## 🎤 Ask Using Your Voice"
)

st.caption(
    f"Record your question in {language}."
)

audio_value = st.audio_input(
    "Record your agriculture question",
    sample_rate=16000,
    label_visibility="collapsed"
)


# ============================================================
# SPEECH TO TEXT
# ============================================================

if audio_value is not None:

    with st.spinner(
        f"🎙️ Converting your {language} speech to text..."
    ):

        try:

            voice_question = speech_to_text(
                audio_value,
                language
            )

            st.session_state.voice_question = (
                voice_question
            )

        except Exception as e:

            st.error(
                f"Speech recognition error: {e}"
            )

            st.session_state.voice_question = None


# ============================================================
# SHOW VOICE QUESTION
# ============================================================

if st.session_state.voice_question:

    st.success(
        "🎤 Your question: "
        + st.session_state.voice_question
    )


# ============================================================
# EXAMPLE QUESTIONS
# ============================================================

st.markdown(
    "## 💡 Example Questions"
)

with st.container(border=True):

    st.write(
        "🌾 What are the recommendations for rice cultivation?"
    )

    st.write(
        "🌱 Which fertilizer is recommended for crops?"
    )

    st.write(
        "🐛 How can farmers manage crop pests?"
    )


st.write("")


# ============================================================
# GET AGRICULTURE ANSWER
# ============================================================

if st.button(
    "🌾 Get Agriculture Answer",
    type="primary",
    use_container_width=True
):

    # --------------------------------------------------------
    # Select question
    # --------------------------------------------------------

    if st.session_state.voice_question:

        final_question = (
            st.session_state.voice_question
        )

    elif typed_question.strip():

        final_question = (
            typed_question.strip()
        )

    else:

        final_question = None


    # --------------------------------------------------------
    # Check question
    # --------------------------------------------------------

    if not final_question:

        st.warning(
            "Please type a question or record your "
            "question using the microphone."
        )


    # --------------------------------------------------------
    # Generate answer
    # --------------------------------------------------------

    else:

        with st.spinner(
            "🔍 Searching agricultural knowledge..."
        ):

            try:

                answer = generate_answer(
                    final_question,
                    language
                )


                # Remove unwanted SVG artifact
                answer = re.sub(
                    r"\[svg\]\(http://localhost:[^)]+\)",
                    "",
                    answer,
                    flags=re.IGNORECASE
                )


                # Store answer
                st.session_state.answer = answer

                st.session_state.last_question = (
                    final_question
                )


            except Exception as e:

                st.error(
                    "Something went wrong while generating "
                    "the agriculture answer."
                )

                st.exception(e)


# ============================================================
# DISPLAY ANSWER
# ============================================================

if st.session_state.answer:

    st.markdown(
        "## 🌱 Agriculture Assistant"
    )

    with st.container(border=True):

        st.markdown(
            st.session_state.answer
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "🌾 KrishiMitra AI • AI-powered agricultural "
    "knowledge assistant"
)

st.caption(
    "Helping farmers access agricultural information "
    "more easily."
)