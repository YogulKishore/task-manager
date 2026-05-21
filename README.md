# TaskFlow – Task Manager API

A full-stack task manager built with **FastAPI**, **PostgreSQL**, and vanilla **HTML/CSS/JS**.

🔗 **Live Demo:** [task-manager-cbv3.onrender.com](https://task-manager-cbv3.onrender.com)
📖 **API Docs:** [your-app.onrender.com/docs](https://your-app.onrender.com/docs)

---

## Features

- JWT-based authentication (register, login)
- Full task CRUD (create, read, update, delete)
- Task ownership isolation — users only see their own tasks
- Pagination and `?completed=true/false` filtering
- Clean folder structure
- Pytest test suite
- Dockerized for easy deployment

---

## Tech Stack

| Layer      | Technology               |
|------------|--------------------------|
| Backend    | FastAPI, Python 3.11     |
| Database   | PostgreSQL + SQLAlchemy  |
| Auth       | JWT (python-jose) + bcrypt (passlib) |
| Frontend   | Plain HTML + CSS + JS    |
| Deployment | Render                   |

---

## Project Structure

```
task-manager/
├── backend/
│   ├── __init__.py
│   ├── auth.py          # JWT creation & verification, bcrypt
│   ├── database.py      # SQLAlchemy engine & session
│   ├── models.py        # User & Task ORM models
│   ├── schemas.py       # Pydantic request/response schemas
│   └── routers/
│       ├── auth.py      # POST /register, POST /login
│       └── tasks.py     # CRUD /tasks endpoints
├── frontend/
│   ├── index.html       # Login / Register page
│   └── tasks.html       # Task manager dashboard
├── tests/
│   └── test_api.py      # pytest test cases
├── main.py              # FastAPI app entry point
├── requirements.txt
├── Dockerfile
├── .env.example
└── README.md
```

---

## Environment Variables

Copy `.env.example` to `.env` and fill in the values:

```bash
cp .env.example .env
```

| Variable                    | Description                        |
|-----------------------------|------------------------------------|
| `DATABASE_URL`              | PostgreSQL connection string        |
| `SECRET_KEY`                | Secret for JWT signing              |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiry in minutes (default 60) |

> **Never commit `.env` to git.**  
> Generate a secure secret key:
> ```bash
> python -c "import secrets; print(secrets.token_hex(32))"
> ```

---

## Run Locally

### 1. Clone the repo

```bash
git clone https://github.com/your-username/task-manager.git
cd task-manager
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment

```bash
cp .env.example .env
# Edit .env with your DATABASE_URL and SECRET_KEY
```

For local development you can use SQLite by setting:
```
DATABASE_URL=sqlite:///./taskmanager.db
```

### 5. Run the server

```bash
uvicorn main:app --reload
```

App runs at: http://localhost:8000  
API docs at: http://localhost:8000/docs

---

## Run with Docker

```bash
docker build -t task-manager .
docker run -p 8000:8000 --env-file .env task-manager
```

---

## Run Tests

```bash
pytest
```

Test cases cover:
- User registration and login
- Duplicate username/email rejection
- Task creation, retrieval, update, deletion
- Task ownership isolation
- Completed filter
- Unauthenticated access rejection

---

## API Endpoints

### Authentication

| Method | Endpoint    | Description         |
|--------|-------------|---------------------|
| POST   | `/register` | Create a new user   |
| POST   | `/login`    | Login, returns JWT  |

### Tasks (all require `Authorization: Bearer <token>`)

| Method | Endpoint       | Description                        |
|--------|----------------|------------------------------------|
| POST   | `/tasks`       | Create a task                      |
| GET    | `/tasks`       | Get all tasks (paginated, filtered)|
| GET    | `/tasks/{id}`  | Get a specific task                |
| PUT    | `/tasks/{id}`  | Update a task (title/desc/status)  |
| DELETE | `/tasks/{id}`  | Delete a task                      |

**Query params for GET /tasks:**
- `?page=1&page_size=10` — pagination
- `?completed=true` or `?completed=false` — filter by status

---

## Deployment (Render)

1. Push your code to GitHub
2. Go to [render.com](https://render.com) → New → PostgreSQL → create a free database
3. Copy the **External Database URL**
4. New → Web Service → connect your GitHub repo
5. Set environment variables:
   - `DATABASE_URL` → paste the PostgreSQL URL
   - `SECRET_KEY` → your generated secret
6. Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
7. Deploy!
