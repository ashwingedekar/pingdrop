from datetime import datetime

# Step 1: Reading the Data
def read_ping_data(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return lines

# Step 2: Parsing the Data
def parse_ping_data(lines):
    timestamps = []
    for line in lines:
        try:
            timestamp_str = line.split()[0] + " " + line.split()[1]
            timestamp = datetime.strptime(timestamp_str, '%Y%m%d %H:%M:%S')
            timestamps.append(timestamp)
        except ValueError:
            # Handle lines that do not match expected format
            continue
    return timestamps

# Step 3: Detecting Packet Drops
def detect_packet_drops(timestamps, threshold_seconds=1):
    packet_drops = []
    for i in range(1, len(timestamps)):
        delta = (timestamps[i] - timestamps[i-1]).total_seconds()
        if delta > threshold_seconds:
            # Add information about the packet drop
            packet_drops.append({
                'index': i,
                'timestamp': timestamps[i].strftime('%Y%m%d %H:%M:%S'),
                'delay': delta
            })
    return packet_drops

# Step 4: Saving Packet Drops to File
def save_packet_drops(packet_drops, output_file_path):
    with open(output_file_path, 'w') as file:
        file.write("Packet drops detected:\n")
        for drop in packet_drops:
            drop_info = f"At index {drop['index']} (Timestamp: {drop['timestamp']}), Delay: {drop['delay']} seconds\n"
            file.write(drop_info)
            print(drop_info)  # Print the drop information while saving it

# Putting it all together
file_path = 'ping.txt'
output_file_path = 'packet_drops.txt'

lines = read_ping_data(file_path)
timestamps = parse_ping_data(lines)
packet_drops = detect_packet_drops(timestamps, threshold_seconds=1)  # Threshold set to 1 second
save_packet_drops(packet_drops, output_file_path)

print(f"Packet drops detected and saved to {output_file_path}")
