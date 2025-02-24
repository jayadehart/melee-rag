# Use a Python base image
FROM python:3.9-alpine

# Set the working directory
WORKDIR /app

# Install system dependencies (if needed)
RUN apk add --no-cache gcc musl-dev libffi-dev

# Install pip-tools globally
RUN pip install --no-cache-dir pip-tools

# Copy only the requirements.in first (for caching benefits)
COPY requirements.in .

# Compile the requirements.txt
RUN pip-compile --generate-hashes --output-file=requirements.txt requirements.in

# Install dependencies from compiled requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Define the command to run the application
CMD ["python", "create_db.py"]
