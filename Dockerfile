# (Keep the version in sync with the node install below)
FROM node:20 as frontend

# Install front-end dependencies.
COPY package.json package-lock.json tsconfig.json webpack.config.js ./
RUN npm ci --no-optional --no-audit --progress=false

# Compile static files
COPY ./climtech/static/ ./climtech/static/
RUN npm run build:prod


# Build Python app - this stage is a common base for the prod and dev stages
FROM ghcr.io/osgeo/gdal:ubuntu-small-3.10.0 AS backend

ARG POETRY_VERSION=1.8.3
ARG UID
ENV UID=${UID:-1000}
ARG GID
ENV GID=${GID:-1000}

ENV DJANGO_SETTINGS_MODULE=climtech.settings.production \
    GUNICORN_CMD_ARGS="--max-requests 1200 --max-requests-jitter 50 --access-logfile -" \
    PATH=/home/climtech/.local/bin:/venv/bin:$PATH \
    PORT=8000 \
    PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV=/venv \
    WEB_CONCURRENCY=3 \
    POSTGRES_VERSION=15

# Install operating system dependencies.
RUN apt-get update --yes --quiet \
    && apt-get install -y --no-install-recommends \
    build-essential \
    lsb-release \
    ca-certificates \
    gnupg2 \
    curl \
    cron \
    tini \
    libpq-dev \
    libgeos-dev \
    imagemagick \
    libmagic1 \
    libcairo2-dev \
    libpangocairo-1.0-0 \
    libffi-dev \
    python3-pip \
    python3-dev \
    python3-venv \
    inotify-tools \
    poppler-utils \
    git \
    gosu \
    && echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list \
    && curl --silent https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - \
    && apt-get update \
    && apt-get install -y apt-transport-https rsync libmagickwand-dev unzip postgresql-client-$POSTGRES_VERSION \
    jpegoptim pngquant gifsicle libjpeg-progs webp && \
    rm -rf /var/lib/apt/lists/*

ENV DOCKER_COMPOSE_WAIT_VERSION=2.12.1

# Install docker-compose wait
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/$DOCKER_COMPOSE_WAIT_VERSION/wait /wait
RUN chmod +x /wait
WORKDIR /app
EXPOSE 8000

# Create a virtual environment and install Poetry
RUN python3 -m venv /venv \
    && pip3 install poetry==$POETRY_VERSION

# Create a non-root application user.
# RUN groupadd --gid $GID --force climtech \
#     && useradd --create-home --uid $UID -g climtech climtech
RUN chown --recursive $UID:$GID /app /venv


# This stage builds the image that will run in production
FROM backend as prod

# Switch to application user
USER $UID:$GID

# Install production dependencies
COPY --chown=$UID:$GID pyproject.toml poetry.lock ./
RUN poetry install --only main --no-root

# Copy in application code and install the root package
COPY --chown=$UID:$GID . .
RUN poetry install --only-root



# Collect static files
RUN SECRET_KEY=none django-admin collectstatic --noinput --clear

COPY --chown=$UID:$GID --from=frontend ./climtech/static_compiled /climtech/static_compiled


# RUN SECRET_KEY=none django-admin collectstatic --noinput --clear
COPY --chown=$UID:$GID docker-entrypoint.sh ./

RUN chmod a+x ./docker-entrypoint.sh

ENTRYPOINT ["/usr/bin/tini", "--", "./docker-entrypoint.sh"]

# Run application
CMD ["gunicorn", "climtech.wsgi:application"]


# This stage builds the image that we use for development
FROM backend AS dev

# Install Node.js because newer versions of Heroku CLI have a node binary dependency
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
RUN apt-get install -y nodejs

# Switch to the application user
USER climtech

# Install development dependencies
COPY --chown=climtech pyproject.toml poetry.lock ./
RUN poetry install --no-root

# Pull in the node modules for the frontend
COPY --chown=climtech --from=frontend ./node_modules ./node_modules

# Make sure the working directory is on PYTHONPATH (so django-admin etc. can
# import climtech)
ENV PYTHONPATH=/app
