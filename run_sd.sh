#!/bin/bash

# Define the commands you want to run in each terminal
commands=(
    "python3 uc.py"
    "python3 valvulas.py"
    "python3 umidade.py"
    "python3 meteorologia.py"
)

# Detect OS and choose the correct terminal command
open_terminal() {
    local cmd="$1"
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Check for installed terminal emulator
        if command -v gnome-terminal &> /dev/null; then
            gnome-terminal -- bash -c "$cmd; exec bash"
        elif command -v xfce4-terminal &> /dev/null; then
            xfce4-terminal --hold --command="$cmd"
        elif command -v konsole &> /dev/null; then
            konsole -e "bash -c '$cmd; exec bash'"
        else
            echo "No compatible terminal found on Linux."
            exit 1
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS typically uses Terminal.app
        osascript -e "tell application \"Terminal\" to do script \"$cmd\""
    else
        echo "Unsupported OS: $OSTYPE"
        exit 1
    fi
}

# Loop through each command and open it in a new terminal window
# open_terminal "sudo rabbitmq-server"
for cmd in "${commands[@]}"; do
    current_path=$(pwd)
    open_terminal "cd $current_path && source venv/bin/activate && $cmd"
done
