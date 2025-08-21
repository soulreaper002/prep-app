# Dockerfile for deploying a Python web application to Google Cloud Run
# This Dockerfile sets up a Python environment, installs dependencies, and runs the application using gunicorn
# Use an official lightweight Python image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Command to run the application using gunicorn
# It listens on port 8080, which Cloud Run expects
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]