# 🎪 TV Friend

A full-stack media tracker (TV series, movies, anime etc) that allows users to search for media, save them to a personal watchlist, track watching status, and rate them.

The project was originally built as a desktop app using Python/Flet, but has been completely rewritten into a ✨modern web application (FastAPI + React)✨.

## 🛠 Tech Stack

**Backend:**
* Python 3.11+
* FastAPI (REST API)
* SQLAlchemy 2.0 (ORM)
* PostgreSQL (Database)
* Alembic (Migrations)
* JWT (Authentication)

**Frontend:**
* React 18 (Vite)
* TypeScript
* Tailwind CSS (Styling)
* Zustand (State Management)
* Axios (HTTP Client)

**External APIs:**
* [Kinopoisk Unofficial API](https://kinopoiskapiunofficial.tech/) (Media search and metadata)

## 🚀 Features

* 🔐 User registration and JWT authentication
* 🔍 Search for movies, TV series, and shows
* 📝 Add media to a personal watchlist
* ⭐ Update watch status and personal ratings
* 🗑 Remove items from the watchlist

## 📁 Project Structure
```text
tv-friend/
├── backend/            # FastAPI application
│ ├── app/              # Main application code
│ │ ├── core/           # Security and infrastructure
│ │ ├── models/         # SQLAlchemy database models
│ │ ├── routers/        # HTTP endpoints
│ │ ├── schemas/        # Pydantic validation schemas
│ │ └── services/       # Business logic and API clients
│ └── alembic/          # Database migrations
├── frontend/           # React SPA
│ └── src/
│ ├── api/              # Axios clients
│ ├── components/       # Reusable UI components
│ ├── pages/            # Route components
│ └── store/            # Zustand state
└── docker-compose.yml  # Local PostgreSQL setup
```


## ⚙️ How to Run Locally

### 1. Start the Database
Make sure you have Docker installed. Run this from the project root:
```bash
docker compose up -d
```
### 2. Backend Setup
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
pip install -r requirements.txt
```
Create a .env file in the backend folder (use .env.example as a template) and add your Kinopoisk API key.
```bash
alembic upgrade head
uvicorn app.main:app --reload
```
API will be available at http://localhost:8000. Swagger docs at http://localhost:8000/docs.

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
The app will be available at http://localhost:5173.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.