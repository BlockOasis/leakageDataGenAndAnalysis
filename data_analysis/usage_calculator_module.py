"""
usage_calculation.py

This script calculates the water usage at different endpoints in a water distribution
network and returns the hash of the calculated usage data.

Functions:
- calculate_endpoint_usage: Calculates and returns the hash of water usage at endpoints.
"""


import pandas as pd
import hashlib
from io import StringIO

def calculate_endpoint_usage(csv_data):
    """
    Calculates water usage at endpoints within the entire dataset and returns the SHA-256 hash of the calculated data.

    Parameters:
    - csv_data (str): String containing CSV formatted data.
    """
    # Read the dataset from the CSV string
    data = pd.read_csv(StringIO(csv_data))

    # Filter data to include only 'Endpoint' type
    filtered_data = data[data['type'] == 'Endpoint']

    # Grouping the data by sensor ID and calculating total water usage for each endpoint
    grouped_data = filtered_data.groupby('sensor_id')['water_usage'].sum().reset_index()

    # Convert the grouped data to a CSV string and calculate its hash (without index and header)
    grouped_data_csv = grouped_data.to_csv(index=False, header=False)
    hash_result = hashlib.sha256(grouped_data_csv.encode()).hexdigest()

    return hash_result

if __name__ == "__main__":
    # Example CSV data as a string
    csv_data = """
    timestamp,sensor_id,type,device_type,water_usage
2023-01-01 00:00:00,1011,Endpoint,Home,0
2023-01-01 00:00:00,1012,Endpoint,Home,61
2023-01-01 00:00:00,1013,Endpoint,Home,60
2023-01-01 00:00:00,1014,Endpoint,Factory,90
2023-01-01 00:00:00,1015,Endpoint,Factory,250
2023-01-01 00:00:00,1016,Endpoint,Fire_Hydrant,0
2023-01-01 00:00:00,1001,Junction,Local,533.633810377806
2023-01-01 00:00:00,1017,Endpoint,Home,33
2023-01-01 00:00:00,1018,Endpoint,Home,0
2023-01-01 00:00:00,1019,Endpoint,Home,10
2023-01-01 00:00:00,1020,Endpoint,Home,76
2023-01-01 00:00:00,1021,Endpoint,Home,0
2023-01-01 00:00:00,1022,Endpoint,Factory,87
2023-01-01 00:00:00,1023,Endpoint,Factory,0
2023-01-01 00:00:00,1024,Endpoint,Fire_Hydrant,0
2023-01-01 00:00:00,1025,Endpoint,Fire_Hydrant,0
2023-01-01 00:00:00,1026,Endpoint,Fire_Hydrant,0
2023-01-01 00:00:00,1002,Junction,Local,206
2023-01-01 00:00:00,1027,Endpoint,Home,0
2023-01-01 00:00:00,1028,Endpoint,Home,64
2023-01-01 00:00:00,1029,Endpoint,Home,64
2023-01-01 00:00:00,1030,Endpoint,Home,0
2023-01-01 00:00:00,1031,Endpoint,Factory,203
2023-01-01 00:00:00,1032,Endpoint,Agricultural_Channel,95
2023-01-01 00:00:00,1033,Endpoint,Agricultural_Channel,0
2023-01-01 00:00:00,1034,Endpoint,Agricultural_Channel,18
2023-01-01 00:00:00,1035,Endpoint,Fire_Hydrant,0
2023-01-01 00:00:00,1036,Endpoint,Fire_Hydrant,0
2023-01-01 00:00:00,1037,Endpoint,Fire_Hydrant,0
2023-01-01 00:00:00,1038,Endpoint,Fire_Hydrant,0
2023-01-01 00:00:00,1003,Junction,Local,444
2023-01-01 00:00:00,1039,Endpoint,Home,17
2023-01-01 00:00:00,1040,Endpoint,Home,47
2023-01-01 00:00:00,1041,Endpoint,Home,78
2023-01-01 00:00:00,1042,Endpoint,Home,23
2023-01-01 00:00:00,1043,Endpoint,Factory,221
2023-01-01 00:00:00,1044,Endpoint,Factory,328
2023-01-01 00:00:00,1045,Endpoint,Agricultural_Channel,0
2023-01-01 00:00:00,1046,Endpoint,Agricultural_Channel,311
2023-01-01 00:00:00,1047,Endpoint,Agricultural_Channel,234
2023-01-01 00:00:00,1048,Endpoint,Agricultural_Channel,0
2023-01-01 00:00:00,1049,Endpoint,Fire_Hydrant,0
2023-01-01 00:00:00,1050,Endpoint,Fire_Hydrant,0
2023-01-01 00:00:00,1004,Junction,Local,1259
2023-01-01 00:00:00,1051,Endpoint,Home,0
2023-01-01 00:00:00,1052,Endpoint,Home,43
2023-01-01 00:00:00,1053,Endpoint,Home,0
2023-01-01 00:00:00,1054,Endpoint,Home,23
2023-01-01 00:00:00,1055,Endpoint,Factory,0
2023-01-01 00:00:00,1056,Endpoint,Factory,172
2023-01-01 00:00:00,1057,Endpoint,Agricultural_Channel,113
2023-01-01 00:00:00,1058,Endpoint,Agricultural_Channel,180
2023-01-01 00:00:00,1059,Endpoint,Agricultural_Channel,0
2023-01-01 00:00:00,1060,Endpoint,Agricultural_Channel,0
2023-01-01 00:00:00,1061,Endpoint,Agricultural_Channel,140
2023-01-01 00:00:00,1062,Endpoint,Fire_Hydrant,0
2023-01-01 00:00:00,1063,Endpoint,Fire_Hydrant,0
2023-01-01 00:00:00,1064,Endpoint,Fire_Hydrant,0
2023-01-01 00:00:00,1065,Endpoint,Fire_Hydrant,0
2023-01-01 00:00:00,1066,Endpoint,Fire_Hydrant,0
2023-01-01 00:00:00,1067,Endpoint,Fire_Hydrant,0
2023-01-01 00:00:00,1068,Endpoint,Fire_Hydrant,0
2023-01-01 00:00:00,1005,Junction,Local,671
2023-01-01 00:00:00,1069,Endpoint,Home,0
2023-01-01 00:00:00,1070,Endpoint,Home,29
2023-01-01 00:00:00,1071,Endpoint,Home,13
2023-01-01 00:00:00,1072,Endpoint,Home,0
2023-01-01 00:00:00,1073,Endpoint,Factory,244
2023-01-01 00:00:00,1074,Endpoint,Factory,322
2023-01-01 00:00:00,1075,Endpoint,Fire_Hydrant,0
2023-01-01 00:00:00,1076,Endpoint,Fire_Hydrant,0
2023-01-01 00:00:00,1077,Endpoint,Fire_Hydrant,0
2023-01-01 00:00:00,1078,Endpoint,Fire_Hydrant,0
2023-01-01 00:00:00,1079,Endpoint,Fire_Hydrant,0
2023-01-01 00:00:00,1080,Endpoint,Fire_Hydrant,0
2023-01-01 00:00:00,1081,Endpoint,Fire_Hydrant,0
2023-01-01 00:00:00,1082,Endpoint,Fire_Hydrant,0
2023-01-01 00:00:00,1083,Endpoint,Fire_Hydrant,0
2023-01-01 00:00:00,1084,Endpoint,Fire_Hydrant,0
2023-01-01 00:00:00,1006,Junction,Local,608
2023-01-01 00:00:00,1085,Endpoint,Home,61
2023-01-01 00:00:00,1086,Endpoint,Home,0
2023-01-01 00:00:00,1087,Endpoint,Home,20
2023-01-01 00:00:00,1088,Endpoint,Home,53
2023-01-01 00:00:00,1089,Endpoint,Factory,40
2023-01-01 00:00:00,1090,Endpoint,Agricultural_Channel,240
2023-01-01 00:00:00,1091,Endpoint,Agricultural_Channel,135
2023-01-01 00:00:00,1092,Endpoint,Agricultural_Channel,13
2023-01-01 00:00:00,1093,Endpoint,Agricultural_Channel,233
2023-01-01 00:00:00,1094,Endpoint,Agricultural_Channel,153
2023-01-01 00:00:00,1095,Endpoint,Fire_Hydrant,0
2023-01-01 00:00:00,1096,Endpoint,Fire_Hydrant,0
2023-01-01 00:00:00,1097,Endpoint,Fire_Hydrant,0
2023-01-01 00:00:00,1007,Junction,Local,948
2023-01-01 00:00:00,1098,Endpoint,Home,0
2023-01-01 00:00:00,1099,Endpoint,Home,33
2023-01-01 00:00:00,1100,Endpoint,Home,42
2023-01-01 00:00:00,1101,Endpoint,Home,54
2023-01-01 00:00:00,1102,Endpoint,Factory,0
2023-01-01 00:00:00,1103,Endpoint,Agricultural_Channel,353
2023-01-01 00:00:00,1104,Endpoint,Fire_Hydrant,0
2023-01-01 00:00:00,1105,Endpoint,Fire_Hydrant,0
2023-01-01 00:00:00,1106,Endpoint,Fire_Hydrant,0
2023-01-01 00:00:00,1107,Endpoint,Fire_Hydrant,0
2023-01-01 00:00:00,1108,Endpoint,Fire_Hydrant,980
2023-01-01 00:00:00,1109,Endpoint,Fire_Hydrant,0
2023-01-01 00:00:00,1110,Endpoint,Fire_Hydrant,0
2023-01-01 00:00:00,1111,Endpoint,Fire_Hydrant,0
2023-01-01 00:00:00,1112,Endpoint,Fire_Hydrant,0
2023-01-01 00:00:00,1008,Junction,Local,1494.2396926045485
2023-01-01 00:00:00,1113,Endpoint,Home,17
2023-01-01 00:00:00,1114,Endpoint,Home,0
2023-01-01 00:00:00,1115,Endpoint,Home,0
2023-01-01 00:00:00,1116,Endpoint,Home,0
2023-01-01 00:00:00,1117,Endpoint,Home,0
2023-01-01 00:00:00,1118,Endpoint,Factory,419
2023-01-01 00:00:00,1119,Endpoint,Agricultural_Channel,0
2023-01-01 00:00:00,1120,Endpoint,Agricultural_Channel,107
2023-01-01 00:00:00,1121,Endpoint,Fire_Hydrant,0
2023-01-01 00:00:00,1009,Junction,Local,586.4585998134704
2023-01-01 00:00:00,1122,Endpoint,Home,94
2023-01-01 00:00:00,1123,Endpoint,Home,12
2023-01-01 00:00:00,1124,Endpoint,Home,89
2023-01-01 00:00:00,1125,Endpoint,Home,0
2023-01-01 00:00:00,1126,Endpoint,Home,0
2023-01-01 00:00:00,1127,Endpoint,Factory,112
2023-01-01 00:00:00,1128,Endpoint,Agricultural_Channel,243
2023-01-01 00:00:00,1129,Endpoint,Agricultural_Channel,309
2023-01-01 00:00:00,1130,Endpoint,Agricultural_Channel,326
2023-01-01 00:00:00,1131,Endpoint,Agricultural_Channel,179
2023-01-01 00:00:00,1132,Endpoint,Fire_Hydrant,0
2023-01-01 00:00:00,1133,Endpoint,Fire_Hydrant,0
2023-01-01 00:00:00,1134,Endpoint,Fire_Hydrant,0
2023-01-01 00:00:00,1135,Endpoint,Fire_Hydrant,0
2023-01-01 00:00:00,1136,Endpoint,Fire_Hydrant,0
2023-01-01 00:00:00,1137,Endpoint,Fire_Hydrant,0
2023-01-01 00:00:00,1138,Endpoint,Fire_Hydrant,0
2023-01-01 00:00:00,1139,Endpoint,Fire_Hydrant,0
2023-01-01 00:00:00,1140,Endpoint,Fire_Hydrant,0
2023-01-01 00:00:00,1141,Endpoint,Fire_Hydrant,0
2023-01-01 00:00:00,1010,Junction,Local,1364
2023-01-01 00:00:00,1000,Junction,Master,8114.332102795825
"""

print(calculate_endpoint_usage(csv_data))
