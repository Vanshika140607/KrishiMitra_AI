import speech_recognition as sr
import tempfile


# -----------------------------------------
# LANGUAGE CODES
# -----------------------------------------

LANGUAGE_CODES = {
    "English": "en-IN",
    "Hindi": "hi-IN",
    "Marathi": "mr-IN"
}


# -----------------------------------------
# SPEECH TO TEXT
# -----------------------------------------

def speech_to_text(audio_file, language):

    """
    Convert recorded browser audio into text.

    audio_file:
        Audio recorded using Streamlit st.audio_input()

    language:
        English, Hindi, or Marathi
    """

    # -----------------------------------------
    # CREATE SPEECH RECOGNIZER
    # -----------------------------------------

    recognizer = sr.Recognizer()


    # -----------------------------------------
    # GET LANGUAGE CODE
    # -----------------------------------------

    language_code = LANGUAGE_CODES[language]


    # -----------------------------------------
    # SAVE STREAMLIT AUDIO TO TEMP FILE
    # -----------------------------------------

    with tempfile.NamedTemporaryFile(
        suffix=".wav",
        delete=False
    ) as temp_audio:

        temp_audio.write(
            audio_file.getvalue()
        )

        temp_audio_path = temp_audio.name


    # -----------------------------------------
    # READ AUDIO FILE
    # -----------------------------------------

    try:

        with sr.AudioFile(temp_audio_path) as source:

            audio_data = recognizer.record(
                source
            )


        # -----------------------------------------
        # CONVERT SPEECH TO TEXT
        # -----------------------------------------

        text = recognizer.recognize_google(
            audio_data,
            language=language_code
        )


        return text


    # -----------------------------------------
    # SPEECH NOT UNDERSTOOD
    # -----------------------------------------

    except sr.UnknownValueError:

        return None


    # -----------------------------------------
    # SPEECH SERVICE ERROR
    # -----------------------------------------

    except sr.RequestError as e:

        raise Exception(
            f"Speech recognition service error: {e}"
        )


# -----------------------------------------
# TEST
# -----------------------------------------

if __name__ == "__main__":

    print("\n========================================")
    print("🎤 MULTILINGUAL SPEECH TEST")
    print("========================================")

    print("\nSupported languages:")

    for language in LANGUAGE_CODES:

        print(
            f"{language} → "
            f"{LANGUAGE_CODES[language]}"
        )
