from license_manager import LicenseManager

# Test license generation and validation
lm = LicenseManager()

print("=== Testing Demo License ===")
key, data = lm.generate_license_key('Demo Client', expiry_minutes=3)
print(f"Generated key: {key}")
print(f"Expires: {data['expires']}")

# Test validation
is_valid, result = lm.validate_license_key(key, 'Demo Client')
print(f"Validation result: {is_valid}")
print(f"Result details: {result}")

# Test with exact key from API
print("\n=== Testing API Key ===")
api_key = "AGRI-AC54-B826-DE91-E43E"
is_valid2, result2 = lm.validate_license_key(api_key, 'Demo Client')
print(f"API Key validation: {is_valid2}")
print(f"API Result details: {result2}")
