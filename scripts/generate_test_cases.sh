#!/bin/bash

# Function to generate a random test case
generate_test_case() {
    local num_neighborhoods=$1
    local num_homebuyers=$2
    local filename=$3

    echo "Generating test case with $num_neighborhoods neighborhoods and $num_homebuyers homebuyers"

    > "$filename"  # Clear the file

    # Generate neighborhoods
    for ((i=0; i<num_neighborhoods; i++)); do
        echo "N N$i E:$((RANDOM % 10 + 1)) W:$((RANDOM % 10 + 1)) R:$((RANDOM % 10 + 1))" >> "$filename"
    done

    # Generate homebuyers
    for ((i=0; i<num_homebuyers; i++)); do
        echo -n "H H$i E:$((RANDOM % 10 + 1)) W:$((RANDOM % 10 + 1)) R:$((RANDOM % 10 + 1)) " >> "$filename"
        
        # Generate preferences
        pref=$(seq 0 $((num_neighborhoods-1)) | shuf | sed 's/^/N/' | tr '\n' '>' | sed 's/>$//')
        echo "$pref" >> "$filename"
    done
}

# Function to run a test case
run_test_case() {
    local input_file=$1
    local output_file=$2

    echo "Running test case: $input_file"
    python3 app/main.py "$input_file" "$output_file"

    if [ $? -eq 0 ]; then
        echo "Test case completed successfully"
        echo "Output:"
        cat "$output_file"
        echo
    else
        echo "Test case failed"
    fi
}

# Main script
echo "Homeowners and Neighborhoods Exercise Test Suite"
echo "================================================"

# Ensure the Python script exists
if [ ! -f app/main.py ]; then
    echo "Error: app/main.py not found"
    exit 1
fi

# Test case 0: Example test case from PDF
run_test_case "assets/inputs/case0.txt" "assets/outputs/case_0_output.txt"

# Test case 1: Simple case (3 neighborhoods, 9 homebuyers)
generate_test_case 3 9 "assets/inputs/test_case_1_input.txt"
run_test_case "assets/inputs/test_case_1_input.txt" "assets/outputs/test_case_1_output.txt"

# Test case 2: Larger case (5 neighborhoods, 20 homebuyers)
generate_test_case 5 20 "assets/inputs/test_case_2_input.txt"
run_test_case "assets/inputs/test_case_2_input.txt" "assets/outputs/test_case_2_output.txt"

# Test case 3: Edge case (1 neighborhood, 3 homebuyers)
generate_test_case 1 3 "assets/inputs/test_case_3_input.txt"
run_test_case "assets/inputs/test_case_3_input.txt" "assets/outputs/test_case_3_output.txt"

# Test case 4: Another edge case (10 neighborhoods, 10 homebuyers)
generate_test_case 10 10 "assets/inputs/test_case_4_input.txt"
run_test_case "assets/inputs/test_case_4_input.txt" "assets/outputs/test_case_4_output.txt"

echo "All tests completed"