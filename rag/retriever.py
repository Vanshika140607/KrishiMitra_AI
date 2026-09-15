from pathlib import Path

import chromadb
from langchain_huggingface import HuggingFaceEmbeddings


# --------------------------------------------------
# PATHS
# --------------------------------------------------

VECTORSTORE_DIR = Path("vectorstore/chroma")


# --------------------------------------------------
# EMBEDDING MODEL
# --------------------------------------------------

MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


print("Loading multilingual embedding model...")

embeddings = HuggingFaceEmbeddings(
    model_name=MODEL_NAME
)

print("Multilingual embedding model loaded.")


# --------------------------------------------------
# CONNECT TO CHROMADB
# --------------------------------------------------

client = chromadb.PersistentClient(
    path=str(VECTORSTORE_DIR)
)

collection = client.get_collection(
    name="agriculture_documents"
)

print("Connected to ChromaDB.")
print("Total documents:", collection.count())


# --------------------------------------------------
# RETRIEVE DOCUMENTS
# --------------------------------------------------

def retrieve_documents(question, number_of_results=20):

    # Convert question into vector
    question_vector = embeddings.embed_query(
        question
    )

    # Retrieve more candidates
    results = collection.query(
        query_embeddings=[question_vector],
        n_results=number_of_results
    )

    return results


# --------------------------------------------------
# REMOVE DUPLICATES
# --------------------------------------------------

def remove_duplicates(results):

    unique_documents = []
    unique_metadatas = []

    seen_texts = set()

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    for i in range(len(documents)):

        text = documents[i].strip()

        if text not in seen_texts:

            seen_texts.add(text)

            unique_documents.append(text)
            unique_metadatas.append(
                metadatas[i]
            )

    return {
        "documents": [unique_documents],
        "metadatas": [unique_metadatas]
    }


# --------------------------------------------------
# KEYWORD RELEVANCE
# --------------------------------------------------

