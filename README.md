# Session-Based Dice Game API (FastAPI)

A REST API that models a dice game using session-based state, clean architecture, and testable business logic — without relying on global mutable state.

---

## Why this project exists

Most beginner projects rely on global variables or in-memory state, which breaks in real-world APIs.

This project solves that by:

- introducing session-based state management  
- isolating game data per session  
- structuring logic into service and repository layers  
- making the system fully testable  

---

## Key Features

- Session-based gameplay (no shared global state)  
- FastAPI REST API  
- SQLite persistence (repository layer)  
- Service layer for business logic  
- Automated tests (pytest)  
- Docker support  
- CI with linting, formatting, typing, and tests  

---

## Architecture

- **API layer**: request validation and HTTP handling  
- **Service layer**: game rules and orchestration  
- **Repository layer**: database interaction  
- **Domain layer**: pure models and logic  

---

## Example Usage

### Create session

```bash
POST /sessions
{
  "game_session_id": "c1b2e3..."
}
```
### Roll dice

```bash
POST /sessions/{game_session_id}/roll
{
  "game_session_id": "c1b2e3...",
  "rolls": [3, 5],
  "total": 8,
  "outcome": "lose",
  "points_delta": -3,
  "points_total": -3,
  "extra_turn": false
}
```
### API docs:

http://localhost:8000/docs


## Run Locally

```bash
pip install -e .
uvicorn dice_game.api.app:app --reload
```

## Run with Docker

```bash
docker build -t dice-game-api .
docker run -p 8000:8000 dice-game-api
```

## Testing

```bash
pytest
```

### CI pipeline runs:

- Ruff (linting)
- Black (formatting)
- Mypy (type checking)
- Pytest (tests)

---

## What this project demonstrates

- Designing stateful systems without global variables
- Clean separation between API, service, and storage layers
- Writing testable backend logic
- Building production-style Python APIs with FastAPI
- Using Docker for containerization
- Setting up CI pipelines for quality assurance