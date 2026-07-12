import asyncio
import sys
import database
import scanner

def print_menu():
    print("\n" + "="*30)
    print(" Bluetooth Attendance System")
    print("="*30)
    print("1. Register new device")
    print("2. View registered devices")
    print("3. Start attendance scanner")
    print("4. Exit")
    print("="*30)

def register_device():
    print("\n--- Register New Device ---")
    name = input("Enter Name/ID: ").strip()
    if not name:
        print("Name cannot be empty.")
        return
        
    mac = input("Enter Bluetooth MAC Address (e.g., 00:11:22:33:44:55): ").strip()
    if not mac:
        print("MAC Address cannot be empty.")
        return
        
    success, msg = database.register_user(mac, name)
    print(msg)

def view_devices():
    print("\n--- Registered Devices ---")
    users = database.load_users()
    if not users:
        print("No devices registered yet.")
    else:
        for mac, name in users.items():
            print(f"- {name}: {mac}")

async def main():
    database.init_db()
    
    while True:
        print_menu()
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == '1':
            register_device()
        elif choice == '2':
            view_devices()
        elif choice == '3':
            try:
                await scanner.run_scanner()
            except KeyboardInterrupt:
                print("\nReturned to main menu.")
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nExited.")
        sys.exit(0)
