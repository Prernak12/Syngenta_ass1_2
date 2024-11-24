# Stage 1: Build stage
FROM python:3.10-slim AS base

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies in a virtual environment for optimization
COPY requirements.txt .
RUN python -m venv /venv && /venv/bin/pip install --upgrade pip && /venv/bin/pip install -r requirements.txt

# Stage 2: Final stage
FROM python:3.10-slim

# Set environment variables
ENV VIRTUAL_ENV=/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy only necessary files
COPY --from=base /venv /venv
COPY main.py chunks.py wine_data_filter.py ./
COPY Mall_Customers.csv winequality-red.csv ./

# Expose port 8000 for FastAPI
EXPOSE 8000

# Run FastAPI app with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
