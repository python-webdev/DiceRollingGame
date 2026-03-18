# Dice Rolling Game

A modern, feature-rich dice rolling application with dual interfaces (CLI and REST API), persistent game sessions, comprehensive statistics, and clean architecture design.

## Features

### Core Gameplay
- **Three Game Modes**: Classic, Lucky, and Risk with distinct scoring mechanics
- **Six Dice Types**: D4, D6, D8, D10, D12, D20 support
- **Dynamic Setup**: Roll 2+ dice per turn with customizable configurations
- **Point System**: Gain/lose points based on outcomes and game mode rules
- **Extra Turns**: Lucky mode grants bonus turns for doubles

### Dual Interface Design
- **Interactive CLI**: Rich terminal interface with menus, pagination, and real-time stats
- **REST API**: Full-featured FastAPI web service with OpenAPI documentation
- **Statistics Dashboard**: Live tracking of rolls, averages, best scores, and more
- **Persistent Storage**: SQLite database with game session management

### Advanced Features
- **Game Sessions**: Create, manage, and track multiple independent sessions
- **Roll History**: Complete audit trail with filtering, pagination, and export
- **Statistics Engine**: Comprehensive analytics and performance metrics
- **Simulation Mode**: Monte Carlo simulations for strategy analysis
- **CSV Export**: Historical data export for external analysis

## Architecture

The application follows clean architecture principles with clear separation of concerns:

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

### Layer Dependencies
- **API Layer** → Services → Domain
- **CLI Layer** → Services → Domain  
- **Services** → Storage → Domain
- **Storage** → Domain (models only)

## Installation & Setup

### Prerequisites
- Python 3.10+
- pip (Python package manager) 
- Docker (optional, for containerized deployment)

### Option 1: Local Python Installation
```bash
# Install the package and dependencies
pip install -e .

# For development (includes testing tools)
pip install -e ".[dev]"
```

### Option 2: Docker Container
```bash
# Build the Docker image
docker build -t dice-game-api .

# Run the containerized API
docker run -p 8000:8000 dice-game-api

# Run in background
docker run -d -p 8000:8000 dice-game-api
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

### REST API Server

**Local Development:**
```bash
# Development server with auto-reload
uvicorn dice_game.api.app:app --reload

# Production server
uvicorn dice_game.api.app:app --host 0.0.0.0 --port 8000
```

**Docker Container:**
```bash
# Build and run containerized API
docker build -t dice-game-api .
docker run -p 8000:8000 dice-game-api

# Or run pre-built image in background
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

Visit `http://localhost:8000/docs` for interactive API documentation.

**Container Management:**
```bash
# View running containers
docker ps

# Stop container
docker stop <container_id>

# View container logs
docker logs <container_id>
```

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

## Statistics Tracking

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

## Testing

Run the comprehensive test suite:
```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=src/dice_game --cov-report=html

# Run specific test module
pytest tests/test_api_sessions.py -v
```

## Deployment

### Docker Containerization
The application is fully containerized with Docker for easy deployment:

**Features:**
- **Optimized Docker build** - Multi-stage build with layer caching
- **Security focused** - .dockerignore excludes sensitive files
- **Fast builds** - Minimal build context (5.36kB)
- **Production ready** - Uvicorn ASGI server with proper configuration

**Docker Commands:**
```bash
# Build optimized image
docker build -t dice-game-api .

# Run with port mapping
docker run -p 8000:8000 dice-game-api

# Production deployment
docker run -d --name dice-api -p 8000:8000 --restart unless-stopped dice-game-api
```

### CI/CD Pipeline
Automated testing and Docker builds via GitHub Actions:
- **Code quality** - Ruff linting, Black formatting, MyPy type checking
- **Multi-version testing** - Python 3.11, 3.12, 3.13 compatibility  
- **Docker validation** - Container build and API functionality tests
- **Coverage reporting** - Comprehensive test coverage analysis

## Development

### Project Structure
- **Domain-Driven Design**: Core business logic isolated from infrastructure
- **Repository Pattern**: Clean data access abstraction
- **Dependency Injection**: Loose coupling between layers
- **Error Handling**: Comprehensive exception handling with proper HTTP status codes
- **Containerization**: Docker-first deployment strategy

### Key Design Patterns
- **Factory Pattern**: Application and service creation
- **Repository Pattern**: Data access abstraction
- **Command Pattern**: CLI action handling
- **Strategy Pattern**: Game mode implementations

## Requirements

### Runtime Dependencies
- `fastapi` - Modern web framework for building APIs
- `uvicorn` - ASGI web server implementation
- `pydantic` - Data validation using Python type hints

### Development Dependencies  
- `pytest` - Testing framework
- `pytest-cov` - Coverage reporting

## License

This project is available under the MIT License.

## Contributing

1. Fork the repository
2. Create a feature branch: `git switch -C feature-name`
3. Make your changes with tests
4. Run the test suite: `pytest`
5. Submit a pull request

## Version History

- **v2.0.0** - Complete architectural rewrite with REST API, clean architecture, and persistent sessions
- **v1.x** - Legacy single-file CLI implementation

- Dice count must be a valid number ≥ 2
- Game mode must be one of: classic, lucky, risk
- Dice type must be one of: D4, D6, D8, D10, D12, D20
- Main menu accepts only (r)oll (h)istory s(t)ats (s)imulate (e)xport to CSV (c)lear history (q)uit: 
- Invalid inputs prompt retry with helpful messages
