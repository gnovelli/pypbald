# Base image
FROM python:2.7-slim

# Install dependencies
RUN sed -i 's/deb.debian.org/archive.debian.org/g' /etc/apt/sources.list && \
    sed -i 's|security.debian.org|archive.debian.org|g' /etc/apt/sources.list && \
    sed -i '/buster-updates/d' /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y --allow-unauthenticated build-essential default-libmysqlclient-dev libpcap-dev && \
    pip install mysqlclient dpkt pypcap

# Set working directory
WORKDIR /usr/src/app/src

# Copy application code
COPY . /usr/src/app/

# Create logs directory
RUN mkdir -p /usr/src/app/logs

# Command to run the application
CMD ["python", "main.py"]
