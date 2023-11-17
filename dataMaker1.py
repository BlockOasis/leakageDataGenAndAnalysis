import csv
import random
import time

def get_flow_rate_pattern(location_type, hour_of_day):
    """Generate a flow rate based on location type and hour of the day."""
    if location_type == 'home':
        if 6 <= hour_of_day <= 8 or 18 <= hour_of_day <= 20:  # Peak usage times
            return random.uniform(3.0, 8.0)
        else:
            return random.uniform(0.2, 3.0)
    elif location_type == 'factory':
        if 8 <= hour_of_day <= 17:  # Daytime working hours
            return random.uniform(10.0, 30.0)
        else:
            return random.uniform(2.0, 10.0)
    elif location_type == 'agricultural_channel':
        if 5 <= hour_of_day <= 7 or 17 <= hour_of_day <= 19:
            return random.uniform(20.0, 50.0)
        else:
            return random.uniform(5.0, 20.0)
    else:
        return random.uniform(0.5, 15.0)  # Default flow rate for other locations

def introduce_leakage(leakage_probability, leakage_factor_range):
    """Randomly decide whether to introduce leakage."""
    if random.random() < leakage_probability:
        return random.uniform(*leakage_factor_range)
    return 1.0

def generate_sensor_data(sensor_id, location_type, start_time, duration_days, interval_hours, leakage_probability=0.01, leakage_factor_range=(0.95, 0.99)):
    """Generate sample data for a water flow sensor, including leakage."""
    data_points = []
    cumulative_volume = 0
    interval_seconds = interval_hours * 3600

    for i in range(int(duration_days * 24 / interval_hours)):
        timestamp = start_time + i * interval_seconds
        hour_of_day = time.localtime(timestamp).tm_hour

        leakage_factor = introduce_leakage(leakage_probability, leakage_factor_range)

        flow_rate = get_flow_rate_pattern(location_type, hour_of_day) * leakage_factor
        cumulative_volume += flow_rate * interval_hours  # Flow rate already in volume/hour

        data_point = {
            "timestamp": timestamp,
            "sensor_id": sensor_id,
            "flow_rate": flow_rate,
            "cumulative_volume": cumulative_volume,
            "location_type": location_type
        }
        data_points.append(data_point)

    return data_points

def write_to_csv(file_name, fieldnames, data):
    """Write the data to a CSV file."""
    with open(file_name, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

# Define sensor locations
sensor_locations = ['home', 'factory', 'agricultural_channel', 'main_supply', 'branch_line', 'treatment_plant', 'pump_station', 'critical_junction']

# Generate sensors
sensors = [{"sensor_id": f"{location}_sensor_{i:03d}", "location_type": location} for location in sensor_locations for i in range(1, 11)]

# Generate and write data
all_sensor_data = []
start_time = time.time()
duration_days = 3  # Duration for data generation
interval_hours = 1  # Interval for data generation

for sensor in sensors:
    sensor_data = generate_sensor_data(sensor["sensor_id"], sensor["location_type"], start_time, duration_days, interval_hours)
    all_sensor_data.extend(sensor_data)

fieldnames = ["timestamp", "sensor_id", "flow_rate", "cumulative_volume", "location_type"]
write_to_csv("sensor_data.csv", fieldnames, all_sensor_data)
