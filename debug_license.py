from license_manager import LicenseManager
from datetime import datetime, timedelta
import hashlib

lm = LicenseManager()

# Test the exact key we got from the API
test_key = "AGRI-0717-7BD6-F606-900C"
client_name = "Demo Client"

print(f"Testing key: {test_key}")
print(f"Client: {client_name}")

# Clean the key
clean_key = test_key.replace('AGRI-', '').replace('-', '')
print(f"Clean key: {clean_key}")

# Try to reverse engineer what time this key was created
current_time = datetime.now()
print(f"Current time: {current_time}")

# Try different times around now
for minutes_back in range(0, 10):
    test_issue_time = current_time - timedelta(minutes=minutes_back)
    test_expiry_time = test_issue_time + timedelta(minutes=3)
    
    license_string = f"{client_name}|{test_expiry_time.isoformat()}|{lm.secret_key}"
    expected_hash = hashlib.sha256(license_string.encode()).hexdigest()[:16].upper()
    
    print(f"Minutes back: {minutes_back}, Hash: {expected_hash}, Match: {clean_key == expected_hash}")
    
    if clean_key == expected_hash:
        print(f"FOUND MATCH! Issue time: {test_issue_time}, Expiry: {test_expiry_time}")
        print(f"Is expired? {current_time > test_expiry_time}")
        break
