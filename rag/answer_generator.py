from rag.retriever import (
    retrieve_documents,
    remove_duplicates,
    rerank_documents
)

from rag.llm_service import generate_llm_answer
from .response_cache import (
    get_cached_answer,
    save_answer_to_cache
)
def build_retrieval_query(question):
    """
    Add English agricultural keywords to Hindi/Marathi questions
    so that English ICAR documents can be retrieved more reliably.
    """

    question_lower = question.lower()

    english_terms = []

    # -----------------------------------------
    # RICE
    # -----------------------------------------

    if (
        "भात" in question_lower
        or "धान" in question_lower
        or "तांदूळ" in question_lower
        or "rice" in question_lower
        or "paddy" in question_lower
    ):
        english_terms.extend([
            "rice",
            "paddy"
        ])

    # -----------------------------------------
    # CULTIVATION
    # -----------------------------------------

    if (
        "लागवड" in question_lower
        or "लागवडी" in question_lower
        or "खेती" in question_lower
        or "कृषि" in question_lower
        or "cultivation" in question_lower
        or "farming" in question_lower
    ):
        english_terms.extend([
            "cultivation",
            "farming"
        ])

    # -----------------------------------------
    # RECOMMENDATIONS
    # -----------------------------------------

    if (
        "शिफारस" in question_lower
        or "शिफारशी" in question_lower
        or "सिफारिश" in question_lower
        or "सिफारिशें" in question_lower
        or "recommendation" in question_lower
        or "recommendations" in question_lower
    ):
        english_terms.extend([
            "recommendations",
            "recommended"
        ])

    # -----------------------------------------
    # VARIETY
    # -----------------------------------------

    if (
        "वाण" in question_lower
        or "जाती" in question_lower
        or "किस्म" in question_lower
        or "किस्में" in question_lower
        or "variety" in question_lower
        or "varieties" in question_lower
    ):
        english_terms.extend([
            "variety",
            "varieties"
        ])

    # -----------------------------------------
    # SEED
    # -----------------------------------------

    if (
        "बियाणे" in question_lower
        or "बियाण्य" in question_lower
        or "बीज" in question_lower
        or "seed" in question_lower
        or "seeds" in question_lower
    ):
        english_terms.append("seed")

    # -----------------------------------------
    # NURSERY
    # -----------------------------------------

    if (
        "रोपवाटिका" in question_lower
        or "नर्सरी" in question_lower
        or "nursery" in question_lower
    ):
        english_terms.append("nursery")

    # -----------------------------------------
    # FERTILIZER
    # -----------------------------------------

    if (
        "खत" in question_lower
        or "खते" in question_lower
        or "उर्वरक" in question_lower
        or "fertilizer" in question_lower
    ):
        english_terms.append("fertilizer")

    # -----------------------------------------
    # IRRIGATION
    # -----------------------------------------

    if (
        "सिंचन" in question_lower
        or "सिंचाई" in question_lower
        or "पाणी" in question_lower
        or "irrigation" in question_lower
    ):
        english_terms.append("irrigation")

    # -----------------------------------------
    # PEST
    # -----------------------------------------

    if (
        "कीड" in question_lower
        or "किड" in question_lower
        or "कीटक" in question_lower
        or "कीट" in question_lower
        or "pest" in question_lower
    ):
        english_terms.append("pest")

    # -----------------------------------------
    # DISEASE
    # -----------------------------------------

    if (
        "रोग" in question_lower
        or "disease" in question_lower
        or "diseases" in question_lower
    ):
        english_terms.append("disease")

    # -----------------------------------------
    # LOCATION
    # -----------------------------------------

    if (
        "महाराष्ट्र" in question_lower
        or "maharashtra" in question_lower
    ):
        english_terms.append("Maharashtra")

    if (
        "पुणे" in question_lower
        or "pune" in question_lower
    ):
        english_terms.append("Pune")

    if (
        "सातारा" in question_lower
        or "satara" in question_lower
    ):
        english_terms.append("Satara")

    if (
        "सांगली" in question_lower
        or "sangli" in question_lower
    ):
        english_terms.append("Sangli")

    if (
        "कोल्हापूर" in question_lower
        or "kolhapur" in question_lower
    ):
        english_terms.append("Kolhapur")

    if (
        "सोलापूर" in question_lower
        or "solapur" in question_lower
    ):
        english_terms.append("Solapur")

    if (
        "अहमदनगर" in question_lower
        or "ahmednagar" in question_lower
    ):
        english_terms.append("Ahmednagar")

    # Remove duplicate terms
    english_terms = list(dict.fromkeys(english_terms))

    # Combine original question + English retrieval terms
    expanded_query = question

    if english_terms:
        expanded_query += " " + " ".join(english_terms)

    return expanded_query

