import asyncio
from bleak import BleakScanner

class Device:
    def __init__(self, signal_strength, time):
            self.signal_strength = signal_strength
            self.time = time


async def scan_for_device(duration: int, time: int):
    print(f"Scanning for devices for {duration} seconds...")
    
    for _ in range(10):  
        devices = await BleakScanner.discover()

        for device in devices:
            if device.name == device_name:
                signals.append(device.rssi)
        
        await asyncio.sleep(0.01)  

# Global variables
device_name = "Quinn"  
samples_per_second = 10
duration = 1  # Total time to scan for devices in each iteration
signals = []
total_time = 20  # Total number of iterations

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

for time_period in range(total_time):
    loop.run_until_complete(scan_for_device(duration, time_period))

# Print all collected signal strengths
for signal in signals:
    print(f"Signal strength: {signal:.2f}")
