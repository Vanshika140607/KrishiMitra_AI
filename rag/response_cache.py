import sqlite3
import hashlib
from pathlib import Path
from datetime import datetime


# -----------------------------------------
# CACHE DATABASE LOCATION
# -----------------------------------------

CACHE_DIR = Path("vectorstore")
CACHE_DIR.mkdir(exist_ok=True)

CACHE_DB = CACHE_DIR / "response_cache.db"


# -----------------------------------------
# CREATE DATABASE TABLE
# -----------------------------------------

def create_cache_table():

    connection = sqlite3.connect(CACHE_DB)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS response_cache (
            cache_key TEXT PRIMARY KEY,
            question TEXT NOT NULL,
            language TEXT NOT NULL,
            answer TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


# -----------------------------------------
# CREATE UNIQUE CACHE KEY
# -----------------------------------------

def create_cache_key(question, language):

    text = f"{question.strip().lower()}|{language.strip().lower()}"

    cache_key = hashlib.sha256(
        text.encode("utf-8")
    ).hexdigest()

    return cache_key


# -----------------------------------------
# GET ANSWER FROM CACHE
# -----------------------------------------

def get_cached_answer(question, language):

    create_cache_table()

    cache_key = create_cache_key(
        question,
        language
    )

    connection = sqlite3.connect(CACHE_DB)

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT answer
        FROM response_cache
        WHERE cache_key = ?
        """,
        (cache_key,)
    )

    result = cursor.fetchone()

    connection.close()

    if result:
        print("\n⚡ Answer found in cache.")

        return result[0]

    print("\n🔎 Answer not found in cache.")

    return None


# -----------------------------------------
# SAVE ANSWER TO CACHE
# -----------------------------------------

def save_answer_to_cache(
    question,
    language,
    answer
):

    create_cache_table()

    cache_key = create_cache_key(
        question,
        language
    )

    connection = sqlite3.connect(CACHE_DB)

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT OR REPLACE INTO response_cache
        (
            cache_key,
            question,
            language,
            answer,
            created_at
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            cache_key,
            question,
            language,
            answer,
            datetime.now().isoformat()
        )
    )

    connection.commit()
    connection.close()

    print("\n💾 Answer saved to cache.")


# -----------------------------------------
# TEST CACHE
# -----------------------------------------

if __name__ == "__main__":

    question = "What are the recommendations for rice cultivation?"

    language = "English"

    test_answer = "Rice cultivation requires suitable varieties, proper nursery management and fertilizer application."

    print("\n========================================")
    print("🌾 RESPONSE CACHE TEST")
    print("========================================")

    save_answer_to_cache(
        question,
        language,
        test_answer
    )

    answer = get_cached_answer(
        question,
        language
    )

    print("\nCached answer:")
    print(answer)