def calculate_keyword_score(question, document):

    question_lower = question.lower()
    document_lower = document.lower()

    score = 0

    # =================================================
    # MULTILINGUAL AGRICULTURE TERMS
    # Hindi + Marathi + English
    # =================================================

    agriculture_terms = {

        # -------------------------
        # RICE
        # -------------------------
        "rice": ["rice", "paddy"],
        "paddy": ["rice", "paddy"],

        "भात": ["rice", "paddy"],
        "धान": ["rice", "paddy"],
        "तांदूळ": ["rice", "paddy"],

        # -------------------------
        # CULTIVATION / FARMING
        # -------------------------
        "cultivation": ["cultivation", "farming"],
        "farming": ["cultivation", "farming"],

        "खेती": ["cultivation", "farming"],
        "कृषि": ["cultivation", "farming"],

        "लागवड": ["cultivation"],
        "लागवडी": ["cultivation"],
        "लागवडीसाठी": ["cultivation"],

        # -------------------------
        # RECOMMENDATION
        # -------------------------
        "recommendation": ["recommendation", "recommended"],
        "recommendations": ["recommendation", "recommended"],
        "recommended": ["recommendation", "recommended"],

        "सिफारिश": ["recommendation", "recommended"],
        "सिफारिशें": ["recommendation", "recommended"],
        "सिफारिशों": ["recommendation", "recommended"],

        "शिफारस": ["recommendation", "recommended"],
        "शिफारशी": ["recommendation", "recommended"],
        "शिफारशींच्या": ["recommendation", "recommended"],

        # -------------------------
        # VARIETY
        # -------------------------
        "variety": ["variety", "varieties"],
        "varieties": ["variety", "varieties"],

        "किस्म": ["variety", "varieties"],
        "किस्में": ["variety", "varieties"],

        "वाण": ["variety", "varieties"],
        "जाती": ["variety", "varieties"],

        # -------------------------
        # SEED
        # -------------------------
        "seed": ["seed"],
        "seeds": ["seed"],

        "बीज": ["seed"],
        "बियाणे": ["seed"],
        "बियाण्य": ["seed"],

        # -------------------------
        # NURSERY
        # -------------------------
        "nursery": ["nursery"],

        "नर्सरी": ["nursery"],
        "रोपवाटिका": ["nursery"],

        # -------------------------
        # FERTILIZER
        # -------------------------
        "fertilizer": ["fertilizer"],
        "fertilizers": ["fertilizer"],

        "उर्वरक": ["fertilizer"],
        "खत": ["fertilizer"],
        "खते": ["fertilizer"],

        # -------------------------
        # IRRIGATION
        # -------------------------
        "irrigation": ["irrigation"],

        "सिंचाई": ["irrigation"],
        "सिंचन": ["irrigation"],
        "पाणी": ["irrigation"],

        # -------------------------
        # PEST
        # -------------------------
        "pest": ["pest"],
        "pests": ["pest"],

        "कीट": ["pest"],
        "कीटक": ["pest"],
        "किड": ["pest"],
        "किडी": ["pest"],
        "कीड": ["pest"],

        # -------------------------
        # DISEASE
        # -------------------------
        "disease": ["disease"],
        "diseases": ["disease"],

        "रोग": ["disease"],
        "रोगांचा": ["disease"],
        "रोगों": ["disease"],

        # -------------------------
        # WEED
        # -------------------------
        "weed": ["weed"],
        "weeds": ["weed"],

        "खरपतवार": ["weed"],
        "तण": ["weed"],
    }


    # =================================================
    # SCORE AGRICULTURE TERMS
    # =================================================

    for question_term, english_terms in agriculture_terms.items():

        if question_term in question_lower:

            for english_term in english_terms:

                if english_term in document_lower:
                    score += 2


    # =================================================
    # LOCATION TERMS
    # =================================================

    locations = {

        "maharashtra": ["maharashtra"],
        "महाराष्ट्र": ["maharashtra"],

        "pune": ["pune"],
        "पुणे": ["pune"],

        "satara": ["satara"],
        "सातारा": ["satara"],

        "sangli": ["sangli"],
        "सांगली": ["sangli"],

        "kolhapur": ["kolhapur"],
        "कोल्हापूर": ["kolhapur"],

        "solapur": ["solapur"],
        "सोलापूर": ["solapur"],

        "ahmednagar": ["ahmednagar"],
        "अहमदनगर": ["ahmednagar"],
    }


    # =================================================
    # SCORE LOCATION MATCH
    # =================================================

    for question_location, english_locations in locations.items():

        if question_location in question_lower:

            for location in english_locations:

                if location in document_lower:
                    score += 5


    # =================================================
    # RICE + MAHARASHTRA SPECIAL BOOST
    # =================================================

    rice_question = (
        "rice" in question_lower
        or "paddy" in question_lower
        or "भात" in question_lower
        or "धान" in question_lower
        or "तांदूळ" in question_lower
    )

    maharashtra_question = (
        "maharashtra" in question_lower
        or "महाराष्ट्र" in question_lower
    )


    if rice_question and maharashtra_question:

        document_has_rice = (
            "rice" in document_lower
            or "paddy" in document_lower
        )

        document_has_maharashtra = (
            "maharashtra" in document_lower
        )

        if document_has_rice and document_has_maharashtra:
            score += 10


    # =================================================
    # RECOMMENDATION CONTENT BOOST
    # =================================================

    recommendation_phrases = [
        "recommended varieties",
        "recommended",
        "nursery sowing",
        "seed",
        "fertilizer",
        "weed management",
        "pest management",
    ]


    for phrase in recommendation_phrases:

        if phrase in document_lower:
            score += 2


    return score
# --------------------------------------------------
# RERANK DOCUMENTS
# --------------------------------------------------

def rerank_documents(question, results):

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    ranked_results = []

    for i in range(len(documents)):

        document = documents[i]

        keyword_score = calculate_keyword_score(
            question,
            document
        )

        ranked_results.append(
            {
                "document": document,
                "metadata": metadatas[i],
                "keyword_score": keyword_score
            }
        )

    # Highest keyword score first
    ranked_results.sort(
        key=lambda x: x["keyword_score"],
        reverse=True
    )

    return ranked_results


# --------------------------------------------------
# TEST
# --------------------------------------------------

if __name__ == "__main__":

    question = input(
        "\nAsk an agriculture question: "
    )

    print("\nSearching ChromaDB...")

    results = retrieve_documents(
        question,
        number_of_results=20
    )

    results = remove_duplicates(
        results
    )

    ranked_results = rerank_documents(
        question,
        results
    )

    print("\n========================================")
    print("RERANKED AGRICULTURAL INFORMATION")
    print("========================================")

    # Show top 5 after reranking
    for i, result in enumerate(
        ranked_results[:5]
    ):

        print(
            f"\n--- Result {i + 1} ---"
        )

        print(
            "Keyword score:",
            result["keyword_score"]
        )

        print(
            "Source:",
            result["metadata"]["source"]
        )

        print(
            "Page:",
            result["metadata"]["page"]
        )

        print(
            result["document"]
        )