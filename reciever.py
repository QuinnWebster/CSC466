import asyncio
from bleak import BleakScanner

device_address = "XX:XX:XX:XX:XX:XX"  # Replace with the address of the device we are looking for
device_name = "Quinn"  # Replace with your device's name


def rssi_to_distance(rssi):
    rssi_ref=-42
    path_loss=2.5
    print('rssi', rssi)
    return 10 ** ((rssi_ref - rssi) / (10 * path_loss))


class Device:
    def __init__(self, signal_strength, time):
            self.signal_strength = signal_strength
            self.time = time

signals = []

# Scan for the device for a specified duration
async def scan_for_device(duration: int, time: int):
    print(f"Scanning for devices for {duration} seconds...")

    devices = await BleakScanner.discover(timeout=duration) 
    
    for device in devices:
        # Check if the device name matches
        if device.name == device_name:
            # Directly access rssi to avoid the error
            # print(f"Found device: {device.name} - {device.address} - RSSI value (essentially distance) {device.rssi}")
            signals.append(Device(device.rssi, time))




# Create a new event loop and set it
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# Run the scan for 3 seconds

for i in range(5):

    loop.run_until_complete(scan_for_device(1, i)) 

for signal in signals:
    print(signal.signal_strength)

signals_with_distance = [rssi_to_distance(signal.signal_strength) for signal in signals]

print(signals_with_distance)