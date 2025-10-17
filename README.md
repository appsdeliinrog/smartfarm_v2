# Tanzania Crop Price Monitoring System - Setup Guide

## 🏠 Setting Up on Your Home PC

Follow these steps to set up the project on your home computer.

---

## 📋 Prerequisites

### Required Software:
- **Python 3.8+** (Download from [python.org](https://python.org))
- **Node.js 16+** (Download from [nodejs.org](https://nodejs.org))
- **Git** (Download from [git-scm.com](https://git-scm.com))

### Optional but Recommended:
- **VS Code** (Code editor)
- **Postman** (API testing)

---

## 🚀 Project Setup Instructions

### 1. **Clone/Copy the Project**
```bash
# If using Git (recommended)
git clone <your-repository-url>
cd agri-open

# OR if copying files manually, navigate to project folder
cd agri-open
```

### 2. **Backend Setup (Django)**

#### Create Python Virtual Environment:
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

#### Install Python Dependencies:
```bash
# Install all required packages
pip install -r requirements.txt
```

#### Database Setup:
```bash
# Apply database migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser
```

#### Import Sample Data:
```bash
# Import the PDF data (if you have the PDF files)
python manage.py import_pdf path/to/your/pdf/file.pdf
```

### 3. **Frontend Setup (React + Vite)**

#### Navigate to frontend directory:
```bash
cd frontend
```

#### Install Node.js Dependencies:
```bash
# Install all frontend packages
npm install
```

#### Install Additional Dependencies (if needed):
```bash
# Tailwind CSS (should already be in package.json)
npm install -D tailwindcss postcss autoprefixer

# Chart library
npm install recharts

# HTTP client
npm install axios
```

---

## 🏃‍♂️ Running the Application

### Start Backend Server:
```bash
# From project root directory
# Make sure virtual environment is activated
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Start Django development server
python manage.py runserver
```
The backend will be available at: `http://127.0.0.1:8000`

### Start Frontend Server:
```bash
# In a new terminal, navigate to frontend directory
cd frontend

# Start Vite development server
npm run dev
```
The frontend will be available at: `http://localhost:5173` (or another port if 5173 is busy)

---

## 🔧 Project Structure

```
agri-open/
├── 📁 backend/
│   ├── agri_open/          # Django project settings
│   ├── crops/              # Main Django app
│   ├── manage.py           # Django management script
│   └── db.sqlite3          # Database file
├── 📁 frontend/
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── hooks/          # Custom React hooks
│   │   ├── utils/          # Utility functions
│   │   └── api.js          # API configuration
│   ├── package.json        # Node.js dependencies
│   └── vite.config.js      # Vite configuration
├── requirements.txt        # Python dependencies
├── nextplan.md            # Development roadmap
└── README.md              # This file
```

---

## 🗂️ Important Files

### Backend Configuration:
- `agri_open/settings.py` - Django settings
- `crops/models.py` - Database models
- `crops/views.py` - API endpoints
- `crops/serializers.py` - API serializers

### Frontend Configuration:
- `frontend/src/api.js` - API base configuration
- `frontend/src/App.jsx` - Main React component
- `frontend/tailwind.config.js` - Tailwind CSS configuration

---

## 🛠️ Common Issues & Solutions

### Issue: "Python not found"
**Solution:** Make sure Python is installed and added to PATH

### Issue: "npm not found"
**Solution:** Install Node.js which includes npm

### Issue: "Module not found" errors
**Solution:** 
```bash
# For Python modules
pip install -r requirements.txt

# For Node modules
cd frontend && npm install
```

### Issue: Port already in use
**Solution:**
```bash
# For Django (try different port)
python manage.py runserver 8001

# For Vite (it usually auto-selects available port)
npm run dev
```

### Issue: CORS errors
**Solution:** Make sure both servers are running and check `agri_open/settings.py` for CORS configuration

---

## 📊 Verify Setup

### Test Backend:
1. Open `http://127.0.0.1:8000/api/commodities/` in browser
2. Should see JSON response with commodities data

### Test Frontend:
1. Open `http://localhost:5173` in browser
2. Should see the Tanzania Crop Price Monitor dashboard

### Test Integration:
1. Select a commodity in the frontend dropdown
2. Price chart should load showing trend data
3. Price grid should show current prices

---

## 🔄 Development Workflow

### Daily Development:
1. **Start Backend:** `source .venv/bin/activate && python manage.py runserver`
2. **Start Frontend:** `cd frontend && npm run dev`
3. **Make Changes:** Edit files in your preferred editor
4. **Test Changes:** Both servers auto-reload on file changes

### Adding New Features:
1. **Backend:** Add to `crops/views.py`, `models.py`, `serializers.py`
2. **Frontend:** Add components in `frontend/src/components/`
3. **Test APIs:** Use Postman or browser to test API endpoints

---

## 📝 Next Steps

1. ✅ **Setup Complete** - Follow the setup instructions above
2. 🔍 **Explore Code** - Familiarize yourself with the codebase
3. 📈 **Review Plan** - Check `nextplan.md` for feature roadmap
4. 🚀 **Start Development** - Pick features from the next plan to implement

---

## 🆘 Need Help?

### Check These First:
1. Ensure all dependencies are installed
2. Verify both servers are running
3. Check browser console for error messages
4. Look at terminal output for error details

### Common Commands:
```bash
# Restart everything
# Terminal 1:
source .venv/bin/activate
python manage.py runserver

# Terminal 2:
cd frontend
npm run dev

# Update dependencies
pip install -r requirements.txt
cd frontend && npm install

# Reset database (if needed)
rm db.sqlite3
python manage.py migrate
```

---

## 🎯 Current Features

- ✅ **PDF Data Import** - Parse Ministry PDF reports
- ✅ **REST API** - Complete Django REST Framework setup
- ✅ **Interactive Dashboard** - Real-time price monitoring
- ✅ **Price Charts** - Historical trend visualization
- ✅ **Market Filtering** - Filter by commodity, region, market
- ✅ **Unit Conversion** - Toggle between kg and 100kg pricing
- ✅ **Responsive Design** - Works on mobile and desktop

Ready to continue development with the features outlined in `nextplan.md`! 🚀
