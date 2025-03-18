# CSC466

Our team github for our CSC 466 group project

## Tracking Bluetooth Device

1. Run `python tuning.py`
   - This gets the RSSI value per unit distance (Place laptop next to Bluetooth device at 1 unit distance.)
2. Run `python reciever.py`
   - This starts tracking RSSI values emmited by the Bluetooth device
   - Results are put into `results.json`
3. Run `python plotting.py`
   - Copy paste the data from `results.json` from all three tracking devices into `main()` of `plotting.py`
   - The plots the final triangulated results from tracking
