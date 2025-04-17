# --- Base Image ---
# Use an official Python runtime as a parent image
# Choose a specific version for reproducibility
FROM python:3.10-slim

# --- Environment Variables ---
# Set the working directory in the container
WORKDIR /app

# Prevent Python from writing pyc files to disc (optional)
ENV PYTHONDONTWRITEBYTECODE 1
# Ensure Python output is sent straight to terminal (useful for logging)
ENV PYTHONUNBUFFERED 1

# --- Install System Dependencies (if any) ---
# Example: RUN apt-get update && apt-get install -y --no-install-recommends some-package && rm -rf /var/lib/apt/lists/*
# Usually not needed for a basic FastAPI app unless you have specific C libraries

# --- Install Python Dependencies ---
# Copy the requirements file into the container
COPY ./app/requirements.txt /app/requirements.txt

# Install pip dependencies
# --no-cache-dir: Disables the cache, reducing image size
# --upgrade pip: Ensures the latest pip is used
# -r requirements.txt: Installs packages listed in the file
RUN pip install --no-cache-dir --upgrade pip -r requirements.txt

# --- Copy Application Code ---
# Copy the rest of the application code (the 'app' directory) into the container
COPY ./app /app

# --- Expose Port ---
# Expose the port the app runs on (should match Uvicorn command)
EXPOSE 8080

# --- Command ---
# Command to run the application using Uvicorn
# Use 0.0.0.0 as host to accept connections from outside the container
# --port 8080 matches the EXPOSE instruction
# main:app refers to the 'app' instance in the 'main.py' file
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]