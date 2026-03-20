# Session-Based Dice Game API (FastAPI)

A production-ready REST API demonstrating enterprise software development practices through a dice game implementation with session-based state management, clean architecture, and comprehensive testing.

## Live Demo

**API Docs:** https://dice-game-api-d15y.onrender.com/docs

Try the interactive API documentation to explore all endpoints and test the functionality directly in your browser.

## API Preview

![Swagger UI](https://github.com/python-webdev/DiceRollingGame/blob/fa196ddb633ea31225e482776ebce3e0ca55ae15/swagger-ui-screenshot.png)

The interactive Swagger UI provides a comprehensive overview of all available endpoints, organized by functionality:
- **Sessions**: Create, manage, and delete game sessions
- **Roll**: Execute dice rolls with different game modes and dice types
- **History**: Access, export, and manage roll history
- **Stats**: View detailed session statistics and analytics

---

## What This Project Demonstrates 

- **Clean Architecture**: Domain-driven design with proper separation of concerns
- **RESTful API Development**: FastAPI with comprehensive endpoint design and validation
- **Database Design**: SQLite with repository pattern for data persistence
- **Testing Strategy**: Pytest with unit/integration tests and CI/CD pipeline (95%+ coverage)
- **DevOps Practices**: Docker containerization, GitHub Actions CI, and production deployment
- **Code Quality**: Type hints (MyPy), linting (Ruff), formatting (Black), and comprehensive error handling
- **Documentation**: API docs, architectural documentation, and developer onboarding guides

## Why This Project Exists

Most beginner projects rely on global variables or in-memory state, which breaks in production APIs.

This project solves real-world challenges by:

- **Session-based state management**: Isolating game data per user session
- **Scalable architecture**: Service and repository layers for maintainable code  
- **Production readiness**: Proper error handling, validation, and testing
- **Industry standards**: Following enterprise development patterns and practices

---

## Key Features

- **Session-based gameplay**: No shared global state, fully isolated user sessions
- **RESTful API**: FastAPI with comprehensive endpoint design and validation 
- **SQLite persistence**: Repository pattern for clean data access
- **Service layer architecture**: Business logic separated from infrastructure
- **Comprehensive testing**: 95%+ coverage with pytest and CI/CD pipeline
- **Docker deployment**: Production-ready containerization
- **Code quality assurance**: Automated linting, formatting, and type checking

---

## Architecture & Technical Design

Follows **clean architecture principles** with clear separation of concerns:

- **API Layer** (`api/`): FastAPI routes, request validation, and HTTP handling
- **Service Layer** (`services/`): Business logic and orchestration  
- **Repository Layer** (`storage/`): Database operations and data access
- **Domain Layer** (`domain/`): Core models, business rules, and constants
- **CLI Interface** (`cli/`): Command-line user interface

## Architecture Diagram

```text
Client
  ↓
FastAPI Routes
  ↓
Services
  ↓
Repositories
  ↓
SQLite

Services
  ↓
Domain Models / Game Logic
```

The API layer handles HTTP requests and validation.
Services coordinate gameplay rules and session workflows.
Repositories isolate database access.
Domain models keep game state and rules separate from infrastructure.

```
src/dice_game/
├── api/               # REST API layer (FastAPI)
│   ├── app.py        # Application factory and configuration
│   ├── schemas.py    # Pydantic models for request/response validation
│   └── routes/       # API endpoint definitions
├── cli/              # Command-line interface
│   ├── ui.py        # User input handling and menu logic
│   └── printing.py  # Output formatting and display
├── domain/           # Core business logic and models
│   ├── models.py    # Domain entities and value objects
│   ├── modes.py     # Game mode definitions
│   ├── config.py    # Configuration management
│   └── constants.py # Game constants and enums
├── services/         # Application services and orchestration
│   ├── logic.py     # Core game logic implementation
│   ├── simulation.py # Monte Carlo simulation engine
│   └── game_session_service.py # Session management
└── storage/          # Data persistence layer
    ├── connection.py # Database connection management
    ├── roll_repository.py # Roll data operations
    └── session_repository.py # Session data operations
```

### Design Patterns Implemented
- **Factory Pattern**: Application and service creation
- **Repository Pattern**: Data access abstraction
- **Command Pattern**: CLI action handling
- **Strategy Pattern**: Game mode implementations
- **Dependency Injection**: Loose coupling between layers

---

## API Endpoints

### Session Management
- `POST /sessions` - Create new game session
- `GET /sessions/{game_session_id}` - Get session details
- `DELETE /sessions/{game_session_id}` - Delete session

### Game Actions  
- `POST /sessions/{game_session_id}/roll` - Roll dice in session
- `GET /sessions/{game_session_id}/stats` - Get session statistics

### History & Data
- `GET /sessions/{game_session_id}/history` - Get roll history (paginated)
- `DELETE /sessions/{game_session_id}/history` - Clear session history
- `GET /sessions/{game_session_id}/history/export` - Export session data to CSV

### Interactive Documentation
Visit `http://localhost:8000/docs` for comprehensive API documentation with interactive testing.

## cURL Examples

Create a session:

```bash
curl -X POST https://dice-game-api-d15y.onrender.com/sessions
```

Then use the returned `game_session_id` in these requests:

### Roll Dice (Various Game Modes)

**Classic Mode:**
```bash
curl -X POST "https://dice-game-api-d15y.onrender.com/sessions/<GAME_SESSION_ID>/roll" \
  -H "Content-Type: application/json" \
  -d '{"mode":"classic","dice_type":"D6","num_dice":2}'
```

**Lucky Mode:**
```bash
curl -X POST "https://dice-game-api-d15y.onrender.com/sessions/<GAME_SESSION_ID>/roll" \
  -H "Content-Type: application/json" \
  -d '{"mode":"lucky","dice_type":"D6","num_dice":2}'
```

**Risk Mode:**
```bash
curl -X POST "https://dice-game-api-d15y.onrender.com/sessions/<GAME_SESSION_ID>/roll" \
  -H "Content-Type: application/json" \
  -d '{"mode":"risk","dice_type":"D6","num_dice":2}'
```

**With Different Dice Types:**
```bash
# D8 dice
curl -X POST "https://dice-game-api-d15y.onrender.com/sessions/<GAME_SESSION_ID>/roll" \
  -H "Content-Type: application/json" \
  -d '{"mode":"classic","dice_type":"D8","num_dice":3}'

# D12 dice
curl -X POST "https://dice-game-api-d15y.onrender.com/sessions/<GAME_SESSION_ID>/roll" \
  -H "Content-Type: application/json" \
  -d '{"mode":"classic","dice_type":"D12","num_dice":1}'
```

### Session Management

**Get Session Details:**
```bash
curl "https://dice-game-api-d15y.onrender.com/sessions/<GAME_SESSION_ID>"
```

**Get Session Statistics:**
```bash
curl "https://dice-game-api-d15y.onrender.com/sessions/<GAME_SESSION_ID>/stats"
```

**Delete Session:**
```bash
curl -X DELETE "https://dice-game-api-d15y.onrender.com/sessions/<GAME_SESSION_ID>"
```

### History Management

**Get Roll History (Paginated):**
```bash
# Default pagination
curl "https://dice-game-api-d15y.onrender.com/sessions/<GAME_SESSION_ID>/history"

# With pagination parameters
curl "https://dice-game-api-d15y.onrender.com/sessions/<GAME_SESSION_ID>/history?page=1&limit=10"
```

**Export Roll History to CSV:**
```bash
curl "https://dice-game-api-d15y.onrender.com/sessions/<GAME_SESSION_ID>/history/export" \
  -o "dice_game_export.csv"
```

**Clear Session History:**
```bash
curl -X DELETE "https://dice-game-api-d15y.onrender.com/sessions/<GAME_SESSION_ID>/history"
```

### Complete Workflow Example

```bash
# 1. Create a new session
SESSION_RESPONSE=$(curl -s -X POST https://dice-game-api-d15y.onrender.com/sessions)
SESSION_ID=$(echo $SESSION_RESPONSE | grep -o '"game_session_id":"[^"]*' | grep -o '[^"]*$')

# 2. Roll dice multiple times
curl -X POST "https://dice-game-api-d15y.onrender.com/sessions/$SESSION_ID/roll" \
  -H "Content-Type: application/json" \
  -d '{"mode":"classic","dice_type":"D6","num_dice":2}'

curl -X POST "https://dice-game-api-d15y.onrender.com/sessions/$SESSION_ID/roll" \
  -H "Content-Type: application/json" \
  -d '{"mode":"lucky","dice_type":"D8","num_dice":3}'

# 3. Check stats
curl "https://dice-game-api-d15y.onrender.com/sessions/$SESSION_ID/stats"

# 4. View history
curl "https://dice-game-api-d15y.onrender.com/sessions/$SESSION_ID/history"

# 5. Export data
curl "https://dice-game-api-d15y.onrender.com/sessions/$SESSION_ID/history/export" \
  -o "session_${SESSION_ID}_export.csv"
```

---

## Game Modes

### Classic Mode
Traditional dice rolling with balanced scoring:
- **Win**: `total > 10` → +5 points
- **Draw**: `total = 10` → 0 points  
- **Lose**: `total < 10` → -3 points

### Lucky Mode
Features special doubles mechanic for bonus opportunities:
- **Doubles Bonus**: All dice match → +10 points + extra turn
- **Win**: `total > 10` → +5 points
- **Draw**: `total = 10` → 0 points
- **Lose**: `total < 10` → -3 points

### Risk Mode
High-stakes gameplay with increased penalty threshold:
- **Win**: `total > 10` → +5 points
- **Draw**: `total 7-10` → 0 points
- **Risky Loss**: `total < 7` → -3 points

---

## Statistics & Analytics

The application provides comprehensive analytics:

### Session Statistics
- Current point balance and session status
- Roll count and success rates
- Average roll values and distributions

### Historical Analytics  
- Best and worst rolls across all sessions
- Outcome distribution by game mode  
- Performance trends over time
- Dice type effectiveness analysis

### Simulation Engine
- Monte Carlo analysis for strategy optimization
- Probability distribution modeling
- Risk assessment for different configurations

---

## Quick Start Guide

### Prerequisites
- **Python 3.10+** (supports Python 3.11, 3.12, 3.13)
- **pip** (Python package manager)
- **Docker** (optional, for containerized deployment)

### Installation & Setup

```bash
# Install the package and dependencies
pip install -e .
# For development (includes testing tools)
pip install -e ".[dev]"
# Run the API with auto-reload
uvicorn dice_game.api.app:app --reload
# Production server
uvicorn dice_game.api.app:app --host 0.0.0.0 --port 8000
```

## Usage

### Command Line Interface
Start the interactive CLI game:
```bash
python -m dice_game
```

**Available CLI Commands:**
- `(r)oll` - Roll dice with selected configuration
- `(h)istory` - Browse roll history with filtering and pagination  
- `s(t)ats` - View comprehensive statistics
- `(s)imulate` - Run Monte Carlo simulations
- `(e)xport` - Export roll history to CSV
- `(c)lear` - Clear roll history
- `(q)uit` - Exit game

### Docker Deployment

**Quick Start:**
```bash
# Build and run with Docker Compose (Recommended)
docker-compose up -d

# For development with auto-reload  
docker-compose --profile dev up

# View application logs
docker-compose logs -f
```

**Manual Docker Commands:**

```bash
# Build the Docker image
docker build -t dice-game-api .

# Run the containerized API
docker run -p 8000:8000 dice-game-api

# Run in background
docker run -d -p 8000:8000 dice-game-api
```

**Docker Compose (Recommended):**
```bash
# Production deployment
docker-compose up -d

# Development with auto-reload
docker-compose --profile dev up

# View logs
docker-compose logs -f
```

**Container Management:**
```bash
# View running containers
docker ps

# Stop container
docker stop <container_id>

# View container logs
docker logs <container_id>
```

---

## Testing & Quality Assurance

Run the comprehensive test suite:
```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=src/dice_game --cov-report=html

# Run specific test module
pytest tests/test_api_sessions.py -v
```

### CI/CD Pipeline (GitHub Actions)

Automated quality assurance and deployment:
- **Code Quality**: Ruff (linting), Black (formatting), MyPy (type checking)
- **Testing**: Pytest with 95%+ coverage across Python 3.11, 3.12, 3.13
- **Containerization**: Docker build validation and functionality tests
- **Deployment**: Automated container registry publishing

---

## Development & Architecture Patterns

### Enterprise Development Practices
- **Domain-Driven Design**: Core business logic isolated from infrastructure  
- **Repository Pattern**: Clean data access abstraction
- **Dependency Injection**: Loose coupling between layers
- **Error Handling**: Comprehensive exception handling with proper HTTP status codes
- **Containerization**: Docker-first deployment strategy
- **API-First Design**: OpenAPI specification with interactive documentation

---

## Version History & Evolution

- **v2.0.0** (Current) - Complete architectural rewrite with:
  - REST API implementation using FastAPI
  - Clean architecture with proper separation of concerns
  - Persistent session management with SQLite
  - Comprehensive testing suite and CI/CD pipeline
  - Docker containerization and production deployment
  
- **v0.1.x** (Legacy) - Initial CLI-only implementation with single-file architecture

---

## Contributing

1. **Fork** the repository
2. **Create** feature branch: `git switch -C feature-name`
3. **Implement** changes with comprehensive tests
4. **Validate** with full test suite: `pytest --cov=src/dice_game`
5. **Submit** pull request with clear description

### Development Setup
```bash
# Install with development dependencies
pip install -e ".[dev]"

# Run quality checks
ruff check .           # Linting  
black --check .        # Code formatting
mypy .                 # Type checking
pytest --cov=src/dice_game  # Testing with coverage
```
