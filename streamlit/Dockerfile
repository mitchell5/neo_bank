FROM python:3.12.8-slim

#Do not use env as this would persist after the build and would impact your containers, children images
ARG DEBIAN_FRONTEND=noninteractive

# force the stdout and stderr streams to be unbuffered.
ENV PYTHONUNBUFFERED=1

#Set up workdir in container, it does not exist yet
WORKDIR /app

# Copy dependency files first
COPY ./pyproject.toml  ./pyproject.toml
COPY ./poetry.lock  ./poetry.lock

# Copy your application code
COPY ./pages ./pages

# Install Poetry and dependencies
RUN apt-get update \
    && apt-get -y upgrade \
    && pip3 install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry install --only main \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


# Copy your credentials (optional - see alternative below)
COPY ./sacred-choir-466017-s9-c7fdbf18a028.json /app/sacred-choir-466017-s9-c7fdbf18a028.json

EXPOSE 8501

#command
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
