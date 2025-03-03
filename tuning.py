import asyncio
from bleak import BleakScanner

def rssi_to_distance(rssi):
    rssi_ref = -47  # Tune this value
    path_loss = 3 #Higer value means more noisy room
    print('rssi', rssi)
    return 10 ** ((rssi_ref - rssi) / (10 * path_loss))

device_name = "Quinn"
rssi_values = []
samples_per_second = 5
duration = 1  # How long each scan will last
total_time = 5  # Total time to scan for

async def scan_for_device(duration: int, samples_per_second: int, total_time: int):
    q = 0
    for second in range(total_time):
        for _ in range(samples_per_second):
            devices = await BleakScanner.discover(timeout=duration / samples_per_second)
            for device in devices:
                if device.name == device_name:
                    rssi_values.append(device.rssi)
                    q += 1


# Run the async function and collect results
async def main():
    await scan_for_device(duration, samples_per_second, total_time)
    print(rssi_values)
    print(f"Average RSSI: {sum(rssi_values) / len(rssi_values)}")
    

# Run the script
asyncio.run(main())
