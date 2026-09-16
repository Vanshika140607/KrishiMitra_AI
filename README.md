# 🌾 KrishiMitra AI

## KrishiMitra AI, an AI-powered agriculture chatbot

KrishiMitra AI is a web-based agriculture chatbot designed to provide relevant and easy-to-understand agricultural information.

The application combines **Retrieval-Augmented Generation (RAG), multilingual embeddings, vector search, Google Gemini, and voice interaction** to answer agriculture-related questions.

---

## 🌱 Features

- 🌾 Agriculture-related question answering
- 🤖 AI-generated responses using Google Gemini
- 📚 Retrieval-Augmented Generation (RAG)
- 🗄️ ChromaDB vector database
- 🧠 Multilingual semantic search
- 🇬🇧 English support
- 🇮🇳 Hindi support
- 🇮🇳 Marathi support
- 🎤 Voice input
- 📄 ICAR agricultural resources
- 🌐 Streamlit web interface
- ☁️ Streamlit Cloud deployment

---

## 🔄 How It Works

**User Question → Query Processing → ChromaDB Retrieval → Relevant Agricultural Context → Google Gemini → Structured Answer**

The system retrieves relevant information from the agricultural knowledge base and provides it to Gemini to generate a clear and structured response.

---

## 📚 Knowledge Base

The chatbot uses agricultural resources including publications and advisories from **ICAR (Indian Council of Agricultural Research)**.

The current knowledge base contains:

**4,559 searchable document chunks**

---

## 🧠 Embeddings

KrishiMitra AI uses:

`sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`

This multilingual embedding model converts text into numerical vector representations.

These vectors are stored in **ChromaDB** to enable semantic search and retrieval of relevant agricultural information.

---

## 🤖 Generative AI

The chatbot uses **Google Gemini** to generate the final response.

Gemini receives the user's question along with relevant information retrieved from the agricultural knowledge base.

---

## 🌐 Multilingual Support

KrishiMitra AI supports:

| Language | Support |
|---|---|
| English | ✅ |
| Hindi | ✅ |
| Marathi | ✅ |

Users can ask agriculture-related questions in their preferred language.

---

## 🎤 Voice Interaction

Users can record their agricultural question directly through the application.

The voice is converted into text and then processed through the RAG pipeline to generate an agricultural answer.

---

## 🛠️ Tech Stack

### AI & NLP
- Google Gemini
- Retrieval-Augmented Generation (RAG)
- Sentence Transformers
- Multilingual Embeddings

### Database
- ChromaDB

### Development
- Python
- Streamlit
- PyPDF
- LangChain Text Splitters
- Speech Recognition

### Deployment
- Git
- GitHub
- Streamlit Cloud

---

## 📂 Project Structure

```text
KrishiMitra_AI/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│   └── documents/
│
├── ingestion/
│   └── create_vectorstore.py
│
├── rag/
│   ├── __init__.py
│   ├── retriever.py
│   ├── answer_generator.py
│   ├── llm_service.py
│   └── response_cache.py
│
├── models/
├── prediction/
├── chatbot/
│
├── utils/
│   ├── __init__.py
│   ├── speech_to_text.py
│   └── test_voice_rag.py
│
└── vectorstore/
    └── chroma/