import os

from dotenv import load_dotenv
from google import genai


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY was not found in .env")


client = genai.Client(api_key=api_key)


def detect_language(audio_file):

    print("\n🔍 Detecting language from audio...")

    audio = client.files.upload(
        file=audio_file
    )

    prompt = """
Listen to the audio carefully.

Identify which ONE of these languages is being spoken:

1. English
2. Hindi
3. Marathi

Return ONLY one of these exact words:

English
Hindi
Marathi

Do not provide any explanation.
"""

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=[
            prompt,
            audio
        ]
    )

    language = response.text.strip()

    if language not in ["English", "Hindi", "Marathi"]:
        raise ValueError(
            f"Unexpected language detected: {language}"
        )

    return language