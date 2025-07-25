# Base image
FROM python:3.12-slim

#Do not use env as this would persist after the build and would impact your containers, children images
ARG DEBIAN_FRONTEND=noninteractive

# force the stdout and stderr streams to be unbuffered.
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy project files (adjust as needed)
COPY ./pyproject.toml ./poetry.lock ./

# Install pip and Poetry
RUN pip install --upgrade pip \
    && pip install --no-cache-dir poetry

# Configure Poetry to not use virtualenvs
RUN poetry config virtualenvs.create false

# Install project dependencies
RUN poetry install --no-interaction --no-ansi

# Copy remaining source code (app.py and modules)
COPY ./app ./

# Set env var for credentials (will be passed during runtime)
ENV GOOGLE_APPLICATION_CREDENTIALS="/app/credentials.json"

# Expose port
EXPOSE 8501

# Run the app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
