import csv
import os
from datetime import datetime

USERS_FILE = 'users.csv'
ATTENDANCE_FILE = 'attendance.csv'

def init_db():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['MAC_Address', 'Name'])
            
    if not os.path.exists(ATTENDANCE_FILE):
        with open(ATTENDANCE_FILE, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['MAC_Address', 'Name', 'Date', 'Time'])

def load_users():
    users = {}
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                users[row['MAC_Address'].upper()] = row['Name']
    return users

def register_user(mac_address, name):
    mac_address = mac_address.upper()
    users = load_users()
    if mac_address in users:
        return False, "MAC address already registered."
    
    with open(USERS_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([mac_address, name])
    return True, "User registered successfully."

def has_attended_today(mac_address):
    mac_address = mac_address.upper()
    today = datetime.now().strftime('%Y-%m-%d')
    if os.path.exists(ATTENDANCE_FILE):
        with open(ATTENDANCE_FILE, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['MAC_Address'] == mac_address and row['Date'] == today:
                    return True
    return False

def mark_attendance(mac_address, name):
    mac_address = mac_address.upper()
    if has_attended_today(mac_address):
        return False, "Attendance already marked for today."
    
    now = datetime.now()
    date_str = now.strftime('%Y-%m-%d')
    time_str = now.strftime('%H:%M:%S')
    
    with open(ATTENDANCE_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([mac_address, name, date_str, time_str])
    
    return True, f"Attendance marked for {name}."
