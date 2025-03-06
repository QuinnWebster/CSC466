import asyncio
from bleak import BleakScanner


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
    signals = []
    num_times = 20  # Total number of iterations

    for _ in range(num_times):
        rssi = await scan_for_device(5, device_name)
        signals.append(rssi)

    print(signals)


# Run the script
if __name__ == "__main__":
    asyncio.run(main())
