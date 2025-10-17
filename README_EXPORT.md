# Tanzania Crop Price Monitoring System

A comprehensive web application for monitoring and analyzing crop prices across Tanzania's markets, featuring AI-powered predictions and smart commodity matching.

## 🎯 Project Overview

This system provides real-time monitoring of wholesale crop prices from Ministry of Agriculture reports, with features including:

- **📊 Interactive Dashboard** - Real-time price monitoring and market analytics
- **🤖 AI Predictions** - Machine learning-powered price forecasting with confidence intervals
- **📄 PDF Processing** - Automated extraction of price data from government reports
- **🔍 Smart Commodity Matching** - Intelligent normalization to prevent duplicate commodities
- **📈 Price Trend Analysis** - Historical data visualization and market comparisons
- **🎯 Best Price Finder** - Identify optimal markets for buying/selling

## 🏗️ Technical Architecture

### Backend (Django REST API)
- **Framework**: Django 5.2.5 + Django REST Framework
- **Database**: SQLite (development) / PostgreSQL (production ready)
- **Features**: PDF parsing, price data normalization, RESTful API endpoints
- **Smart Matching**: Fuzzy matching algorithm for commodity name normalization

### Frontend (React SPA)
- **Framework**: React 18 + Vite
- **Styling**: Tailwind CSS
- **Charts**: Chart.js for data visualization
- **Features**: Responsive design, real-time filtering, interactive dashboards

### Key Components
- **PDF Parser** (`fixed_parser.py`) - Extracts structured data from Ministry reports
- **Commodity Matching** (`commodity_matching.py`) - Prevents duplicate commodities
- **Price Prediction** - AI models for forecasting price trends
- **Admin Interface** - Django admin for data management

## 🚀 Quick Setup

### Prerequisites
- Python 3.10+
- Node.js 16+
- npm or yarn

### Backend Setup
```bash
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Run database migrations
python manage.py migrate

# 3. Create superuser (optional)
python manage.py createsuperuser

# 4. Start development server
python manage.py runserver
```

### Frontend Setup
```bash
# 1. Navigate to frontend directory
cd frontend

# 2. Install dependencies
npm install

# 3. Start development server
npm run dev
```

### Access the Application
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000/api
- **Django Admin**: http://localhost:8000/admin

## 📋 Features Implemented

### ✅ Core Functionality
- [x] PDF upload and automated parsing
- [x] Price data extraction and validation
- [x] Smart commodity name normalization
- [x] Real-time dashboard with filtering
- [x] Price trend visualization
- [x] Market comparison tools
- [x] Best price identification

### ✅ Advanced Features
- [x] AI-powered price predictions (BETA)
- [x] Confidence intervals for forecasts
- [x] Smart alerts for price changes
- [x] Responsive mobile design
- [x] Export capabilities
- [x] Data quality management

### ✅ Data Management
- [x] Automated duplicate detection
- [x] Commodity consolidation tools
- [x] Bulk data import/export
- [x] Data validation and cleaning
- [x] Historical data preservation

## 🗂️ Project Structure

```
agri-open/
├── backend/                    # Django project settings
├── crops/                      # Main Django app
│   ├── models.py              # Database models
│   ├── views.py               # API endpoints
│   ├── serializers.py         # Data serialization
│   ├── services.py            # Business logic
│   ├── commodity_matching.py  # Smart matching service
│   └── management/commands/   # Custom Django commands
├── frontend/                   # React application
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── pages/            # Page components
│   │   ├── hooks/            # Custom hooks
│   │   └── utils/            # Utility functions
│   └── public/               # Static assets
├── parser_poc/                # PDF parsing prototypes
├── fixed_parser.py            # Production PDF parser
├── requirements.txt           # Python dependencies
└── README.md                 # This file
```

## 📊 Data Sources

The system processes official wholesale price reports from:
- **Ministry of Agriculture, Tanzania**
- **Regional Market Information Systems**
- **Commodity Exchange Authorities**

### Supported Commodities
- Beans (Maharage)
- Rice (Mchele)
- Maize (Mahindi)
- Wheat Grain (Ngano)
- Sorghum (Mtama)
- Finger Millet (Ulezi)
- Bulrush Millet (Uwele)
- Irish Potatoes (Viazi Mviringo)

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the root directory:
```
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
```

### API Endpoints
- `GET /api/commodities/` - List all commodities
- `GET /api/price-observations/latest/` - Latest prices
- `GET /api/price-observations/trends/` - Price trends
- `GET /api/price-observations/best_prices/` - Best prices by commodity
- `POST /api/uploads/` - Upload PDF files

## 🧪 Testing & Validation

### Run Tests
```bash
# Backend tests
python manage.py test

# Test smart commodity matching
python manage.py test_smart_matching

# Preview commodity normalizations
python manage.py preview_commodity_matching --upload-id 1
```

### Data Validation
```bash
# Check data integrity
python debug_commodity_data.py

# Validate import process
python manage.py import_prices --dry-run
```

## 🎯 Usage Examples

### Upload and Process PDF
1. Access Django admin at `/admin`
2. Navigate to "PDF Uploads"
3. Upload a Ministry report PDF
4. System automatically parses and imports data
5. View results in the dashboard

### Smart Commodity Matching
The system automatically normalizes commodity names:
- "Beans (Maharage)" → "Beans" with Swahili name "Maharage"
- "beans" → "Beans" (case-insensitive matching)
- "Rice (Mchele)" → "Rice" with Swahili name "Mchele"

### Price Predictions
1. Select a commodity in the dashboard
2. Enable "Show AI Predictions"
3. View 14-day forecasts with confidence intervals
4. Analyze seasonal patterns and trends

## 🚀 Deployment

### Production Considerations
- Switch to PostgreSQL database
- Configure proper SECRET_KEY
- Set DEBUG=False
- Configure static file serving
- Set up proper logging
- Enable HTTPS
- Configure CORS settings

### Docker Deployment (Optional)
```dockerfile
# Example Dockerfile structure
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

## 🤝 Contributing

This is a Final Year Project (FYP) for Agricultural Technology. For contributions or questions:

1. Follow Django and React best practices
2. Maintain data quality and validation
3. Test thoroughly before deploying
4. Document any new features

## 📄 License

Academic project - Please credit the original authors when using or adapting this code.

## 🙏 Acknowledgments

- **Ministry of Agriculture, Tanzania** - Data sources
- **University Supervisors** - Guidance and support
- **Open Source Community** - Libraries and frameworks used

---

**Built with ❤️ for Tanzania's Agricultural Markets**

*Last Updated: August 2025*
