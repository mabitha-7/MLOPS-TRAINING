# Stage 1: Build React frontend
FROM node:18-alpine AS frontend-builder

WORKDIR /app/client

# Copy package files
COPY client/package.json client/package-lock.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY client/src ./src
COPY client/public ./public

# Build React app
RUN npm run build

# Stage 2: Python backend with ML models
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies for OpenCV and other packages
RUN apt-get update && apt-get install -y \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy Python requirements and install dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY server ./server
COPY image_detection ./image_detection
COPY video_processing ./video_processing
COPY model ./model
COPY *.py .
COPY *.yaml .
COPY *.pt .

# Copy pre-built React frontend from stage 1
COPY --from=frontend-builder /app/client/build ./client/build

# Expose ports
EXPOSE 5000 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/ || exit 1

# Set environment variables
ENV FLASK_APP=server/app.py
ENV PYTHONUNBUFFERED=1

# Run the Flask backend
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]
