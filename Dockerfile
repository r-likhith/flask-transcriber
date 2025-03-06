# Use Python 3.10 (recommended for latest supabase library compatibility)
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy all files into the container
COPY . /app

# Install dependencies
RUN pip install -r requirements.txt

# Expose port (Render will map this to its internal port)
EXPOSE 10000

# Command to run your Flask app
CMD ["python", "main.py"]
