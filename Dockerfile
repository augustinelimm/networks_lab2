# Use a prebuilt FastAPI-optimized image
FROM tiangolo/uvicorn-gunicorn:python3.11

# Set metadata
LABEL maintainer="Sebastian Ramirez <tiangolo@gmail.com>"

# Set working directory inside the container
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files
COPY . .

# Expose the FastAPI port
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]