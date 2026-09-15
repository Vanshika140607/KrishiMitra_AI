import sounddevice as sd
import soundfile as sf

from utils.voice_rag import process_voice_question


# ==============================
# SETTINGS
# ==============================

SAMPLE_RATE = 16000
RECORD_SECONDS = 7

AUDIO_FILE = "utils/recording.wav"


# ==============================
# RECORD VOICE
# ==============================

print("\n========================================")
print("🌾 AGRIRAG VOICE ASSISTANT")
print("========================================")

print("\n🎤 Get ready...")
print(f"Speak your agriculture question for {RECORD_SECONDS} seconds.")

input("\nPress ENTER when you are ready to start recording...")

print("\n🔴 Recording... SPEAK NOW!")

audio = sd.rec(
    int(RECORD_SECONDS * SAMPLE_RATE),
    samplerate=SAMPLE_RATE,
    channels=1,
    dtype="float32"
)

sd.wait()

print("⏹️ Recording finished.")

sf.write(
    AUDIO_FILE,
    audio,
    SAMPLE_RATE
)

print("💾 New recording saved.")


# ==============================
# PROCESS VOICE QUESTION
# ==============================

try:

    result = process_voice_question(AUDIO_FILE)

    print("\n========================================")
    print("🌾 FINAL AGRIRAG RESPONSE")
    print("========================================")

    print("\n🌐 Language:")
    print(result["language"])

    print("\n🎤 Question:")
    print(result["question"])

    print("\n🤖 Answer:")
    print(result["answer"])


except Exception as e:

    print("\n========================================")
    print("❌ ERROR")
    print("========================================")

    print(e)
