# Paytaca Map

A comprehensive merchant mapping application that displays BCH-accepting merchants that use Paytaca POS with integrated cashback campaign features. Built with Vue.js, Django, and Leaflet for an interactive map experience.

## 🌟 Features

### Core Functionality
- **Interactive Merchant Map**: Visual representation of BCH-accepting merchants worldwide
- **Merchant Search & Filtering**: Search by name, filter by country, city, category, and transaction history
- **Location-Based Services**: Find merchants near your current location (within 10km radius)
- **Responsive Design**: Optimized for both desktop and mobile devices

### Cashback Campaign Integration
- **Gift Icon Indicators**: Visual indicators for merchants with active cashback campaigns
- **Campaign Details Dialog**: Comprehensive information about cashback offers including:
  - Campaign type (One-Time Claim vs Regular)
  - Cashback percentages and limits
  - Transaction and customer limits
  - Merchant pool limits
- **Reservation System**: Reserve one-time claim campaigns for 6 hours
- **Real-time Exchange Rates**: BCH to local currency conversion using Watchtower API
- **Animated UI Elements**: Gift icon animations and smooth transitions

### Advanced Features
- **Merchant Verification Status**: Visual indicators for verified vs unverified merchants
- **Transaction History**: Last transaction timestamps with relative time display
- **Category Management**: Organized merchant categorization system
- **Google Maps Integration**: Direct links to merchant locations
- **Website Integration**: Direct links to merchant websites

## 🏗️ Architecture

### Frontend
- **Vue.js 3**: Modern reactive framework for building user interfaces
- **Tailwind CSS**: Utility-first CSS framework for responsive design
- **Leaflet.js**: Open-source mapping library for interactive maps
- **Axios**: HTTP client for API communication
- **Vite**: Fast build tool and development server

### Backend
- **Django**: Python web framework for backend services
- **Django REST Framework**: API development toolkit
- **PostgreSQL**: Primary database (configurable)
- **Nginx**: Web server and reverse proxy

### External APIs
- **Engagement Hub API**: Cashback campaign data
- **Watchtower API**: BCH exchange rates
- **OpenStreetMap**: Map tiles and geospatial data

## 🚀 Quick Start

### Prerequisites
- Node.js 16+ and npm
- Python 3.8+
- Docker and Docker Compose (optional)

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Backend Setup
```bash
# Install Python dependencies
pip install -r requirements.txt

# Run Django migrations
python manage.py migrate

# Start Django development server
python manage.py runserver
```

### Docker Setup (Recommended)
```bash
# Build and start all services
docker-compose up --build

# Run in background
docker-compose up -d
```

## 📱 Usage

### Finding Merchants
1. **Search**: Use the search bar to find merchants by name
2. **Filter**: Apply filters by country, city, category, or transaction history
3. **Location**: Click "Show Merchants Near Me" to find nearby merchants
4. **Browse**: Scroll through the merchant list or explore the interactive map

### Cashback Campaigns
1. **Identify**: Look for gift icons (🎁) next to merchant website icons
2. **View Details**: Click the gift icon to see campaign information
3. **Understand Limits**: Review transaction, customer, and merchant limits
4. **Reserve**: For one-time claims, use the reservation system
5. **Claim**: Visit the merchant and pay with BCH through Paytaca

### Map Navigation
- **Zoom**: Use mouse wheel or pinch gestures to zoom in/out
- **Pan**: Click and drag to move around the map
- **Merchant Details**: Click on map markers to see merchant information
- **Location**: Click merchant cards to zoom to their location

## 🔧 Configuration

### Environment Variables
```bash
# Django settings
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:pass@localhost:5432/paytaca_map

# API endpoints
ENGAGEMENT_HUB_API=https://engagementhub.paytaca.com
WATCHTOWER_API=https://watchtower.cash
```

### Map Configuration
```javascript
// Default map center (Tacloban City)
const defaultCenter = [11.2441900, 124.9987370];

// Zoom levels
const zoomLevels = {
  default: 3.5,
  merchant: 17.5,
  nearby: 10
};
```

## 🧪 Development

### Project Structure
```
paytaca-map/
├── frontend/                 # Vue.js frontend application
│   ├── src/
│   │   ├── components/      # Vue components
│   │   ├── stores/          # Pinia stores
│   │   └── assets/          # Static assets
│   ├── package.json
│   └── vite.config.js
├── main/                     # Django backend application
│   ├── models.py            # Database models
│   ├── views.py             # API views
│   ├── urls.py              # URL routing
│   └── migrations/          # Database migrations
├── paytacamap/              # Django project settings
├── requirements.txt          # Python dependencies
├── docker-compose.yml       # Docker configuration
└── README.md
```

### Available Scripts
```bash
# Frontend
npm run dev          # Start development server
npm run build        # Build for production
npm run preview      # Preview production build
npm run test         # Run tests

# Backend
python manage.py runserver    # Start Django server
python manage.py migrate      # Run migrations
python manage.py collectstatic # Collect static files
python manage.py createsuperuser # Create admin user
```

### API Endpoints
- `GET /api/merchants/` - List all merchants
- `GET /api/locations/` - Merchant location data
- `GET /api/logos/` - Merchant logo images
- `GET /api/categories/` - Merchant categories

## 🚀 Deployment

### Production Build
```bash
# Frontend
cd frontend
npm run build

# Backend
python manage.py collectstatic
python manage.py migrate
```

### Docker Production
```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Deploy
docker-compose -f docker-compose.prod.yml up -d
```

### Environment Setup
- Configure production database
- Set up SSL certificates
- Configure reverse proxy (Nginx)
- Set production environment variables

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow Vue.js style guide
- Use conventional commit messages
- Write tests for new features
- Update documentation as needed

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Paytaca Team**: For the vision and support
- **OpenStreetMap**: For map data and tiles
- **Leaflet.js**: For the mapping library
- **Vue.js Community**: For the excellent framework

## 📞 Support

For support and questions:
- Create an issue in this repository
- Contact the Paytaca development team
- Check the project documentation

---

**Built with ❤️ by the Paytaca Team**

