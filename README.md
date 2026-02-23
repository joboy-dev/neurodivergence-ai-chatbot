# Neurodivergence AI Chatbot

A supportive AI chatbot that helps parents and caregivers understand neurodevelopmental conditions in children. The app uses RAG (Retrieval Augmented Generation) to provide context-aware, evidence-based responses about conditions such as ADHD, autism, dyslexia, and related topics—while always emphasizing that it provides informational support only and cannot diagnose. Users should consult qualified healthcare professionals for proper evaluation.

---

## Features

- **Authentication**: Sign up, sign in, and sign out with email and password
- **User Profiles**: View and update profile information (name, email, password)
- **Chat**: Create conversations, send messages, and receive AI-powered responses grounded in your knowledge base
- **Chat History**: Browse and continue previous conversations
- **RAG-Powered Answers**: Uses PDF documents from a local `data` folder to retrieve relevant context before generating responses
- **Neurodiversity Focus**: Tailored prompts for empathetic, non-judgmental support about neurodevelopmental conditions

---

## Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **AI/LLM**: [LangChain](https://www.langchain.com/), [OpenAI](https://openai.com/) (GPT-4o-mini, text-embedding-3-small)
- **Vector Store**: [FAISS](https://github.com/facebookresearch/faiss)
- **Database**: SQLite (configurable; supports PostgreSQL)
- **ORM**: SQLAlchemy
- **Migrations**: Alembic
- **File Storage** (optional): Firebase (Pyrebase)

---

## Prerequisites

- **Python 3.10+**
- **OpenAI API key** (for chat and embeddings)
- **PDF documents** in a `data` folder (for RAG context; app works with an empty folder but will have limited knowledge)

---

## Project Structure

```
neurodivergence-ai-chatbot/
├── app/
│   ├── components/        # UI components
│   └── pages/             # Auth, Chat, Profile, Logout
├── db/
│   ├── models/            # User, Chat, Message
│   └── database.py
├── services/
│   ├── auth.py
│   ├── chat.py
│   ├── rag.py             # RAG pipeline
│   └── user.py
├── utils/
│   ├── firebase.py
│   ├── loggers.py
│   ├── messages.py
│   └── settings.py
├── data/                  # PDFs for RAG (create if missing)
├── logs/                  # Application logs
├── alembic/               # Database migrations
├── main.py                # Entry point
└── requirements.txt
```

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd neurodivergence-ai-chatbot
```

---

### 2. Create a Virtual Environment

#### Windows (Command Prompt)

```cmd
python -m venv venv
venv\Scripts\activate
```

#### Windows (PowerShell)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

> If you get an execution policy error in PowerShell, run:  
> `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

#### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Create the `.streamlit` Directory (Skip if this is already done)

#### Windows (Command Prompt)

```cmd
mkdir .streamlit
```

#### Windows (PowerShell)

```powershell
New-Item -ItemType Directory -Path .streamlit
```

#### macOS / Linux

```bash
mkdir -p .streamlit
```

---

### 5. Configure Secrets (Skip if this is already done)

Create `.streamlit/secrets.toml` with the following structure (replace placeholders with your values):

```toml
[db_credentials]
db_type = "sqlite"
db_url = "sqlite:///neurodivergence.db"

[dir]
temp_dir = "tmp/media"

[api_keys]
openai_api_key = "your-openai-api-key-here"
```

- **db_url**: For SQLite, use `sqlite:///neurodivergence.db` (file created in project root). For PostgreSQL, use something like `postgresql://user:password@localhost:5432/dbname`.
- **openai_api_key**: Get this from [OpenAI Platform](https://platform.openai.com/api-keys).

---

### 6. Create the `data` Folder (for RAG)

Add PDF documents about neurodevelopmental conditions (ADHD, autism, dyslexia, etc.) to a `data` folder. The app loads all PDFs from this directory for retrieval.

#### Windows (Command Prompt)

```cmd
mkdir data
```

#### Windows (PowerShell)

```powershell
New-Item -ItemType Directory -Path data
```

#### macOS / Linux

```bash
mkdir -p data
```

Place your PDF files in `data/`. If the folder is empty, the app will still run but will have limited context for answers.

---

### 7. (Optional) Firebase Configuration

If you plan to use Firebase for file storage (e.g., profile pictures):

1. Create a `firebase_config.py` in the project root.
2. Add your Firebase config (see [Pyrebase docs](https://github.com/nhorvath/Pyrebase)).
3. Add `serviceAccount.json` if using Firebase Admin features.

These files are in `.gitignore` and should never be committed.

---

### 8. Run the Application

```bash
streamlit run main.py
```

The app will open in your browser (usually at `http://localhost:8501`).

---

## Quick Setup Summary by OS

| Step            | Windows (CMD)                    | Windows (PowerShell)                    | macOS / Linux                    |
|----------------|-----------------------------------|-----------------------------------------|----------------------------------|
| Create venv    | `python -m venv venv`            | `python -m venv venv`                   | `python3 -m venv venv`           |
| Activate venv  | `venv\Scripts\activate`          | `.\venv\Scripts\Activate.ps1`           | `source venv/bin/activate`       |
| Create dirs    | `mkdir .streamlit` and `mkdir data` | `New-Item -ItemType Directory -Path .streamlit, data` | `mkdir -p .streamlit data` |
| Run app        | `streamlit run main.py`          | `streamlit run main.py`                 | `streamlit run main.py`          |

---

## Configuration

### Streamlit Theme

Theme settings are in `.streamlit/config.toml`. The default is a dark theme. You can modify colors and fonts there.

### Database Migrations

To create or apply migrations:

```bash
alembic revision --autogenerate -m "Description"
alembic upgrade head
```

---

## Important Notes

- **Diagnostic Disclaimer**: The chatbot is for informational support only. It does not diagnose. Users should consult qualified healthcare professionals (pediatricians, psychologists, specialists) for evaluation.
- **Secrets**: Never commit `.streamlit/secrets.toml`, `firebase_config.py`, or `serviceAccount.json` to version control.
- **Python version**: The project uses Python 3.10+. Check with `python --version` or `python3 --version`.

---

## Troubleshooting

| Issue | Possible fix |
|-------|--------------|
| `ModuleNotFoundError` | Ensure the virtual environment is activated and run `pip install -r requirements.txt` |
| OpenAI API errors | Verify `openai_api_key` in `.streamlit/secrets.toml` and that you have API credits |
| No documents loaded | Ensure `data/` exists and contains `.pdf` files |
| Database errors | Check `db_url` in secrets. For SQLite, ensure the path is correct |
| Streamlit not opening | Try `streamlit run main.py --server.port 8501` and open `http://localhost:8501` manually |

---

## License

See the project's license file for terms.
