# Dockerfile for Flask YOLO App
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy necessary files
COPY . /app

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Command to run the app
CMD ["python", "flask_yolo_post.py"]