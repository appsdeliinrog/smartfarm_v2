# 📦 Project Export Guide

## 🏠 What to Copy to Your Home PC

### ✅ **INCLUDE These Files/Folders:**
```
agri-open/
├── backend/               # Django backend code
├── crops/                 # Django app
├── frontend/              # React frontend code (without node_modules)
├── crop price pdf/        # PDF data files
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies ✅
├── README.md              # Setup instructions ✅
├── nextplan.md            # Development roadmap ✅
├── .gitignore             # Ignore file ✅
├── db.sqlite3             # Database (optional - can recreate)
└── *.py files             # All Python scripts
```

### ❌ **EXCLUDE These Folders (Large/Regenerable):**
```
❌ .venv/                  # Virtual environment (regenerate with pip)
❌ frontend/node_modules/  # Node dependencies (regenerate with npm)
❌ __pycache__/            # Python cache files
❌ *.pyc files             # Compiled Python files
```

---

## 📋 Quick Export Checklist

### Before Leaving Office:
- [x] ✅ Generated `requirements.txt`
- [x] ✅ Created `README.md` with setup instructions
- [x] ✅ Created `.gitignore` to exclude unnecessary files
- [x] ✅ Verified all source code is included

### Copy These Essential Files:
1. **All source code** (backend/, crops/, frontend/src/)
2. **Configuration files** (package.json, vite.config.js, settings.py)
3. **Documentation** (README.md, nextplan.md)
4. **Data files** (crop price pdf/, db.sqlite3)
5. **Dependencies list** (requirements.txt, package.json)

---

## 🚀 Setup on Home PC (Quick Steps)

### 1. Copy Project Files
```bash
# Copy entire project folder (excluding .venv and node_modules)
# Total size should be much smaller without these folders
```

### 2. Setup Python Environment
```bash
cd agri-open
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 3. Setup Frontend
```bash
cd frontend
npm install
```

### 4. Run the Project
```bash
# Terminal 1 (Backend)
python manage.py runserver

# Terminal 2 (Frontend)
cd frontend && npm run dev
```

---

## 💾 Estimated File Sizes

### With Heavy Folders (Don't Copy):
- `.venv/`: ~200-500 MB
- `frontend/node_modules/`: ~100-300 MB
- **Total**: ~500 MB+

### Without Heavy Folders (Copy This):
- Source code: ~5-10 MB
- PDF files: ~10-20 MB
- Database: ~5-10 MB
- **Total**: ~20-40 MB ✅

---

## ⚡ Pro Tips

### Use Git (Recommended):
```bash
# Initialize git repository
git init
git add .
git commit -m "Initial commit"

# Push to GitHub/GitLab for easy sync
```

### Manual Copy Alternative:
1. Zip the project folder (excluding .venv and node_modules)
2. Transfer via USB, cloud storage, or email
3. Unzip on home PC and follow setup instructions

### Quick Verification:
After setup, test these URLs:
- Backend: `http://127.0.0.1:8000/api/commodities/`
- Frontend: `http://localhost:5173`

---

## 🎯 Next Development Session

1. **Setup** (10 mins): Follow README.md instructions
2. **Verify** (5 mins): Test both frontend and backend
3. **Develop** (Rest of time): Implement features from nextplan.md

### First Feature to Implement:
Start with **Market Comparison Dashboard** from Phase 1.5 in nextplan.md - it will provide immediate value for traders!

---

## 📞 Emergency Recovery

If something goes wrong during setup:

### Backend Issues:
```bash
# Reset virtual environment
rm -rf .venv
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
```

### Frontend Issues:
```bash
# Reset node modules
rm -rf node_modules package-lock.json
npm install
```

### Database Issues:
```bash
# Reset database
rm db.sqlite3
python manage.py migrate
# Re-import data if needed
```

**You're all set! 🎉 The project is ready for transport and setup on your home PC.**
