# Base image
FROM python:3.11-slim

# Install dependencies
RUN apt-get update && \
    apt-get install -y build-essential default-libmysqlclient-dev libpcap-dev && \
    pip install mysql-connector-python dpkt pypcap && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /usr/src/app/src

# Copy application code
COPY . /usr/src/app/

# Create logs directory
RUN mkdir -p /usr/src/app/logs

# Command to run the application
CMD ["python3", "main.py"]
