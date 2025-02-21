import asyncio
from bleak import BleakScanner

device_name = "Quinn"  # Replace with your device's name

# Function to scan for devices and return the RSSI of the specific device
async def scan_for_device(duration: int):
    print(f"Scanning for devices for {duration} seconds...")
    devices = await BleakScanner.discover(timeout=duration)  # Scan for the specified duration
    
    for device in devices:
        # Check if the device name matches
        if device.name == device_name:
            print(f"Found device: {device.name} - {device.address} - RSSI: {device.rssi}")
            return device.rssi
    return None  # Return None if the device wasn't found

# Function to find the reference RSSI value at 1 meter
async def find_reference_rssi():
    print("Place the device 1 meter away and press Enter to start scanning for RSSI...")
    input("Press Enter when ready to scan...")
    
    # Scan for the device multiple times (e.g., 10 times) to average the readings
    rssi_values = []
    for _ in range(10):  # Scan 10 times
        rssi = await scan_for_device(duration=2)  # Scan for 2 seconds each time
        if rssi is not None:
            rssi_values.append(rssi)
        else:
            print("Device not found!")
        await asyncio.sleep(2)  # Wait for 2 seconds before the next scan
    
    # Calculate the average RSSI from all the scans
    if rssi_values:
        avg_rssi = sum(rssi_values) / len(rssi_values)
        print(f"Average RSSI at 1 meter: {avg_rssi:.2f}")
    else:
        print("No valid RSSI readings found!")

# Create a new event loop and set it
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# Start the process to find the reference RSSI at 1 meter
loop.run_until_complete(find_reference_rssi())
