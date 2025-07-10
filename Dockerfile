# Use an official Python image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /usr/src/app

# Copy requirements first for better layer caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application
COPY app/ ./app/

# Set environment variables if needed (optional)
ENV PYTHONUNBUFFERED=1

# Expose port if your server listens on one (example: 8000)
EXPOSE 8000

# Set the default command to run your server
CMD ["python", "-m", "app.main"]