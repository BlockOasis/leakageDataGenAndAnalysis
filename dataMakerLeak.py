import random
import csv
from datetime import datetime, timedelta

class Endpoint:
    def __init__(self, endpoint_type, sensor_id, path_to_master):
        self.endpoint_type = endpoint_type
        self.sensor_id = sensor_id
        self.path_to_master = path_to_master
        self.usage_probability, self.max_usage = self.set_usage_parameters()
        self.water_usage = 0

    def set_usage_parameters(self):
        parameters = {
            'Home': (0.7, 100),
            'Factory': (0.8, 500),
            'Agricultural_Channel': (0.6, 400),
            'Fire_Hydrant': (0.01, 1000)
        }
        return parameters[self.endpoint_type]

    def simulate_water_usage(self):
        if random.random() < self.usage_probability:
            self.water_usage = random.randint(10, self.max_usage)
        else:
            self.water_usage = 0
        return self.water_usage

class Junction:
    def __init__(self, junction_type, sensor_id, path_to_master):
        self.junction_type = junction_type
        self.sensor_id = sensor_id
        self.path_to_master = path_to_master
        self.connected_junctions = []
        self.connected_endpoints = []
        self.inflow = 0
        self.outflow = 0

    def connect_to_junction(self, junction):
        self.connected_junctions.append(junction)

    def connect_to_endpoint(self, endpoint):
        self.connected_endpoints.append(endpoint)
        endpoint.connected_junction = self

    def calculate_flow(self):
        self.outflow = sum(endpoint.water_usage for endpoint in self.connected_endpoints)
        self.inflow = self.outflow
        
    def calculate_flow_with_leakage(self, leakage_probability, max_leakage_percent, is_master=False):
        if is_master:
            # For master junction, sum up outflow from all connected local junctions
            self.outflow = sum(junction.outflow for junction in self.connected_junctions)

            # Simulate potential leakage for the master junction
            if random.random() < leakage_probability:
                leakage_percent = random.uniform(0, max_leakage_percent)
                additional_leakage = self.outflow * leakage_percent
                self.outflow += additional_leakage
        else:
            # For local junctions, sum up the water usage from all connected endpoints
            total_endpoint_usage = sum(endpoint.water_usage for endpoint in self.connected_endpoints)
            self.outflow = total_endpoint_usage

            # Simulate potential leakage for local junctions
            if random.random() < leakage_probability:
                leakage_percent = random.uniform(0, max_leakage_percent)
                additional_leakage = total_endpoint_usage * leakage_percent
                self.outflow += additional_leakage

        self.inflow = self.outflow  # Assuming the inflow matches the outflow



def create_junctions_and_endpoints(master_sensor_id):
    sensor_id_counter = master_sensor_id + 1
    path_to_master = [master_sensor_id]

    # Create Master Junction
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

def simulate_network(time_units, start_time, master_sensor_id, leakage_probability, max_leakage_percent):
    local_junctions, master_junction = create_junctions_and_endpoints(master_sensor_id)
    data = []
    current_time = start_time

    for _ in range(time_units):
        # Simulate water usage at endpoints and calculate flow at local junctions
        for lj in local_junctions:
            for endpoint in lj.connected_endpoints:
                endpoint.simulate_water_usage()
            lj.calculate_flow_with_leakage(leakage_probability, max_leakage_percent)

        # Calculate flow for master junction with potential leakage
        master_junction.calculate_flow_with_leakage(leakage_probability, max_leakage_percent, is_master=True)

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


def output_dataset(data):
    fieldnames = ['timestamp', 'sensor_id', 'path_to_master', 'type', 'device_type', 'water_usage']

    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

# Initialize and run the simulation
filename = 'water_distribution_data_leak.csv'
start_time = datetime(2023, 1, 1, 0, 0)
time_units = 24
master_sensor_id = 1000

# Parameters for leakage
leakage_probability = 0.2  # 20% chance of leakage in any given time unit
max_leakage_percent = 0.3  # Up to 30% additional water can be lost due to leakage

data = simulate_network(time_units, start_time, master_sensor_id, leakage_probability, max_leakage_percent)
output_dataset(data)
print(f'Dataset generated: {filename}')
