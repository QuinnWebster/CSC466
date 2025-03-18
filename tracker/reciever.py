import asyncio
from bleak import BleakScanner
import json
import os

RESULT_PATH = "./results/results.json"


async def scan_for_device(num_times: int, device_name):

    print("Scanning for devices...")

    rssi_signals = []

    # Collect RSSI for the device multiple times in each iteration
    for _ in range(num_times):
        devices = await BleakScanner.discover(timeout=1 / num_times)

        for device in devices:
            if device.name == device_name:
                rssi_signals.append(device.rssi)

    if not rssi_signals:
        return None
    average_rssi = sum(rssi_signals) / len(rssi_signals)
    print(f"Average RSSI: {average_rssi}")
    return average_rssi


async def main():
    # Global variables
    device_name = "Quinn"
    rssi_signals = []
    num_times = 20  # Total number of iterations

    for _ in range(num_times):
        rssi = await scan_for_device(5, device_name)
        rssi_signals.append(rssi)

    # put results into json
    os.makedirs(os.path.dirname(RESULT_PATH), exist_ok=True)
    with open(RESULT_PATH, "w") as f:
        json.dump(rssi_signals, f)

    print("RSSI signals dumped into JSON at: ", RESULT_PATH)


# Run the script
if __name__ == "__main__":
    asyncio.run(main())
