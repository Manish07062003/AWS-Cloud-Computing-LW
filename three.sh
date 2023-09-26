#!/bin/bash

# Define a recursive function to calculate GCD
function calculate_gcd {
    if [ $2 -eq 0 ]; then
        echo "GCD: $1"
    else
        calculate_gcd $2 $(($1 % $2))
    fi
}

# Check if two arguments are provided
if [ $# -ne 2 ]; then
    echo "Usage: $0 <integer1> <integer2>"
    exit 1
fi

# Check if both arguments are integers
re='^[0-9]+$'
if ! [[ $1 =~ $re ]] || ! [[ $2 =~ $re ]]; then
    echo "Both arguments must be integers"
    exit 1
fi

# Call the function with provided integers
calculate_gcd $1 $2

