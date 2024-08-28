#!/bin/bash

# Function to run the debug script
run_debug() {
    echo "Running debug script..."
    cd backend
    source venv/bin/activate
    python debug_backend.py
    deactivate
    cd ..
}

# Check if debug flag is set
if [ "$1" = "--debug" ]; then
    run_debug
    exit 0
fi

# Start the Flask backend
echo "Starting Flask backend..."
cd backend
source venv/bin/activate
python app.py &
BACKEND_PID=$!

# Wait for the backend to start
sleep 5

# Check if the backend is running
if ps -p $BACKEND_PID > /dev/null
then
    echo "Flask backend is running."
else
    echo "Error: Flask backend failed to start."
    run_debug
    exit 1
fi

# Start the React frontend
echo "Starting React frontend..."
cd ../frontend
npm start