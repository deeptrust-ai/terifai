FROM python:3.12-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ADD . /app
WORKDIR /app

# Install dependencies
RUN uv pip install --no-cache --system -r requirements.lock
RUN uv pip install --no-cache --system torch torchaudio

# Install the backend package in development mode
RUN pip install -e .

# Install models
RUN python -m backend.install_deps

# Expose the port the app runs on
EXPOSE 7860

# Command to run the application
CMD ["python", "-m", "backend.server"]
