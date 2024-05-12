#!/bin/bash
# entrypoint.sh

# Check the first command-line argument
case "$1" in
    test)
        echo "Running BDD tests..."
        behave /app/features
        ;;
    app)
        echo "Running etl application..."
        python /app/src/etl.py
        ;;
    *)
        echo "Invalid option: $1"
        echo "Usage: docker run <image> [app|test]"
        exit 1
        ;;
esac
