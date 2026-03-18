FROM python:3.13-slim

WORKDIR /app

COPY pyproject.toml ./
COPY README.md ./
COPY src ./src

RUN python -m pip install --upgrade pip && \
  pip install -e .

EXPOSE 8000

CMD ["uvicorn", "dice_game.api.app:app", "--host", "0.0.0.0", "--port", "8000"]