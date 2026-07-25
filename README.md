# CivicAI

An AI-powered public service assistant that helps citizens understand official documents, check eligibility, and get personalized action plans in multiple languages.

Powered by a React frontend, FastAPI backend, and a locally running Gemma 4 model via Ollama.

## Architecture

- **Frontend**: React, Vite, Framer Motion
- **Backend**: FastAPI, PyMuPDF, pytesseract
- **LLM Engine**: Dual providers supported (Local Ollama `gemma4:latest` OR Gemini API)

## Prerequisites

1. **Node.js** (for the Vite frontend)
2. **Python 3.10+** (for the FastAPI backend)
3. **Ollama** running locally with Gemma 4:
   ```bash
   ollama pull gemma4:latest
   ollama run gemma4:latest
   ```
4. **System Dependencies** (for OCR fallback):
   - **Tesseract OCR**: Needs to be installed and available in your PATH.
   - **Poppler**: Needed for converting scanned PDFs to images (e.g., via `brew install poppler` on macOS or downloading Windows binaries).
5. **Environment Configuration**:
   - Copy `.env.example` to `.env` in the `backend/` directory.
   - Add your `GEMINI_API_KEY` to the `.env` file if you wish to use the Gemini cloud provider instead of local Ollama. The app functions entirely locally without it.

## Running the Application Locally

### 1. Start the Backend

Navigate to the `backend/` directory, install requirements, and start Uvicorn:

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 2. Start the Frontend

In a separate terminal, navigate to the `frontend/` directory, install NPM packages, and start Vite:

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at `http://localhost:5173`. API requests are automatically proxied to the backend at port 8000.

## Features

- **Document Analysis**: Upload official PDFs or scanned images.
- **Plain Language Explanations**: Uses Gemma 4 to explain the document simply.
- **Multilingual Support**: Supports English, Hindi, Bengali, Odia, etc.
- **Eligibility & Checklists**: Automatically extracts eligibility status and a checklist of required actions.
- **Missing Document Detection**: Identifies and flags missing supporting documents.
- **Follow-up Chat**: Ask questions about your document in context.
