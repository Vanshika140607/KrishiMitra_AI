import os

from dotenv import load_dotenv
from google import genai


# Load variables from .env
load_dotenv()


# Get Gemini API key
api_key = os.getenv("GEMINI_API_KEY")


# Check whether the key was found
if not api_key:
    raise ValueError("GEMINI_API_KEY was not found in .env")


# Create Gemini client
client = genai.Client(api_key=api_key)


# Send a test question
response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="Explain rice cultivation in 3 simple points."
)


# Display the answer
print("\n==============================")
print("GEMINI RESPONSE")
print("==============================")

print(response.text)