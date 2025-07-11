# Use the official Python image
FROM python:3.10

# Install system dependencies required for OpenCV
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the model file and application files
# COPY static/models/best.pt /app/static/models/best.pt
COPY . /

# Expose port 8080
EXPOSE 8080

# Start the app using Gunicorn with increased timeout and asynchronous workers
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--timeout", "120", "--worker-class", "gevent", "app:app"]