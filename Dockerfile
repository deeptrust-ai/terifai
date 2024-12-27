FROM python:3.12-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ADD . /app
WORKDIR /app

RUN uv pip install --no-cache --system -r requirements.lock

RUN uv pip install --no-cache --system torch

# Install models
RUN python ./backend/install_deps.py

# Expose the port the app runs on
EXPOSE 7860

# Command to run the application
CMD ["python", "-m", "backend.server"]
