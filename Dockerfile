# Use an official, lightweight Python runtime as a parent image
FROM python:3.12-slim

# Set system environment variables to prevent Python from writing pyc files and buffering stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the functional workspace directory inside the container
WORKDIR /app

# Copy the requirements file into the container image layer
COPY requirements.txt .

# Install the universal open-source biological library footprints
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the 9-stage source code, tests, and master runner into the image
COPY run_pipeline.py .
COPY src/ ./src/
COPY tests/ ./tests/

# Establish standard execution directories so the container doesn't crash on mounting paths
RUN mkdir -p data/patient_samples data/output data/reports data/visuals data/validation data/manufacturing data/exports

# Command to execute the master 9-stage pipeline by default when the container fires up
CMD ["python", "run_pipeline.py"]
