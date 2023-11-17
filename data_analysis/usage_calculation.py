"""
usage_calculation.py

This script calculates the water usage at different endpoints in a water distribution
network over a specified time range. It outputs the calculated usage data and its hash
to a CSV file located in the 'outputs' directory.

Functions:
- calculate_endpoint_usage: Calculates and outputs water usage at endpoints.
"""

import os
import pandas as pd
import hashlib

def calculate_endpoint_usage(file_path):
    """
    Calculates water usage at endpoints within a specified time range and saves the data to a CSV file in the 'outputs' directory. Also, computes and prints the hash of the output data.

    Parameters:
    - file_path (str): Path to the dataset file.
    """
    # Load the dataset
    data = pd.read_csv(file_path)

    # Calculating the min and max timestamp values for guidance
    min_timestamp = data['timestamp'].min()
    max_timestamp = data['timestamp'].max()

    print("Available time range for water usage calculation:")
    print(f"From: {min_timestamp}")
    print(f"To:   {max_timestamp}")
    from_timestamp = input("Enter the 'from' timestamp (format YYYY-MM-DD HH:MM:SS): ")
    to_timestamp = input("Enter the 'to' timestamp (format YYYY-MM-DD HH:MM:SS): ")

    # Filtering the data based on the provided time range
    filtered_data = data[(data['timestamp'] >= from_timestamp) & (data['timestamp'] <= to_timestamp) & (data['type'] == 'Endpoint')]

    # Grouping the data by sensor ID and calculating total water usage for each endpoint
    grouped_data = filtered_data.groupby('sensor_id')['water_usage'].sum().reset_index()

    # Create 'outputs' directory if it doesn't exist
    output_dir = 'outputs'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Saving the results to a CSV file in the 'outputs' directory
    output_file_path = os.path.join(output_dir, 'endpoint_water_usage.csv')
    grouped_data.to_csv(output_file_path, index=False)

    # Calculate and print the hash of the output file
    with open(output_file_path, 'rb') as file:
        file_content = file.read()
    hash_result = hashlib.sha256(file_content).hexdigest()

    print(f"Water usage at endpoints has been calculated and stored in {output_file_path}.")
    print(f"The SHA-256 hash of the output file is: {hash_result}")

if __name__ == "__main__":
    file_path = 'datasets/water_distribution_data.csv'  # Replace with the actual path to your dataset
    calculate_endpoint_usage(file_path)
