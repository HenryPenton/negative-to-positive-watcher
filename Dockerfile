FROM python:3.12-slim

LABEL maintainer="Film Negative Converter"
LABEL description="Watches a folder for image negatives and converts them to positives"

# Install Python dependencies
RUN pip install --no-cache-dir Pillow

# Create watch and output directories
RUN mkdir -p /watch /output

# Copy the watcher script
COPY watcher.py /app/watcher.py
RUN chmod +x /app/watcher.py

# Set working directory
WORKDIR /app

# Environment variables (can be overridden)
ENV WATCH_DIR=/watch
ENV OUTPUT_DIR=/output
ENV POLL_INTERVAL=5

# Volumes for input and output
VOLUME ["/watch", "/output"]

# Run the watcher
CMD ["python", "-u", "watcher.py"]
