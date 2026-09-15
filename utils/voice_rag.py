from utils.language_detection import detect_language
from rag.answer_generator import generate_answer


def process_voice_question(audio_file):

    print("\n==============================")
    print("🌾 AGRIRAG VOICE ASSISTANT")
    print("==============================")

    # --------------------------------
    # STEP 1: DETECT LANGUAGE
    # --------------------------------

    print("\n🔍 Detecting language...")

    language = detect_language(audio_file)

    print("🌐 Language:", language)

    # --------------------------------
    # STEP 2: SPEECH TO TEXT
    # --------------------------------

    import speech_recognition as sr

    recognizer = sr.Recognizer()

    if language == "English":
        language_code = "en-IN"

    elif language == "Hindi":
        language_code = "hi-IN"

    elif language == "Marathi":
        language_code = "mr-IN"

    else:
        raise ValueError("Unsupported language")

    print("\n📝 Converting speech to text...")

    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)

    question = recognizer.recognize_google(
        audio_data,
        language=language_code
    )

    print("\n==============================")
    print("🎤 QUESTION")
    print("==============================")

    print(question)

    # --------------------------------
    # STEP 3: RAG + GEMINI
    # --------------------------------

    print("\n🔎 Searching agricultural documents...")

    answer = generate_answer(
        question,
        language=language
    )

    # --------------------------------
    # STEP 4: RETURN RESULT
    # --------------------------------

    return {
        "language": language,
        "question": question,
        "answer": answer
    }