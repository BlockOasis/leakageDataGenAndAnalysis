"""
data_maker.py

This script simulates a basic water distribution network for data generation purposes. 
It creates a network of junctions and endpoints, simulates water usage at these endpoints,
and calculates the flow through the junctions. The generated data is then written to a CSV file.

Classes:
- Endpoint: Represents an endpoint in the network (e.g., home, factory) and simulates water usage.
- Junction: Represents a junction in the network and calculates water flow based on connected endpoints.

Functions:
- create_junctions_and_endpoints: Initializes the network with junctions and endpoints.
- simulate_network: Simulates water usage and flow in the network over a specified time period.
- output_dataset: Writes the generated data to a CSV file.
"""

import random
import csv
from datetime import datetime, timedelta

class Endpoint:
    """ Represents an endpoint in the water distribution network. """
    def __init__(self, endpoint_type, sensor_id, path_to_master):
        self.endpoint_type = endpoint_type
        self.sensor_id = sensor_id
        self.path_to_master = path_to_master
        self.usage_probability, self.max_usage = self.set_usage_parameters()
        self.water_usage = 0

    def set_usage_parameters(self):
        """ Sets water usage parameters based on the type of endpoint. """
        parameters = {
            'Home': (0.7, 100),
            'Factory': (0.8, 500),
            'Agricultural_Channel': (0.6, 400),
            'Fire_Hydrant': (0.01, 1000)
        }
        return parameters[self.endpoint_type]

    def simulate_water_usage(self):
        """ Simulates water usage based on the endpoint's usage probability and maximum usage. """
        if random.random() < self.usage_probability:
            self.water_usage = random.randint(10, self.max_usage)
        else:
            self.water_usage = 0
        return self.water_usage

class Junction:
    """ Represents a junction in the water distribution network. """
    def __init__(self, junction_type, sensor_id, path_to_master):
        self.junction_type = junction_type
        self.sensor_id = sensor_id
        self.path_to_master = path_to_master
        self.connected_junctions = []
        self.connected_endpoints = []
        self.inflow = 0
        self.outflow = 0

    def connect_to_junction(self, junction):
        """ Connects this junction to another junction. """
        self.connected_junctions.append(junction)

    def connect_to_endpoint(self, endpoint):
        """ Connects an endpoint to this junction. """
        self.connected_endpoints.append(endpoint)
        endpoint.connected_junction = self

    def calculate_flow(self):
        """ Calculates the water flow through this junction based on connected endpoints. """
        self.outflow = sum(endpoint.water_usage for endpoint in self.connected_endpoints)
        self.inflow = self.outflow

def create_junctions_and_endpoints(master_sensor_id):
    """ Creates a network of junctions and endpoints for the simulation. """
    sensor_id_counter = master_sensor_id + 1
    path_to_master = [master_sensor_id]

    # Initialize master junction and local junctions
    master_junction = Junction('Master', master_sensor_id, path_to_master[:])

    # Create Local Junctions
    local_junctions = [Junction('Local', sensor_id_counter + i, path_to_master + [sensor_id_counter + i]) for i in range(10)]
    sensor_id_counter += 10

    # Connect Local Junctions to Endpoints
    for lj in local_junctions:
        for _ in range(random.randint(3, 5)):  # Homes
            lj.connect_to_endpoint(Endpoint('Home', sensor_id_counter, lj.path_to_master + [sensor_id_counter]))
            sensor_id_counter += 1
        for _ in range(random.randint(1, 2)):  # Factories
            lj.connect_to_endpoint(Endpoint('Factory', sensor_id_counter, lj.path_to_master + [sensor_id_counter]))
            sensor_id_counter += 1
        for _ in range(random.randint(0, 5)):
            lj.connect_to_endpoint(Endpoint('Agricultural_Channel', sensor_id_counter, lj.path_to_master + [sensor_id_counter]))
            sensor_id_counter += 1
        for _ in range(random.randint(1, 10)):
            lj.connect_to_endpoint(Endpoint('Fire_Hydrant', sensor_id_counter, lj.path_to_master + [sensor_id_counter]))
            sensor_id_counter += 1

    for lj in local_junctions:
        master_junction.connect_to_junction(lj)

    return local_junctions, master_junction

def simulate_network(time_units, start_time, master_sensor_id):
    """ Simulates the water network operation over a given time period. """
    local_junctions, master_junction = create_junctions_and_endpoints(master_sensor_id)
    data = []
    current_time = start_time

    # Simulate water usage and calculate flow
    for _ in range(time_units):

        # Simulate water usage at endpoints, and calculate flow at local junctions
        for lj in local_junctions:
            for endpoint in lj.connected_endpoints:
                endpoint.simulate_water_usage()
            lj.calculate_flow()

        # Update and calculate flow for master junction based on local junctions
        master_junction.outflow = sum(lj.outflow for lj in local_junctions)
        master_junction.inflow = master_junction.outflow

        # Record data for endpoints and local junctions
        for lj in local_junctions:
            for endpoint in lj.connected_endpoints:
                endpoint_data = {
                    'timestamp': current_time.strftime("%Y-%m-%d %H:%M:%S"),
                    'sensor_id': endpoint.sensor_id,
                    'path_to_master': '->'.join(map(str, endpoint.path_to_master)),
                    'type': 'Endpoint',
                    'device_type': endpoint.endpoint_type,
                    'water_usage': endpoint.water_usage
                }
                data.append(endpoint_data)

            junction_data = {
                'timestamp': current_time.strftime("%Y-%m-%d %H:%M:%S"),
                'sensor_id': lj.sensor_id,
                'path_to_master': '->'.join(map(str, lj.path_to_master)),
                'type': 'Junction',
                'device_type': 'Local',
                'water_usage': lj.outflow
            }
            data.append(junction_data)

        # Record data for master junction
        master_data = {
            'timestamp': current_time.strftime("%Y-%m-%d %H:%M:%S"),
            'sensor_id': master_junction.sensor_id,
            'path_to_master': '->'.join(map(str, master_junction.path_to_master)),
            'type': 'Junction',
            'device_type': 'Master',
            'water_usage': master_junction.outflow
        }
        data.append(master_data)

        current_time += timedelta(hours=1)

    return data

def output_dataset(data, filename):
    """ Outputs the simulated data to a CSV file. """
    fieldnames = ['timestamp', 'sensor_id', 'path_to_master', 'type', 'device_type', 'water_usage']
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

if __name__ == "__main__":
    # Main script execution logic
    filename = 'datasets/water_distribution_data.csv'
    start_time = datetime(2023, 1, 1, 0, 0)
    time_units = 240
    master_sensor_id = 1000
    data = simulate_network(time_units, start_time, master_sensor_id)
    output_dataset(data, filename)
    print(f"Dataset generated: {filename}")
