#!/bin/bash
# Bash strict mode: http://redsymbol.net/articles/unofficial-bash-strict-mode/
set -euo pipefail

# ======================================================
# ENVIRONMENT VARIABLES USED DIRECTLY BY THIS ENTRYPOINT
# ======================================================

MIGRATE_ON_STARTUP=${MIGRATE_ON_STARTUP:-true}
CACHE_TABLE_ON_STARTUP=${CACHE_TABLE_ON_STARTUP:-true}

CLIMTECH_LOG_LEVEL=${CLIMTECH_LOG_LEVEL:-INFO}
GUNICORN_NUM_OF_WORKERS=${GUNICORN_NUM_OF_WORKERS:-}
COLLECT_STATICFILES_ON_STARTUP=${COLLECT_STATICFILES_ON_STARTUP:-true}


show_help() {
    echo """
The available ClimTech related commands and services are shown below:

ADMIN COMMANDS:
manage          : Manage ClimTech and its database
shell           : Start a Django Python shell
help            : Show this message

SERVICE COMMANDS:
gunicorn            : Start ClimTech using a prod ready gunicorn server:
                         * Waits for the postgres database to be available first.
                         * Automatically migrates the database on startup.
                         * Binds to 0.0.0.0
gunicorn-wsgi       : Same as gunicorn but runs a wsgi server
"""
}

show_startup_banner() {
  # Use https://manytools.org/hacker-tools/ascii-banner/ and the font ANSI Shadow / Wide / Wide to generate
cat <<EOF
=========================================================================================
   _____ _      _____ __  __ _______ ______ _____ _    _
  / ____| |    |_   _|  \/  |__   __|  ____/ ____| |  | |
 | |    | |      | | | \  / |  | |  | |__ | |    | |__| |
 | |    | |      | | | |\/| |  | |  |  __|| |    |  __  |
 | |____| |____ _| |_| |  | |  | |  | |___| |____| |  | |
  \_____|______|_____|_|  |_|  |_|  |______\_____|_|  |_|

=========================================================================================
EOF
}

run_setup_commands_if_configured() {

        # migrate database
    if [ "$MIGRATE_ON_STARTUP" = "true" ]; then
        echo "python manage.py migrate"
        /app/manage.py migrate --noinput
    fi

        # cache table
    if [ "$CACHE_TABLE_ON_STARTUP" = "true" ]; then
        echo "python manage.py createcachetable"
        /app/manage.py createcachetable
    fi

      # collect staticfiles
     if [ "$COLLECT_STATICFILES_ON_STARTUP" = "true" ]; then
         echo "python manage.py collectstatic --clear --noinput"
         /app/manage.py collectstatic --clear --noinput
     fi
}


run_server() {
    run_setup_commands_if_configured

    if [[ "$1" = "wsgi" ]]; then
        STARTUP_ARGS=(climtech.config.wsgi:application)
    elif [[ "$1" = "asgi" ]]; then
        STARTUP_ARGS=(-k uvicorn.workers.UvicornWorker climtech.config.asgi:application)
    else
        echo -e "\e[31mUnknown run_server argument $1 \e[0m" >&2
        exit 1
    fi

    # Gunicorn args explained in order:
    #
    # 1. See https://docs.gunicorn.org/en/stable/faq.html#blocking-os-fchmod for
    #    why we set worker-tmp-dir to /dev/shm by default.
    # 2. Log to stdout
    # 3. Log requests to stdout
    exec gunicorn --workers="${GUNICORN_NUM_OF_WORKERS}" \
        --worker-tmp-dir "${TMPDIR:-/dev/shm}" \
        --log-file=- \
        --access-logfile=- \
        --capture-output \
        -b "0.0.0.0:8000" \
        --log-level="${CLIMTECH_LOG_LEVEL}" \
        "${STARTUP_ARGS[@]}" \
        "${@:2}"
}

setup_otel_vars(){
  # These key value pairs will be exported on every log/metric/trace by any otel
  # exporters running in subprocesses launched by this script.
  EXTRA_OTEL_RESOURCE_ATTRIBUTES="service.namespace=Climtech,"
  EXTRA_OTEL_RESOURCE_ATTRIBUTES+="deployment.environment=${CLIMTECH_DEPLOYMENT_ENV:-unknown}"

  if [[ -n "${OTEL_RESOURCE_ATTRIBUTES:-}" ]]; then
    # If the container has been launched with some extra otel attributes, make sure not
    # to override them with our Climtech specific ones.
    OTEL_RESOURCE_ATTRIBUTES="${EXTRA_OTEL_RESOURCE_ATTRIBUTES},${OTEL_RESOURCE_ATTRIBUTES}"
  else
    OTEL_RESOURCE_ATTRIBUTES="$EXTRA_OTEL_RESOURCE_ATTRIBUTES"
  fi
  export OTEL_RESOURCE_ATTRIBUTES
  echo "OTEL_RESOURCE_ATTRIBUTES=$OTEL_RESOURCE_ATTRIBUTES"
}


# ======================================================
# COMMANDS
# ======================================================

if [[ -z "${1:-}" ]]; then
    echo "Must provide arguments to docker-entrypoint.sh"
    show_help
    exit 1
fi

show_startup_banner

# wait for required services to be available, using docker-compose-wait
/wait

setup_otel_vars

case "$1" in
gunicorn)
    export OTEL_SERVICE_NAME="climtech-asgi"
    run_server asgi "${@:2}"
    ;;
gunicorn-wsgi)
    export OTEL_SERVICE_NAME="climtech-wsgi"
    run_server wsgi "${@:2}"
    ;;
manage)
    export OTEL_SERVICE_NAME=climtech-manage
    exec python3 manage.py "${@:2}"
    ;;
shell)
    export OTEL_SERVICE_NAME=climtech-shell
    exec python3 manage.py shell
    ;;
*)
    echo "Command given was $*"
    show_help
    exit 1
    ;;
esac
