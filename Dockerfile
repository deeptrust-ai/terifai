# Use the official Python image as a base
FROM python:3.12.2-slim

# Accept the build argument
ARG WHEEL

# Update the package list and pip
RUN apt-get update && \
  apt-get install -y --no-install-recommends && \
  rm -rf /var/lib/apt/lists/*
RUN python -m pip install --upgrade pip

# Install torch and torchaudio
RUN pip install --no-cache-dir torch torchaudio

# Set the working directory
WORKDIR /app

# Copy the source code into the image
COPY ./src /app/src

# Install models
RUN python ./src/install_deps.py

# Copy the wheel file and install it
COPY ./dist/$WHEEL /app/$WHEEL
RUN pip install --no-cache-dir --upgrade /app/$WHEEL

# Expose the port the app runs on
EXPOSE 7860

# Set the PYTHONPATH environment variable
ENV PYTHONPATH="src"

# Command to run the application
CMD python -m src.server
