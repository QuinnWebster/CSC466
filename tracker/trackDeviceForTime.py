import asyncio
from bleak import BleakScanner

RSSI_UNIT = -56  # Tune this value to rssi value at one unit distance
PATH_LOSS = 2.9  # Higher value for more noisy room


# Convert RSSI to distance in unit distance
def rssi_to_distance(rssi):
    rssi_ref = RSSI_UNIT
    path_loss = PATH_LOSS
    print("rssi", rssi)
    return 10 ** ((rssi_ref - rssi) / (10 * path_loss))


# Smoothing the RSSI values
class EMAFilter:
    def __init__(self, alpha: float):
        self.alpha = alpha  # Smoothing factor between 0 and 1
        self.smoothed_value = None

    def update(self, rssi_value: float):
        if self.smoothed_value is None:
            self.smoothed_value = rssi_value
        else:
            self.smoothed_value = (
                self.alpha * rssi_value + (1 - self.alpha) * self.smoothed_value
            )
        return self.smoothed_value


# Initialize the EMA filter with a smoothing factor
EMA_FILTER = EMAFilter(alpha=0.1)  # Tweak alpha for faster/slower response


# Scan for devices and return the RSSI of the specific device
async def scan_for_device(duration_sec: int, device_name):
    devices = await BleakScanner.discover(timeout=duration_sec)

    for device in devices:
        # Check if the device name matches
        if device.name == device_name:
            print(
                f"Found device: {device.name} - {device.address} - RSSI: {device.rssi}"
            )
            return device.rssi
    return None


# Function to track the distance over 20 seconds, checking every 2 seconds
async def track_distance(device_name):
    for _ in range(10):  # We will scan 10 times (every 2 seconds for 20 seconds)
        rssi = await scan_for_device(duration_sec=2, device_name=device_name)

        if rssi is not None:
            smoothed_rssi = EMA_FILTER.update(rssi)
            distance = rssi_to_distance(smoothed_rssi)
            print(
                f"Smoothed RSSI: {smoothed_rssi}, Estimated Distance: {distance:.2f} meters"
            )
        else:
            print("Device not found!")
        await asyncio.sleep(2)


def main():
    device_name = "Quinn"

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(track_distance(device_name))


if __name__ == "__main__":
    main()
