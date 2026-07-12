import asyncio
from bleak import BleakScanner

async def discover_devices():
    print("Scanning for all nearby Bluetooth devices for 10 seconds...")
    print("Please make sure your target device (e.g., phone) has Bluetooth turned ON and is discoverable.")
    print("-" * 60)
    print(f"{'MAC Address':<20} | {'Device Name / Local Name':<30} | {'RSSI (Signal)'}")
    print("-" * 60)
    
    # return_adv=True returns a dict of {address: (BLEDevice, AdvertisementData)}
    devices = await BleakScanner.discover(timeout=10.0, return_adv=True)
    for address, (device, adv_data) in devices.items():
        name = device.name or adv_data.local_name or "Unknown Device"
        print(f"{address:<20} | {name:<30} | {adv_data.rssi} dBm")
        
    print("-" * 60)
    print("Scan complete. Identify your device from the list above by name or RSSI (closest device has strongest signal, e.g., -40 to -60 dBm).")

if __name__ == "__main__":
    asyncio.run(discover_devices())
