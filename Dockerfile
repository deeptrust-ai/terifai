# Use the official Python image as a base
FROM python:3.12.2-slim

# Accept the build argument
ARG wheel

# Update the package list and pip
RUN apt-get update && \
  apt-get install -y --no-install-recommends && \
  rm -rf /var/lib/apt/lists/*
RUN python -m pip install --upgrade pip

# Set the working directory
WORKDIR /app

# Copy the wheel file and install it
COPY ./dist/$wheel /app/$wheel
RUN pip install --no-cache-dir --upgrade /app/$wheel

# Copy the source code into the image
COPY ./src /app/src

# Expose the port the app runs on
EXPOSE 7860

# Command to run the application
CMD python -m src.server
