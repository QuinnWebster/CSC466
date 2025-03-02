import asyncio
from bleak import BleakScanner

device_address = "XX:XX:XX:XX:XX:XX"  # Replace with the address of the device we are looking for
device_name = "Quinn"  # Replace with your device's name

samples_per_second = 10
duration = 1 #Total time to scan for devices in each iteration

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

async def scan_for_device(duration: int, time: int, samples_per_second: int):
    print(f"Scanning for devices for {duration} seconds...")

    rssi_values = []

    for _ in range(samples_per_second):
        devices = await BleakScanner.discover(timeout=duration/samples_per_second)

        for device in devices:
            if device.name == device_name:
                rssi_values.append(device.rssi)
        
        await asyncio.sleep(1/samples_per_second)

    if rssi_values:
        avg_rssi = sum(rssi_values) / len(rssi_values)
        print(f"Iteration {time}: Avg RSSI = {avg_rssi:.2f}")
        signals.append(Device(avg_rssi, time))
    else:
        print(f"Iteration {time}: No device found.")


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

for time_period in range(5):

    loop.run_until_complete(scan_for_device(duration, time_period, samples_per_second)) 

for signal in signals:
    print(signal.signal_strength)

signals_with_distance = [rssi_to_distance(signal.signal_strength) for signal in signals]

print(signals_with_distance)