# Base image
FROM python:3.12-slim

# Install dependencies
RUN pip install --no-cache-dir requests pandas numpy kubernetes

# Copy the Python script into the container
COPY cpu_anomaly.py /app/cpu_anomaly.py

# Set working directory
WORKDIR /app

# Run the script
CMD ["python", "cpu_anomaly.py"]
