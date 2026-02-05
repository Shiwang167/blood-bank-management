# BloodBridge - Blood Bank Management System

A production-ready, cloud-based blood bank management system that connects blood donors, hospitals, and blood banks in real-time.

![Architecture](C:/Users/Shiwa/.gemini/antigravity/brain/dc85a287-c153-4740-8e84-bbae77323569/bloodbridge_architecture_1770054667190.png)

## 🌟 Live Demo

**Frontend:** [Your S3 URL]  
**Backend API:** http://43.204.234.177/api  
**Health Check:** http://43.204.234.177/health

### Demo Credentials
- **Donor:** demo.donor@bloodbridge.com / Demo123!
- **Hospital:** demo.hospital@bloodbridge.com / Demo123!
- **Manager:** demo.manager@bloodbridge.com / Demo123!

## 💻 Tech Stack

**Frontend:** React 18, Vite, CSS3  
**Backend:** Python Flask, Gunicorn, Nginx  
**Database:** PostgreSQL (AWS RDS)  
**Cloud:** AWS (EC2, RDS, S3, CloudFront)  
**Auth:** JWT, Bcrypt

## ✨ Features

- Role-based access control (Donor, Hospital, Manager)
- Real-time blood request matching
- Donation eligibility tracking (90-day interval)
- Inventory management with low-stock alerts
- Emergency request prioritization
- Secure JWT authentication

## 🏗️ Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed system design.

## 🚀 Quick Start

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python scripts/migrate_db.py
python app.py
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## 📚 Documentation

- [Architecture Design](ARCHITECTURE.md)
- [Deployment Guide - Amazon Linux](DEPLOYMENT_AMAZON_LINUX.md)
- [Frontend Deployment - S3/CloudFront](FRONTEND_S3_CLOUDFRONT.md)
- [Testing Guide](TESTING_GUIDE.md)
- [HTTPS Setup](SETUP_HTTPS_BACKEND.md)

## 🔐 Security

- Password hashing with bcrypt (12 rounds)
- JWT token authentication (24-hour expiry)
- CORS protection
- Environment-based secrets
- SQL injection prevention

## 📊 Database Schema

- **users** - User accounts with roles
- **blood_requests** - Blood request management
- **inventory** - Blood type inventory tracking
- **donations** - Donation history

## 🎯 API Endpoints

```
POST   /api/auth/register     - Register user
POST   /api/auth/login        - Login user
GET    /api/requests          - Get blood requests
POST   /api/requests          - Create request
GET    /api/inventory         - Get inventory
PUT    /api/inventory         - Update inventory
GET    /api/donor/eligibility - Check eligibility
```

## 👨‍💻 Author

**[Your Name]**  
LinkedIn: [Your LinkedIn]  
Email: [Your Email]

## 📝 License

Educational/Portfolio Project

---

**Built with ❤️ for saving lives through technology**
