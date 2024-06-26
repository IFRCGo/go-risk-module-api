#!/bin/bash -x

# Using --max-tasks-per-child to handle memory leaks
celery -A risk_module worker --loglevel=info --max-tasks-per-child=20
