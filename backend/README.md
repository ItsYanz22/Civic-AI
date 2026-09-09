# CivicAI 🏛️🤖

**An AI-powered Public Service Assistant built using Google Gemma 4**

CivicAI is an intelligent assistant that helps citizens understand government documents, determine eligibility for welfare schemes, identify missing documents, and simplify complex administrative processes using Retrieval-Augmented Generation (RAG) and Google Gemma 4.

---

## 🚀 Problem Statement

Millions of citizens struggle to understand government schemes, official notifications, eligibility criteria, and required documentation due to complex legal language and scattered information.

CivicAI bridges this gap by providing a conversational AI assistant that can:

- Explain government documents in simple language.
- Analyze uploaded documents.
- Determine scheme eligibility.
- Identify missing documents.
- Answer follow-up questions with evidence.

---

## ✨ Features

- 📄 Government document understanding
- 🖼️ OCR support for scanned documents and images
- 🔍 Retrieval-Augmented Generation (RAG)
- 🤖 Powered by Google Gemma 4
- 📋 Eligibility analysis
- 📑 Missing document detection
- 💬 Conversational AI assistant
- 📚 Evidence-based responses

---

## 🏗️ Project Architecture

```
User Upload
        │
        ▼
 PDF / Image Parser
        │
        ▼
 OCR (Fallback)
        │
        ▼
 Text Extraction
        │
        ▼
 Chunking
        │
        ▼
 Embeddings
        │
        ▼
 Vector Database
        │
        ▼
 Relevant Context Retrieval
        │
        ▼
 Google Gemma 4
        │
        ▼
 AI Response
```

---

## 🛠️ Tech Stack

### Backend

- Python
- FastAPI

### Document Processing

- PyMuPDF
- OCR (Fallback)

### AI

- Google Gemma 4

### RAG

- Sentence Transformers
- Vector Database
- Semantic Search

### Frontend

- (To be added)

---

## 📂 Project Structure

```
backend/
│
├── prompts/
├── services/
├── routes/
├── uploads/
├── data/
├── embeddings/
├── vector_store/
└── app.py
```

---

## 📌 Current Progress

- ✅ PDF Parsing
- ✅ OCR Fallback Pipeline
- ✅ Markdown Generation
- ✅ JSON Conversion
- ✅ Document Chunking
- ⏳ Embedding Generation
- ⏳ Vector Database
- ⏳ RAG Pipeline
- ⏳ Gemma 4 Integration
- ⏳ Frontend Integration

---

## 🎯 Future Enhancements

- Multi-language support
- Voice interaction
- More government schemes
- Better document verification
- Mobile application
- Personalized citizen dashboard

---

## 👥 Team

Build with Gemma Hackathon Team

---

## 📄 License

This project is developed for the **Build with Gemma Hackathon** and is intended for educational and research purposes.
## Integrations (Optional)

### Snowflake (Analytics Logging)
To log analysis sessions and chat messages to a data warehouse:
1. Sign up for a [Snowflake account](https://www.snowflake.com/).
2. Run the DDL script in \scripts/snowflake_schema.sql\ to create the tables.
3. Add credentials to your .env:
   `env
   SNOWFLAKE_ACCOUNT=your_account
   SNOWFLAKE_USER=your_user
   SNOWFLAKE_PASSWORD=your_password
   SNOWFLAKE_WAREHOUSE=your_warehouse
   SNOWFLAKE_DATABASE=your_database
   SNOWFLAKE_SCHEMA=your_schema
   SNOWFLAKE_ROLE=your_role
   ``n
**Fail-Soft Design:** The Snowflake integration is entirely optional and uses fire-and-forget logic. If credentials are missing or the services are down, CivicAI logs a warning and continues functioning normally without blocking or delaying the user experience.
