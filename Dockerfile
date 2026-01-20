FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies (optional but safe)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency list
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source code
COPY app/ ./app/

# Cloud Run uses port 8080
ENV PORT=8080
EXPOSE 8080

# Start FastAPI with Uvicorn (WebSocket compatible)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
