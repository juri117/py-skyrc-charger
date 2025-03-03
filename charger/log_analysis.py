

import csv
import datetime

from commands import get_cmd_start, Action, get_cmd_poll_vals, get_cmd_stop, Config, parse_data


line_count = 0
out = []
with open('logs/usb_data_2025-02-27_12-44-46.txt', 'r') as f:
    for line in f:
        parts = line.strip().split(':')
        if len(parts) != 2:
            continue

        time_str = parts[0].strip()
        hex_data = parts[1].strip()
        if not hex_data:
            continue

        try:
            data = bytes.fromhex(hex_data)
            result = parse_data(data)
            if result:
                result['time'] = time_str

                if line_count % 100 == 0:
                    out.append(result)
                    print(f"{parts[0]}: {result}")
        except ValueError:
            continue
        line_count += 1


# Write results to CSV
with open('log_output.csv', 'w', newline='') as csvfile:
    if len(out) > 0:
        # Get field names from first result dict
        fieldnames = list(out[0].keys())
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(out)
