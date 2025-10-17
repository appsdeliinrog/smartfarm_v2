"""
License Key Generator for Agri-Open System
Use this script to generate license keys for your clients
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from license_manager import LicenseManager

def main():
    print("🔑 AGRI-OPEN LICENSE KEY GENERATOR")
    print("="*50)
    
    lm = LicenseManager()
    
    while True:
        print("\nOptions:")
        print("1. Generate license key for client")
        print("2. Validate existing license key")
        print("3. Test license system")
        print("4. Exit")
        
        choice = input("\nSelect option (1-4): ").strip()
        
        if choice == '1':
            client_name = input("Enter client/organization name: ").strip()
            if not client_name:
                print("❌ Client name cannot be empty!")
                continue
            
            try:
                days = int(input("License validity (days, default 365): ") or "365")
            except ValueError:
                days = 365
            
            key, data = lm.generate_license_key(client_name, days)
            
            print(f"\n✅ LICENSE KEY GENERATED")
            print(f"📋 Client: {client_name}")
            print(f"🔑 License Key: {key}")
            print(f"📅 Valid until: {data['expires'][:10]}")
            print(f"⏰ Duration: {days} days")
            
            # Save to file for record keeping
            with open('generated_licenses.txt', 'a', encoding='utf-8') as f:
                f.write(f"{data['issued'][:10]} | {client_name} | {key} | {data['expires'][:10]}\n")
            
            print(f"📝 Record saved to generated_licenses.txt")
            
        elif choice == '2':
            license_key = input("Enter license key to validate: ").strip().upper()
            client_name = input("Enter client name: ").strip()
            
            is_valid, result = lm.validate_license_key(license_key, client_name)
            
            if is_valid:
                print(f"✅ License is VALID")
                print(f"📅 Expires: {result.strftime('%Y-%m-%d')}")
            else:
                print(f"❌ License is INVALID: {result}")
                
        elif choice == '3':
            print("\n🧪 TESTING LICENSE SYSTEM")
            
            # Generate test key
            test_key, test_data = lm.generate_license_key("Test Client", 30)
            print(f"Generated test key: {test_key}")
            
            # Validate test key
            is_valid, result = lm.validate_license_key(test_key, "Test Client")
            print(f"Validation result: {'✅ Valid' if is_valid else '❌ Invalid'}")
            
            # Test wrong client name
            is_valid2, result2 = lm.validate_license_key(test_key, "Wrong Client")
            print(f"Wrong client test: {'❌ Should be invalid' if not is_valid2 else '⚠️ Problem detected'}")
            
            print("🧪 Test completed")
            
        elif choice == '4':
            print("👋 Goodbye!")
            break
            
        else:
            print("❌ Invalid option. Please select 1-4.")

if __name__ == "__main__":
    main()
