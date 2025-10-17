# License Management System Documentation

## 🔐 Overview

The Tanzania Crop Price Monitoring System includes a built-in licensing system that allows you to monetize your software by requiring clients to purchase license keys to remove watermarks and fully use the system.

## 🎯 How It Works

### For Unlicensed Users (Trial Mode):
- Red banner appears at the top: "Trial Version - Activate License to Remove Watermark"
- Semi-transparent watermarks overlay the entire interface
- All functionality works, but the watermarks indicate unlicensed use
- Users can click "Activate License" to enter their license key

### For Licensed Users:
- No watermarks or banners
- Clean, professional interface
- Full access to all features

## 🔑 License Key System

### Key Format:
```
AGRI-XXXX-XXXX-XXXX-XXXX
```

### Security Features:
- Keys are generated using SHA-256 hashing
- Keys are tied to specific client/organization names
- Expiration dates are built into the key validation
- Cannot be reverse-engineered or guessed

## 💰 Monetization Workflow

### 1. Client Contact
When clients want to purchase the system:
1. They download/receive the trial version
2. They see the watermarks and licensing message
3. They contact you for a license

### 2. License Generation
Use the license generator script:
```bash
python generate_license_keys.py
```

Options:
- Generate license key for specific client
- Set custom expiration (default: 365 days)
- Validate existing keys
- Test the system

### 3. Key Delivery
Provide the client with:
- Their unique license key (AGRI-XXXX-XXXX-XXXX-XXXX)
- Setup instructions
- Their exact organization name (must match for validation)

### 4. Client Activation
Client activates by:
1. Clicking "Activate License" in the red banner
2. Entering their organization name exactly as provided
3. Entering the license key
4. System validates and removes watermarks

## 🛠️ Technical Implementation

### Backend Components:
- `license_manager.py` - Core license generation and validation
- `crops/license_views.py` - Django API endpoints
- License status API endpoints for frontend

### Frontend Components:
- `Watermark.jsx` - Displays watermarks and license activation
- `LicenseAdmin.jsx` - Admin panel for testing
- License status checking and activation forms

### API Endpoints:
- `GET /api/license/status/` - Check current license status
- `POST /api/license/activate/` - Activate a license key
- `DELETE /api/license/deactivate/` - Remove license (for testing)
- `GET /api/license/demo-key/` - Generate demo keys (remove in production)

## 📋 License Generator Usage

### Generate a License:
```bash
python generate_license_keys.py
```

Select option 1, then:
- Enter client name: "Tanzania Ministry of Agriculture"
- Enter validity days: 365 (or custom)
- Receive generated key: AGRI-1A2B-3C4D-5E6F-7G8H

### Example Generated Keys:
```
Client: Tanzania Ministry of Agriculture
Key: AGRI-4F2A-8B9E-1C7D-3E6F
Valid: 365 days

Client: Dodoma Regional Office  
Key: AGRI-7B3F-2A8E-9C1D-5F4A
Valid: 365 days
```

## 💼 Business Model Suggestions

### Pricing Tiers:
1. **Basic License** - $500/year
   - Single organization use
   - Standard features
   - Email support

2. **Regional License** - $1,500/year  
   - Multi-location use within region
   - All features + custom branding
   - Priority support

3. **Enterprise License** - $3,000/year
   - Nationwide deployment
   - Custom features + integrations
   - Dedicated support

### License Terms:
- Annual licensing (renewable)
- Tied to organization name
- Non-transferable
- Includes updates and support

## 🔧 Customization

### Change Contact Information:
Edit `frontend/src/components/Watermark.jsx`:
```jsx
<p>Email: your-email@domain.com</p>
<p>Phone: +255-XXX-XXX-XXX</p>
```

### Modify Watermark Text:
Edit the watermark messages in `Watermark.jsx`:
```jsx
<div className="text-6xl font-bold mb-4 text-center">
  YOUR CUSTOM TEXT
</div>
```

### Adjust License Validity:
In `license_manager.py`, change default days:
```python
def generate_license_key(self, client_name, expiry_days=365):
```

### Change Secret Key:
⚠️ **Important**: Change the secret key in production:
```python
self.secret_key = "your-unique-secret-key-2025"
```

## 🚀 Deployment Considerations

### For Production:
1. **Remove Demo Features**:
   - Remove `/license-admin` route
   - Remove demo key generation endpoint
   - Remove LicenseAdminPage component

2. **Secure the System**:
   - Change the secret key in `license_manager.py`
   - Add rate limiting to license endpoints
   - Log license activation attempts

3. **License File Location**:
   - Ensure `license.json` is writable by the web server
   - Consider database storage for multi-server deployments

### File Locations:
```
license.json          # Stores active license (auto-created)
generated_licenses.txt # Your record of issued licenses
```

## 📞 Client Support

### Common Issues:
1. **"Invalid license key"**
   - Check client name spelling (case-sensitive)
   - Verify key wasn't corrupted in transmission
   - Confirm key hasn't expired

2. **"License expired"**
   - Generate new key with extended validity
   - Client needs to re-activate

3. **Cannot activate**
   - Check internet connection
   - Verify API endpoints are accessible
   - Check browser console for errors

### Support Script:
```bash
# Check client's license status
python -c "
from license_manager import LicenseManager
lm = LicenseManager()
print(lm.get_license_status())
"
```

## 📈 Success Tracking

The system automatically logs:
- License activation attempts
- Generated license keys (in `generated_licenses.txt`)
- Active license status

Monitor these to track:
- Conversion from trial to paid
- License renewals needed
- Popular client types

---

**This licensing system provides a professional, secure way to monetize your Tanzania Crop Price Monitoring System while maintaining a great user experience for paying clients.** 🇹🇿💚
