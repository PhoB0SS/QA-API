#!/bin/bash
set -e

alembic upgrade head
fastapi dev qa_api/main.py --host $API_HOST --port $API_PORT