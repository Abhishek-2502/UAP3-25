# Use Python 3.11 base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies (including Tesseract-OCR)
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . /app

# Copy locally downloaded Python dependencies
COPY wheelhouse /app/wheelhouse

# Install dependencies from wheelhouse (if available)
RUN pip install --no-index --find-links=/app/wheelhouse -r requirements.txt

# Install the package
RUN pip install .

# Expose FastAPI default port
EXPOSE 9001

# Start the FastAPI server
CMD ["realtime_va"]
