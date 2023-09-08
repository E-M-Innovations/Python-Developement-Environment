# Base image for the Docker container.
ARG BASE_IMAGE=python:3.11.5-alpine3.18
FROM ${BASE_IMAGE}
#   ---------------

# Fill in for the argument parameters 
# -----------------------------------
# Poetry Configuration
# Version of the Poetry package manager to use.
ARG POETRY_VERSION=1.6.1
# Environment configuration (e.g., "1.5.6"(number) or "production"). 
ARG YOUR_ENV=production

# Set environment variables
# ---------------------------
# - `YOUR_ENV=$YOUR_ENV`: Sets container-specific configurations via the `$YOUR_ENV` variable.
# - `PYTHONFAULTHANDLER=1`: Enables detailed tracebacks for Python errors.
# - `PYTHONUNBUFFERED=1`: Disables Python's output buffering for immediate container output.
# - `PYTHONHASHSEED=random`: Generates random hash seeds to diversify hash values between runs.
# - `PIP_NO_CACHE_DIR=off`: Disables pip package caching for downloads.
# - `PIP_DISABLE_PIP_VERSION_CHECK=on`: Suppresses pip version checks to avoid update checks.
# - `PIP_DEFAULT_TIMEOUT=100`: Sets a default pip operation timeout in seconds.
# - `POETRY_VERSION=${POETRY_VERSION}`: Sets the Poetry version via the `$POETRY_VERSION` variable.
ENV YOUR_ENV=$YOUR_ENV \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=${POETRY_VERSION}

# System deps: lock poetry version 
RUN pip install "poetry==${POETRY_VERSION}"

# Copy only requirements to cache them in docker layer
WORKDIR /code
COPY pyproject.toml /code/
RUN if [ -f poetry.lock ]; then \
      COPY poetry.lock /code/; \
    fi

# Project initialization:
# ---------------------------
# If $YOUR_ENV is "production", add "--no-dev" to poetry install, which skips dev dependencies. 
# This is useful for deploying production apps. Flags --no-interaction and --no-ansi ensure non-interactive, color-free install.
RUN poetry config virtualenvs.create false \
  && poetry install $(test "$YOUR_ENV" == production && echo "--no-dev") --no-interaction --no-ansi

# Check if Cython is a dependency and install GCC if needed
RUN poetry show cython >/dev/null 2>&1 && \
    apk update && apk add build-base || true

# Creating folders, and files for a project:
COPY src/ /code/

# CMD or ENTRYPOINT directive to run the Python script
# CMD ["python", "PY_example.py"]

# # Compile the C file
# RUN gcc -o C_example C_example.c

# # CMD or ENTRYPOINT directive to run the compiled C program
# CMD ["./C_example"]