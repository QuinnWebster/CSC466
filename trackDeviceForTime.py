import asyncio
from bleak import BleakScanner

device_name = "Quinn" 

# Convert RSSI to distance in meters
def rssi_to_distance(rssi):
    rssi_ref = -45.6  # Reference RSSI at 1m distance
    path_loss = 4   # Path loss exponent, adjust this param
    print('rssi', rssi)
    return 10 ** ((rssi_ref - rssi) / (10 * path_loss)) 


#Smoothing the RSSI values
class EMAFilter:
    def __init__(self, alpha: float):
        self.alpha = alpha  # Smoothing factor between 0 and 1
        self.smoothed_value = None
    
    def update(self, rssi_value: float):
        if self.smoothed_value is None:
            self.smoothed_value = rssi_value
        else:
            self.smoothed_value = self.alpha * rssi_value + (1 - self.alpha) * self.smoothed_value
        return self.smoothed_value

# Initialize the EMA filter with a smoothing factor
ema_filter = EMAFilter(alpha=0.1)  # Tweak alpha for faster/slower response

# Scan for devices and return the RSSI of the specific device
async def scan_for_device(duration: int):
    devices = await BleakScanner.discover(timeout=duration)  
    
    for device in devices:
        # Check if the device name matches
        if device.name == device_name:
            print(f"Found device: {device.name} - {device.address} - RSSI: {device.rssi}")
            return device.rssi
    return None

# Function to track the distance over 20 seconds, checking every 2 seconds
async def track_distance():
    for _ in range(10):  # We will scan 10 times (every 2 seconds for 20 seconds)
        rssi = await scan_for_device(duration=2)  # Scan for 2 seconds
        if rssi is not None:
            smoothed_rssi = ema_filter.update(rssi)  # Apply EMA smoothing
            distance = rssi_to_distance(smoothed_rssi)  # Convert RSSI to distance
            print(f"Smoothed RSSI: {smoothed_rssi}, Estimated Distance: {distance:.2f} meters")
        else:
            print("Device not found!")
        await asyncio.sleep(2)  # Wait for 2 seconds before the next scan

# Create a new event loop and set it
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# Start tracking the device's distance
loop.run_until_complete(track_distance())
