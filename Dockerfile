# Base image
FROM python:3.10

# Set environment variables to avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install required system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry

# Set workdir
WORKDIR /app

# Copy project files
COPY pyproject.toml poetry.lock ./
RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR

COPY . .

# Install dependencies
RUN poetry install --without dev --no-root

# Run the application
CMD ["poetry", "run", "python", "create_db.py"]
