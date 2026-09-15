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

BACKUP_MODEL = "gemini-3.5-flash"


# -----------------------------------------
# GENERATE RESPONSE USING ONE MODEL
# -----------------------------------------

def call_gemini(model, prompt):

    print(f"\n🤖 Using model: {model}")

    response = client.models.generate_content(
        model=model,
        contents=prompt
    )

    return response.text


# -----------------------------------------
# MAIN LLM SERVICE
# -----------------------------------------

def generate_llm_answer(prompt):

    # -----------------------------------------
    # TRY PRIMARY MODEL
    # -----------------------------------------

    try:

        return call_gemini(
            PRIMARY_MODEL,
            prompt
        )

    except Exception as primary_error:

        error_message = str(primary_error)

        print("\n⚠️ Primary model failed.")
        print("Error:", error_message)


        # -----------------------------------------
        # TEMPORARY SERVER ERROR (503)
        # -----------------------------------------

        if "503" in error_message:

            print(
                "\n⚠️ Primary Gemini model is temporarily "
                "unavailable."
            )

            # Short wait instead of 10/20/40 seconds
            time.sleep(2)


        # -----------------------------------------
        # RATE LIMIT / QUOTA ERROR (429)
        # -----------------------------------------

        elif "429" in error_message:

            print(
                "\n⚠️ Primary model reached its "
                "rate limit."
            )


        # -----------------------------------------
        # OTHER ERROR
        # -----------------------------------------

        else:

            print(
                "\n⚠️ Primary model encountered "
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

        return call_gemini(
            BACKUP_MODEL,
            prompt
        )

    except Exception as backup_error:

        print("\n❌ Backup model also failed.")
        print(
            "Error:",
            str(backup_error)
        )


    # -----------------------------------------
    # BOTH MODELS FAILED
    # -----------------------------------------

    return (
        "Sorry, the agriculture AI service is "
        "temporarily unavailable. Please try again "
        "after some time."
    )
# -----------------------------------------
# TEST THE LLM SERVICE
# -----------------------------------------

if __name__ == "__main__":

    test_prompt = """
Answer the following question in simple English.

What is agriculture?
"""

    answer = generate_llm_answer(test_prompt)

    print("\n========================================")
    print("🌾 LLM SERVICE TEST")
    print("========================================")

    print(answer)