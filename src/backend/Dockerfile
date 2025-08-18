# Use the Chainguard Python image as a builder
FROM cgr.dev/chainguard/python:latest-dev AS builder

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN python -m venv /app/venv && \
    /app/venv/bin/pip install --no-cache-dir -r requirements.txt


# Use the Chainguard Python image for the runtime
FROM cgr.dev/chainguard/python:latest-dev

# Set the working directory
WORKDIR /app

# Copy the virtual environment from the builder stage
COPY --from=builder /app/venv ./venv

# Copy the application code
COPY src .

USER root
# Set the entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

USER nonroot

ENTRYPOINT ["/entrypoint.sh"]

# Expose the port
EXPOSE 8000