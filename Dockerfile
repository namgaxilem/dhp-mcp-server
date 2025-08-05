FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies (optional but useful for full FastAPI + Uvicorn stack)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project
COPY . .

# Make the script executable
RUN chmod +x ./start.sh

# Expose ports if needed (example: 8000-9000+)
EXPOSE 8080

# Set entrypoint to the bash script
ENTRYPOINT ["./start.sh"]
