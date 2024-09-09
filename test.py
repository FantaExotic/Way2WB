import time
from datetime import datetime

msg = {'id': 'ASML', 'exchange': 'NMS', 'quoteType': 8, 'price': 766.75, 'timestamp': 1725882442000, 'marketHours': 0, 'changePercent': 1.8544378280639648, 'dayVolume': 0, 'change': 13.96002197265625, 'priceHint': 2}
# Convert the current time to milliseconds
current_timestamp_s = int(time.time())
current_timestamp_ms = int(time.time() * 1000)

# Convert both timestamps to datetime objects
msg_timestamp_s = msg['timestamp'] / 1000  # Convert msg timestamp to seconds
msg_datetime = datetime.fromtimestamp(msg_timestamp_s)

current_datetime = datetime.fromtimestamp(current_timestamp_ms / 1000)

# Validate if the msg timestamp is from today
is_same_day = msg_datetime.date() == current_datetime.date()

print(f"Is the timestamp from today? {is_same_day}")