FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies for ML and PDF processing
# Install system dependencies including BLAS and LAPACK for SciPy/ML
RUN apt-get update && apt-get install -y \
    build-essential \
    libopenblas-dev \
    liblapack-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy and install dependencies first (faster builds)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend code
COPY app/ ./app/

# Copy the frontend folder (Critical for your HTML to load!)
COPY frontend/ ./frontend/

# Set environment variables
ENV PORT=8080
EXPOSE 8080

# Start FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
