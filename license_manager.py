"""
License management system for the agri-open project
Handles watermark display and license key validation
"""
import hashlib
import json
from datetime import datetime, timedelta
from pathlib import Path

class LicenseManager:
    """Manages license keys and watermark display"""
    
    def __init__(self):
        self.license_file = Path('license.json')
        self.secret_key = "agri-open-tanzania-2025"  # Change this for production
        
    def generate_license_key(self, client_name, expiry_days=365, expiry_minutes=None):
        """Generate a license key for a client"""
        if expiry_minutes:
            expiry_date = (datetime.now() + timedelta(minutes=expiry_minutes)).isoformat()
        else:
            expiry_date = (datetime.now() + timedelta(days=expiry_days)).isoformat()
        
        # Create license data
        license_data = {
            'client': client_name,
            'issued': datetime.now().isoformat(),
            'expires': expiry_date,
            'features': ['dashboard', 'analytics', 'pdf_upload', 'ai_predictions']
        }
        
        # Create hash for validation
        license_string = f"{client_name}|{expiry_date}|{self.secret_key}"
        license_hash = hashlib.sha256(license_string.encode()).hexdigest()[:16].upper()
        
        license_key = f"AGRI-{license_hash[:4]}-{license_hash[4:8]}-{license_hash[8:12]}-{license_hash[12:16]}"
        
        return license_key, license_data
    
    def validate_license_key(self, license_key, client_name):
        """Validate if a license key is correct for the client"""
        try:
            # First check if this is a demo key
            demo_file = Path('demo_keys.json')
            if demo_file.exists():
                try:
                    with open(demo_file, 'r') as f:
                        demo_keys = json.load(f)
                    
                    for demo in demo_keys:
                        if demo['key'] == license_key and demo['client'] == client_name:
                            expiry_date = datetime.fromisoformat(demo['expires'])
                            if datetime.now() < expiry_date:
                                return True, expiry_date
                            else:
                                return False, "License expired"
                except Exception as e:
                    print(f"Demo key validation error: {e}")
            
            # Remove dashes and prefix for standard validation
            clean_key = license_key.replace('AGRI-', '').replace('-', '')
            current_date = datetime.now()
            
            # Check keys issued up to 2 years ago (standard licenses)
            for days_ago in range(0, 730):
                issue_date = current_date - timedelta(days=days_ago)
                expiry_date = issue_date + timedelta(days=365)
                
                license_string = f"{client_name}|{expiry_date.isoformat()}|{self.secret_key}"
                expected_hash = hashlib.sha256(license_string.encode()).hexdigest()[:16].upper()
                
                if clean_key == expected_hash:
                    # Check if not expired
                    if datetime.now() < expiry_date:
                        return True, expiry_date
                    else:
                        return False, "License expired"
            
            return False, "Invalid license key"
            
        except Exception as e:
            return False, f"License validation error: {str(e)}"
    
    def save_license(self, license_key, client_name):
        """Save activated license to file"""
        is_valid, result = self.validate_license_key(license_key, client_name)
        
        if is_valid:
            license_info = {
                'key': license_key,
                'client': client_name,
                'activated': datetime.now().isoformat(),
                'expires': result.isoformat(),
                'status': 'active'
            }
            
            with open(self.license_file, 'w') as f:
                json.dump(license_info, f, indent=2)
            
            return True, "License activated successfully"
        else:
            return False, result
    
    def get_license_status(self):
        """Get current license status - License system disabled"""
        # License system disabled - always return licensed status
        return {
            'licensed': True,
            'trial': False,
            'client': 'System User',
            'expires': None,
            'message': 'Licensed Version'
        }
    
    def remove_license(self):
        """Remove license file (for testing)"""
        if self.license_file.exists():
            self.license_file.unlink()
            return True
        return False

# Example usage and key generation
if __name__ == "__main__":
    lm = LicenseManager()
    
    # Generate some example license keys
    print("=== LICENSE KEY GENERATOR ===")
    
    clients = ["Tanzania Ministry of Agriculture", "Dodoma Regional Office", "Arusha Market Authority"]
    
    for client in clients:
        key, data = lm.generate_license_key(client)
        print(f"\nClient: {client}")
        print(f"License Key: {key}")
        print(f"Valid until: {data['expires'][:10]}")
        
        # Test validation
        is_valid, result = lm.validate_license_key(key, client)
        print(f"Validation: {'✅ Valid' if is_valid else '❌ Invalid'}")
