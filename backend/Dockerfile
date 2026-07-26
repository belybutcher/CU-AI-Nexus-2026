# --- CU AI Nexus backend image ---
FROM python:3.12-slim

# Prevents Python from writing .pyc files and buffering stdout/stderr (better logs).
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# System dependencies needed by Pillow / psycopg2.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Storage directories that AI/report outputs are written to.
RUN mkdir -p app/storage/uploads app/storage/enhanced app/storage/heatmaps app/storage/reports models

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
