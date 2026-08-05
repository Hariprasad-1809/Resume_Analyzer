# Resume Role Match Analyzer 🚀

An AI-powered web application that analyzes a candidate's resume (PDF) against target job roles. Rather than giving a simple ATS keyword percentage, it performs deep semantic parsing, skill extraction, experience matching, title alignment, and optional AI-driven personalized feedback.

---

## ✨ Features

- 📄 **Resume Upload & Parsing**: Parses PDF resumes to extract structured layout, text, contact information, work experience, projects, skills, education, and achievements using PyMuPDF.
- 🎯 **Intelligent Skill Matching**: Extracts and compares skills using fuzzy matching (`RapidFuzz`) and exact phrase mappings.
- 🧠 **Semantic Matching Engine**: Uses sentence-transformers (`all-MiniLM-L6-v2`) and NLP (`spaCy`) to compute explainable relevance scores across skill overlap, experience depth, title matching, and project alignment.
- 🤖 **AI Recommendations (OpenRouter Integration)**: Generates tailored feedback, missing keywords, structural refinements, and learning resources powered by LLMs via OpenRouter.
- 📊 **Interactive Dashboard**: Modern glassmorphic dashboard built with Next.js, Tailwind CSS, and Recharts visualization.
- ⚙️ **Configurable Weights**: Fine-tune component weighting (skills, experience, projects) directly from the application UI.
- 🔒 **Privacy & Local State**: Runs with zero cloud dependency by default using local SQLite storage, with full PostgreSQL support when configured.

---

## 🛠️ Tech Stack

### Backend
- **Framework**: Python 3.10+ / FastAPI / Uvicorn
- **Parsing & NLP**: PyMuPDF (`fitz`), spaCy (`en_core_web_sm`), Sentence-Transformers (`all-MiniLM-L6-v2`), RapidFuzz
- **AI Integration**: OpenRouter API (`httpx`)
- **Database & ORM**: SQLite / PostgreSQL (SQLAlchemy)
- **Validation**: Pydantic v2

### Frontend
- **Framework**: Next.js 14+ (App Router, TypeScript)
- **Styling**: Tailwind CSS, Lucide Icons, Modern Glassmorphism
- **Visualization**: Recharts
- **HTTP Client**: Axios
- **File Upload**: React Dropzone

---

## 📁 Project Structure

```
Resume-Role-Match-Analyzer/
├── backend/
│   ├── app/
│   │   ├── api/          # FastAPI route handlers & endpoints
│   │   ├── core/         # Config, database setup, & custom exceptions
│   │   ├── db/           # Database seeds & initial data
│   │   ├── models/       # SQLAlchemy ORM models
│   │   ├── schemas/      # Pydantic data validation schemas
│   │   └── services/     # Parser, matcher, AI recommendation & extractor logic
│   ├── uploads/          # Local resume uploads (git-ignored)
│   ├── .env.example      # Environment template (safe to commit)
│   ├── Dockerfile        # Container build definition
│   └── requirements.txt  # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── app/          # Next.js App Router pages (Upload, Dashboard, History, Settings)
│   │   └── components/   # UI components, layout, and charts
│   └── package.json      # Node dependencies & scripts
├── .gitignore            # Root Git ignore rules (protects API keys & secrets)
├── README.md             # Project documentation
└── LICENSE               # MIT License
```

---

## ⚙️ Environment & API Key Setup

> [!CAUTION]
> **Security Reminder**: Never commit `.env` files or hardcoded API keys to Git. Your `.env` files are ignored by `.gitignore` by default.

### 1. Backend Environment Setup
Copy `.env.example` in the `backend/` directory to `.env`:

```bash
cd backend
cp .env.example .env
```

Edit `backend/.env` to configure your environment variables:

```env
# Database Configuration
DATABASE_URL=sqlite:///./sql_app.db
ENV=development
PROJECT_NAME="Resume Role Match Analyzer"

# CORS Configuration
ALLOWED_ORIGINS=["http://localhost:3000"]

# OpenRouter API Key (Optional for AI-powered suggestions)
# Get your API key from: https://openrouter.ai/keys
OPENROUTER_API_KEY=your_actual_api_key_here
OPENROUTER_MODEL=nvidia/nemotron-3-ultra-550b-a55b:free
```

---

## 🚀 Running Locally

### 1. Backend Setup (FastAPI)

Navigate to the `backend` folder and set up a Python virtual environment:

```bash
# Navigate to backend directory
cd backend

# Create virtual environment (optional but recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy language model
python -m spacy download en_core_web_sm
```

Start the backend server using **`app.main:app`**:

```bash
python -m uvicorn app.main:app --reload --port 8000
```

The backend server will run at:
- **API Base URL**: `http://localhost:8000`
- **Interactive Swagger Docs**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

---

### 2. Frontend Setup (Next.js)

Open a new terminal, navigate to the `frontend` folder, and install dependencies:

```bash
cd frontend

# Install Node modules
npm install

# Start Next.js development server
npm run dev
```

The frontend application will be available at:
- `http://localhost:3000`

---

## 🔌 API Endpoints Overview

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/v1/resume/roles` | List pre-seeded target job roles |
| `POST` | `/api/v1/resume/analyze` | Upload PDF resume & target role for full analysis |
| `GET` | `/api/v1/history` | List previous resume evaluation records |
| `GET` | `/api/v1/history/{id}` | Get detailed evaluation results for a specific ID |

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for details.
