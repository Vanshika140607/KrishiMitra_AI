from pathlib import Path

import chromadb
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader


# --------------------------------------------------
# PATHS
# --------------------------------------------------

DOCUMENTS_DIR = Path("data/documents")
VECTORSTORE_DIR = Path("vectorstore/chroma")


# --------------------------------------------------
# MULTILINGUAL EMBEDDING MODEL
# --------------------------------------------------

MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


# --------------------------------------------------
# LOAD PDFS
# --------------------------------------------------

print("\nLoading PDFs...")

documents = []

for pdf_file in DOCUMENTS_DIR.glob("*.pdf"):

    print(f"Reading: {pdf_file.name}")

    reader = PdfReader(str(pdf_file))

    for page_number, page in enumerate(reader.pages):

        text = page.extract_text()

        if text and text.strip():

            documents.append(
                {
                    "text": text,
                    "source": pdf_file.name,
                    "page": page_number + 1
                }
            )


print(f"Pages loaded: {len(documents)}")


# --------------------------------------------------
# CHUNKING
# --------------------------------------------------

print("\nCreating chunks...")

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=150
)

chunks = []

for document in documents:

    split_texts = text_splitter.split_text(
        document["text"]
    )

    for text in split_texts:

        chunks.append(
            {
                "text": text,
                "source": document["source"],
                "page": document["page"]
            }
        )


print(f"Total chunks: {len(chunks)}")


# --------------------------------------------------
# LOAD MULTILINGUAL EMBEDDING MODEL
# --------------------------------------------------

print("\nLoading multilingual embedding model...")

embeddings = HuggingFaceEmbeddings(
    model_name=MODEL_NAME
)

print("Multilingual embedding model loaded.")


# --------------------------------------------------
# CREATE CHROMA DATABASE
# --------------------------------------------------

print("\nCreating ChromaDB...")

client = chromadb.PersistentClient(
    path=str(VECTORSTORE_DIR)
)


# --------------------------------------------------
# DELETE OLD COLLECTION
# --------------------------------------------------

print("\nRemoving old ChromaDB collection if it exists...")

try:

    client.delete_collection(
        name="agriculture_documents"
    )

    print("Old collection deleted.")

except Exception:

    print("No old collection found.")


# --------------------------------------------------
# CREATE NEW COLLECTION
# --------------------------------------------------

collection = client.create_collection(
    name="agriculture_documents"
)

print("New ChromaDB collection created.")


# --------------------------------------------------
# ADD CHUNKS TO CHROMA
# --------------------------------------------------

print("\nCreating embeddings and storing documents...")

for i, chunk in enumerate(chunks):

    vector = embeddings.embed_query(
        chunk["text"]
    )

    collection.add(
        ids=[f"chunk_{i}"],
        embeddings=[vector],
        documents=[chunk["text"]],
        metadatas=[
            {
                "source": chunk["source"],
                "page": chunk["page"]
            }
        ]
    )

    # Show progress every 100 chunks
    if (i + 1) % 100 == 0:

        print(
            f"Stored {i + 1}/{len(chunks)} chunks..."
        )


# --------------------------------------------------
# FINAL RESULT
# --------------------------------------------------

print("\n================================")
print("MULTILINGUAL VECTOR DATABASE CREATED")
print("================================")

print("Embedding model:", MODEL_NAME)
print("Total chunks stored:", collection.count())