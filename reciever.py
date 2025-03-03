import asyncio
from bleak import BleakScanner

def rssi_to_distance(rssi):
    rssi_ref=-47 #Tune this value
    path_loss=3
    print('rssi', rssi)
    return 10 ** ((rssi_ref - rssi) / (10 * path_loss))

class Device:
    def __init__(self, signal_strength, time):
            self.signal_strength = signal_strength
            self.time = time


async def scan_for_device(duration: int, time: int, samples_per_second: int):
    print(f"Scanning for devices for {duration} seconds...")

    rssi_values = []

    for _ in range(samples_per_second):
        print("here")
        devices = await BleakScanner.discover(timeout=duration/samples_per_second)

        for device in devices:
            if device.name == device_name:
                rssi_values.append(device.rssi)
        
        await asyncio.sleep(0.05)

    if rssi_values:
        avg_rssi = sum(rssi_values) / len(rssi_values)
        print(f"Iteration {time + 1}: Avg RSSI = {avg_rssi:.2f}")
        signals.append(Device(avg_rssi, time))
    else:
        print(f"Iteration {time}: No device found.")


#Global variables
device_name = "Quinn"  
samples_per_second = 10
duration = 1 #Total time to scan for devices in each iteration
signals = []
total_time = 10


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

for time_period in range(total_time):

    loop.run_until_complete(scan_for_device(duration, time_period, samples_per_second)) 



signals_with_distance = [rssi_to_distance(signal.signal_strength) for signal in signals]

for signal in signals_with_distance:
    print(f"Estimated distance: {signal:.2f} meters")
