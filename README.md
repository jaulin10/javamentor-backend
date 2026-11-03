# JavaMentor — Backend API

REST API for **JavaMentor**, a Java learning platform that combines an AI chat assistant with a catalog of hands-on exercises.

Frontend: [javamentor-frontend](https://github.com/jaulin10/javamentor-frontend)

## Tech stack

- **Python 3.11** + **FastAPI**
- **PostgreSQL** with **SQLAlchemy** (ORM)
- **JWT** authentication (`python-jose`, `passlib[bcrypt]`)
- **OpenAI API** for the conversational assistant
- **Docker Compose** for a local PostgreSQL instance

## Features

- User registration and login with JWT tokens
- Per-user Java level (beginner / intermediate / advanced) used to adapt the assistant's answers
- Chat assistant with multi-conversation history
- Exercise catalog organized by difficulty and topic

## API endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/register` | Create an account |
| POST | `/api/auth/login` | Log in and get a JWT |
| GET | `/api/auth/me` | Current user profile |
| POST | `/api/chat/send` | Send a message to the assistant |
| GET | `/api/chat/conversations` | List the user's conversations |
| GET | `/api/chat/conversations/{id}` | Get one conversation |
| DELETE | `/api/chat/conversations/{id}` | Delete a conversation |
| GET | `/api/exercises/` | List exercises |
| GET | `/api/exercises/{id}` | Get one exercise |
| POST | `/api/exercises/seed` | Load sample exercises |

Interactive docs are available at `http://localhost:8000/docs` once the server is running.

## Project structure

```
app/
├── main.py          # FastAPI app, CORS, routers
├── database.py      # SQLAlchemy engine and session
├── models/          # User, Conversation, Exercise
├── schemas/         # Pydantic request/response models
├── routers/         # auth, chat, exercises
├── services/        # auth, conversation, OpenAI logic
└── utils/           # password hashing, JWT helpers
```

## Getting started

### 1. Clone and install

```bash
git clone https://github.com/jaulin10/javamentor-backend.git
cd javamentor-backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Start PostgreSQL

```bash
docker compose up -d
```

### 3. Configure environment variables

Copy the example file and fill in your own values:

```bash
cp .env.example .env
```

| Variable | Description |
|---|---|
| `DATABASE_URL` | PostgreSQL connection string |
| `SECRET_KEY` | Secret used to sign JWT tokens |
| `OPENAI_API_KEY` | Your OpenAI API key |

`.env` is ignored by Git — never commit real credentials.

### 4. Run the server

```bash
uvicorn app.main:app --reload
```

The API runs at `http://localhost:8000`.

## Roadmap

- Automated tests (pytest) for auth, chat and exercises
- Database migrations with Alembic
- Code submission and automatic evaluation of exercise solutions
- Progress tracking per user and per topic
- Dockerfile for the API itself

## License

MIT — see [LICENSE](LICENSE).
