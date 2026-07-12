import asyncio
from bleak import BleakScanner
import database

async def scan_and_mark(duration=5.0):
    print(f"Scanning for {duration} seconds...")
    devices = await BleakScanner.discover(timeout=duration)
    
    users = database.load_users()
    
    found_registered = False
    for device in devices:
        mac = device.address.upper()
        if mac in users:
            found_registered = True
            name = users[mac]
            success, msg = database.mark_attendance(mac, name)
            if success:
                print(f"[ATTENDANCE MARKED] {name} ({mac}) at {database.datetime.now().strftime('%H:%M:%S')}")
            else:
                # Already marked today
                pass
                
    if not found_registered:
        print("No registered devices found during this scan.")

async def run_scanner(interval=10.0, scan_duration=5.0):
    print("Scanner started. Press Ctrl+C to stop.")
    try:
        while True:
            await scan_and_mark(duration=scan_duration)
            print(f"Waiting for {interval} seconds before next scan...")
            await asyncio.sleep(interval)
    except asyncio.CancelledError:
        print("Scanner stopped.")
