# CSC466

Our team github for our CSC 466 group project

## Tracking Bluetooth Device

1. Run `python find_reference.py`
   - This gets the RSSI value per unit distance (Place laptop next to Bluetooth device at 1 unit distance.)
   - Note down the unit RSSI value.
2. Run `python reciever.py`
   - This starts tracking RSSI values emmited by the Bluetooth device
   - Results are put into `results.json`
3. Run `python plotting.py`
   - Copy paste the data from `results.json` from all three tracking devices into `distances_a`, `distances_b`, and `distances_c`
   - Input each device's `UNIT_RSSI_A`, `UNIT_RSSI_B`, and `UNIT_RSSI_c`
   - Adjust the expected path's points with array `expected_path`
   - This plots the final triangulated results from tracking