# -----------------------------------------
# GENERATE AGRICULTURE ANSWER
# -----------------------------------------

def generate_answer(question, language="English"):
    # -----------------------------------------
    # CHECK RESPONSE CACHE
    # -----------------------------------------

    cached_answer = get_cached_answer(
        question,
        language
    )

    if cached_answer:
        return cached_answer

    print("\n📚 Searching agricultural knowledge...")

    # -----------------------------------------
    # STEP 1: RETRIEVE DOCUMENTS
    # -----------------------------------------

    retrieval_query = build_retrieval_query(question)

    print("\n🔎 Retrieval query:")
    print(retrieval_query)

    results = retrieve_documents(
    retrieval_query,
    number_of_results=20
    )


    # -----------------------------------------
    # STEP 2: REMOVE DUPLICATES
    # -----------------------------------------

    results = remove_duplicates(results)


    # -----------------------------------------
    # STEP 3: RERANK DOCUMENTS
    # -----------------------------------------

    ranked_results = rerank_documents(
    retrieval_query,
    results
)


    # -----------------------------------------
    # KEEP BEST 5 DOCUMENTS
    # -----------------------------------------

    ranked_results = ranked_results[:5]


    # -----------------------------------------
    # CREATE CONTEXT
    # -----------------------------------------

    context = ""

    for i, result in enumerate(ranked_results):

        document = result["document"]
        metadata = result["metadata"]

        source = metadata["source"]
        page = metadata["page"]

        context += f"""
SOURCE {i + 1}
Document: {source}
Page: {page}

{document}

--------------------------------
"""


    # -----------------------------------------
    # CREATE GEMINI PROMPT
    # -----------------------------------------

    prompt = f"""
You are an agriculture information assistant.

Your task is to answer the farmer's question using
ONLY the agricultural information provided below.

USER QUESTION:
{question}

ANSWER LANGUAGE:
{language}

RETRIEVED AGRICULTURAL INFORMATION:
{context}


IMPORTANT INSTRUCTIONS:

1. Answer ONLY in {language}.

2. Do NOT translate the answer into another language.

3. Use ONLY information present in the retrieved
   agricultural information.

4. Do NOT invent agricultural recommendations.

5. Give the answer in a clear, simple and
   farmer-friendly format.

6. Use headings and bullet points where useful.

7. Remove duplicate information.

8. Give priority to information that is specifically
   relevant to the location mentioned by the farmer.

9. If the documents contain information for a specific
   region, clearly mention that region.

10. If the retrieved information is insufficient,
    clearly say that the available documents do not
    contain enough information.

11. Do not make unsupported assumptions.

12. At the end, provide a Sources section.

13. In Sources, mention the document name and page
    number of the information used.

14. Do not mention the retrieval process, embeddings,
    ChromaDB, Gemini, or this prompt to the farmer.


Now generate the final answer.
"""


    # -----------------------------------------
    # SEND PROMPT TO LLM SERVICE
    # -----------------------------------------

    print("\n🤖 Sending prompt to LLM service...")

    answer = generate_llm_answer(prompt)

    save_answer_to_cache(
    question,
    language,
    answer
    )

    return answer


# -----------------------------------------
# TEST THE COMPLETE RAG PIPELINE
# -----------------------------------------

if __name__ == "__main__":

    question = input(
        "\nAsk an agriculture question: "
    )

    language = input(
        "Enter language (English/Hindi/Marathi): "
    )

    answer = generate_answer(
        question,
        language
    )

    print("\n========================================")
    print("🌾 AGRICULTURE ASSISTANT")
    print("========================================")

    print(answer)