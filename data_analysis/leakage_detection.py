"""
leakage_detection.py

This script analyzes a dataset from a water distribution network to detect and report potential leakages.
It considers discrepancies in expected and actual water flows to identify the location and severity of leakages.

Functions:
- detect_leakages: Identifies potential leakages and their details.
- main: Entry point for running the leakage detection analysis.
"""

import pandas as pd

def detect_leakages(data):
    """
    Detects leakages in the network based on discrepancies in water flows.

    Parameters:
    - data (DataFrame): The dataset containing water flow information.

    Returns:
    - List[Dict]: A list of dictionaries containing leakage information.
    """
    leakages = []
    total_leakage_amount = 0
    grouped_data = data.groupby(['timestamp'])

    for timestamp, group in grouped_data:
        junctions = group[group['type'] == 'Junction']
        endpoints = group[group['type'] == 'Endpoint']

        for _, junction in junctions.iterrows():
            junction_outflow = junction['water_usage']
            connected_endpoints = endpoints[endpoints['path_to_master'].str.contains(str(junction['sensor_id']))]
            total_usage_endpoints = connected_endpoints['water_usage'].sum()

            if junction_outflow > total_usage_endpoints:
                leakage_amount = junction_outflow - total_usage_endpoints
                total_leakage_amount += leakage_amount
                leakage_percentage = (leakage_amount / junction_outflow) * 100
                leakages.append({
                    'timestamp': timestamp,
                    'junction_id': junction['sensor_id'],
                    'leakage_amount': leakage_amount,
                    'leakage_percentage': leakage_percentage,
                    'path_to_master': junction['path_to_master']
                })

    return leakages, total_leakage_amount

def main():
    """
    Main function to execute leakage detection.
    """
    # Load the dataset
    file_path = 'datasets/water_distribution_data_leak.csv'
    data = pd.read_csv(file_path)

    # Detect leakages
    leakage_info, total_leakage = detect_leakages(data)

    # Print the results
    print("Leakage Detection Report:")
    print("-" * 30)
    for leak in leakage_info:
        print(f"Timestamp: {leak['timestamp']}\nJunction ID: {leak['junction_id']}\nLeakage: {leak['leakage_amount']} units ({leak['leakage_percentage']:.2f}%)\nPath to Master: {leak['path_to_master']}")
        print("-" * 30)

    print(f"Total Leakage in the System: {total_leakage:.2f} units")

if __name__ == "__main__":
    main()
