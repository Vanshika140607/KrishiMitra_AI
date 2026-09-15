import os
import time

from dotenv import load_dotenv
from google import genai


# -----------------------------------------
# LOAD ENVIRONMENT VARIABLES
# -----------------------------------------

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY was not found in .env"
    )


# -----------------------------------------
# CREATE GEMINI CLIENT
# -----------------------------------------

client = genai.Client(
    api_key=api_key
)


# -----------------------------------------
# MODEL CONFIGURATION
# -----------------------------------------

PRIMARY_MODEL = "gemini-3.6-flash"
BACKUP_MODEL = "gemini-3.5-flash-lite"


# -----------------------------------------
# GENERATE RESPONSE USING ONE MODEL
# -----------------------------------------

def call_gemini(model, prompt):

    print(f"\n🤖 Using model: {model}")

    response = client.models.generate_content(
        model=model,
        contents=prompt
    )

    if not response.text:
        raise Exception("Gemini returned an empty response.")

    return response.text


# -----------------------------------------
# MAIN LLM SERVICE
# -----------------------------------------

def generate_llm_answer(prompt):

    # -----------------------------------------
    # TRY PRIMARY MODEL
    # -----------------------------------------

    try:

        answer = call_gemini(
            PRIMARY_MODEL,
            prompt
        )

        print("\n✅ Primary Gemini model succeeded.")

        return answer

    except Exception as primary_error:

        error_message = str(primary_error)

        print("\n⚠️ Primary model failed.")
        print("Error:", error_message)

        if "503" in error_message:

            print(
                "\n⚠️ Primary Gemini model is temporarily "
                "unavailable."
            )

            time.sleep(2)

        elif "429" in error_message:

            print(
                "\n⚠️ Primary Gemini model reached "
                "its rate limit."
            )

        else:

            print(
                "\n⚠️ Primary Gemini model encountered "
                "another error."
            )


    # -----------------------------------------
    # TRY BACKUP MODEL
    # -----------------------------------------

    try:

        print(
            f"\n🔄 Trying backup model: "
            f"{BACKUP_MODEL}"
        )

        answer = call_gemini(
            BACKUP_MODEL,
            prompt
        )

        print("\n✅ Backup Gemini model succeeded.")

        return answer

    except Exception as backup_error:

        print("\n❌ Backup model also failed.")
        print("Error:", str(backup_error))


    # -----------------------------------------
    # BOTH MODELS FAILED
    # -----------------------------------------

    raise Exception(
        "Both Gemini models are currently unavailable. "
        "Please try again later."
    )