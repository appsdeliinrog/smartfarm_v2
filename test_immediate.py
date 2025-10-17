from license_manager import LicenseManager

lm = LicenseManager()

print("=== Generating Demo Key ===")
key, data = lm.generate_license_key('Demo Client', expiry_minutes=3)
print(f"Generated key: {key}")
print(f"Expires: {data['expires']}")

print("\n=== Immediate Validation ===")
is_valid, result = lm.validate_license_key(key, 'Demo Client')
print(f"Valid: {is_valid}")
print(f"Result: {result}")

# Let's also check the exact hash
clean_key = key.replace('AGRI-', '').replace('-', '')
print(f"\nClean key: {clean_key}")

import hashlib
from datetime import datetime
license_string = f"Demo Client|{data['expires']}|{lm.secret_key}"
expected_hash = hashlib.sha256(license_string.encode()).hexdigest()[:16].upper()
print(f"Expected hash: {expected_hash}")
print(f"Match: {clean_key == expected_hash}")
