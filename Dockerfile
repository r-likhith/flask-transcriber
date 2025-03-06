# Use Python base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy files
COPY . /app

# Install dependencies
RUN pip install -r requirements.txt

# Expose port
EXPOSE 10000

# Run the app
CMD ["python", "main.py"]
# Dockerfile for Render
