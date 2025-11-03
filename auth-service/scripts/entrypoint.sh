#!/bin/bash
set -e

FLAG_FILE="/app/.initialized"

if [ -f "$FLAG_FILE" ]; then
    echo "Initialization is already done"
else
    echo "Creating tables"
    uv run python scripts/init_db.py

    touch "$FLAG_FILE"

    echo "Initialized successfully"
fi

exec "$@"