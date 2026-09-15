import os

from dotenv import load_dotenv
from google import genai

from .retriever import retrieve_documents, remove_duplicates


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY was not found in .env")


client = genai.Client(api_key=api_key)


def create_search_query(question, language):

    # English questions can be searched directly
    if language == "English":
        return question

    prompt = f"""
Convert the following agricultural question into clear English
for searching an agricultural knowledge database.

Original language: {language}

Question:
{question}

Important:
- Preserve the exact agricultural meaning.
- Do not answer the question.
- Do not add new information.
- Return ONLY the English search query.
"""

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt
    )

    return response.text.strip()


def retrieve_multilingual_documents(
    question,
    language,
    number_of_results=8
):

    print("\n🌐 Creating search query...")

    search_query = create_search_query(
        question,
        language
    )

    print("\n🔎 Search query:")
    print(search_query)

    print("\n📚 Searching ChromaDB...")

    results = retrieve_documents(
        search_query,
        number_of_results=number_of_results
    )

    results = remove_duplicates(results)

    return results