import asyncio
from bleak import BleakScanner


async def scan_for_device(duration_sec: int, device_name):
    print(f"Scanning for devices for {duration_sec} seconds...")
    devices = await BleakScanner.discover(timeout=duration_sec)

    for device in devices:
        if device.name == device_name:
            print(
                f"Found device: {device.name} - {device.address} - RSSI: {device.rssi}"
            )
            return device.rssi
    return None


# Find the reference RSSI value at 1 unit distance
async def find_reference_rssi(device_name):
    print(
        "Place the device 1 unit distance away and press Enter to start scanning for RSSI..."
    )
    input("Press Enter when ready to scan...")

    rssi_values = []
    for _ in range(10):  # Scan 10 times
        rssi = await scan_for_device(duration_sec=2, device_name=device_name)
        if rssi is not None:
            rssi_values.append(rssi)
        else:
            print("Device not found!")
        await asyncio.sleep(2)

    if rssi_values:
        avg_rssi = sum(rssi_values) / len(rssi_values)
        print(f"Average RSSI at 1 unit distance: {avg_rssi:.2f}")
    else:
        print("No valid RSSI readings found!")


def main():
    device_name = "Quinn"

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Find the reference RSSI at 1 unit distance
    loop.run_until_complete(find_reference_rssi(device_name))


if __name__ == "__main__":
    main()
