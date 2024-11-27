#!/bin/bash

# Display a greeting message
echo "Welcome to the Driver's Sleep Alarm Program"
echo "This tool will alert you when it's time to take a break or wake up."

# Ask the user to input the time in minutes for the sleep alarm
read -p "Enter the number of minutes until the sleep alarm: " minutes

# Validate if the input is a positive number
if ! [[ "$minutes" =~ ^[0-9]+$ ]] || [ "$minutes" -le 0 ]; then
    echo "Invalid input. Please enter a positive number."
    exit 1
fi

# Display countdown and wait for the set time to pass
echo "The alarm will go off in $minutes minutes."
sleep $((minutes * 60))

# Trigger the sleep alarm
echo "Time's up! Please take a break or wake up now!"

# Play a sound to alert the driver (using `aplay` or any sound-playing tool)
# Ensure that `aplay` is installed, or replace it with another sound-playing command if needed.
if command -v aplay &> /dev/null; then
    aplay /path/to/alarm-sound.wav
else
    echo "Alarm sound player not found. Please install 'aplay' or replace with a suitable sound command."
fi

echo "Stay safe on the road!"
