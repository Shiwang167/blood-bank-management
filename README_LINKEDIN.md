# 🩸 BloodBridge - Cloud-Based Blood Bank Management System

A production-ready, full-stack web application that connects blood donors, hospitals, and blood banks in real-time using AWS cloud infrastructure.

![BloodBridge Banner](https://img.shields.io/badge/Status-Live-success?style=for-the-badge)
![AWS](https://img.shields.io/badge/AWS-Cloud-orange?style=for-the-badge&logo=amazon-aws)
![React](https://img.shields.io/badge/React-Frontend-blue?style=for-the-badge&logo=react)
![Flask](https://img.shields.io/badge/Flask-Backend-green?style=for-the-badge&logo=flask)

---

## 🌟 **Live Demo**

**Frontend:** `http://bloodbank-frontend.s3-website-ap-south-1.amazonaws.com`  
**Backend API:** `http://43.204.234.177/api`  
**Health Check:** `http://43.204.234.177/health`

### **Demo Credentials:**

| Role | Email | Password |
|------|-------|----------|
| **Donor** | demo.donor@bloodbridge.com | Demo123! |
| **Hospital** | demo.hospital@bloodbridge.com | Demo123! |
| **Manager** | demo.manager@bloodbridge.com | Demo123! |

---

## 🏗️ **Architecture**

```
┌─────────────────────────────────────────────────────────────┐
│                         Users                                │
└────────────────────┬────────────────────────────────────────┘
                     │
              ┌──────▼──────┐                          ┌──────────────┐
              │  S3 Bucket  │                          │     EC2      │
              │  Frontend   │─────────────────────────▶│   Backend    │
              │   (React)   │      API Calls           │   (Flask)    │
              └─────────────┘                          └──────┬───────┘
                                                              │
                                                       ┌──────▼───────┐
                                                       │     RDS      │
                                                       │ PostgreSQL   │
                                                       └──────────────┘
```

---

## 💻 **Tech Stack**

### **Frontend**
- ⚛️ React 18 + Vite
- 🎨 CSS3 (Custom styling)
- 🔐 JWT Authentication
- 📱 Responsive Design

### **Backend**
- 🐍 Python Flask
- 🔒 JWT + Bcrypt
- 🌐 RESTful API
- 🔧 Gunicorn WSGI Server
- 🚀 Nginx Reverse Proxy

### **Database**
- 🗄️ PostgreSQL (AWS RDS)
- 📊 Normalized Schema (3NF)
- 🔄 Migration Scripts

### **Cloud Infrastructure (AWS)**
- ☁️ EC2 (t2.micro) - Backend hosting
- 🗄️ RDS (PostgreSQL) - Database
- 📦 S3 - Static website hosting
- 🌍 CloudFront - CDN (optional)
- 🔐 Security Groups + VPC

### **DevOps**
- 🐧 Amazon Linux 2023
- ⚙️ Systemd Service Management
- 📝 Application Logging
- 🔄 Auto-restart on failure

---

## ✨ **Key Features**

### **Role-Based Access Control**
- 👤 **Donors**: View matching requests, check eligibility, schedule donations
- 🏥 **Hospitals**: Create urgent blood requests, track status
- 👨‍💼 **Managers**: Update inventory, view analytics, manage all requests

### **Core Functionality**
- ✅ User authentication with JWT
- ✅ Blood type matching algorithm
- ✅ Donation eligibility checking (90-day interval)
- ✅ Emergency request prioritization
- ✅ Real-time inventory management
- ✅ Low-stock alerts
- ✅ Donation history tracking

### **Security**
- 🔐 Password hashing (bcrypt, 12 rounds)
- 🎫 JWT token authentication (24-hour expiry)
- 🛡️ CORS protection
- 🔒 Environment-based secrets
- 🚫 SQL injection prevention (parameterized queries)

---

## 📊 **Database Schema**

### **Users Table**
```sql
- user_id (UUID, Primary Key)
- name, email, password_hash
- role (donor/hospital/manager)
- blood_type
- last_donation_date
- created_at, updated_at
```

### **Blood Requests Table**
```sql
- request_id (UUID, Primary Key)
- blood_type, quantity
- urgency (high/normal)
- status (open/fulfilled/cancelled)
- hospital_name, patient_name
- contact_number
- created_by (Foreign Key → users)
- created_at, required_by
```

### **Inventory Table**
```sql
- blood_type (Primary Key)
- units_available
- last_updated
```

### **Donations Table**
```sql
- donation_id (UUID, Primary Key)
- donor_id (Foreign Key → users)
- request_id (Foreign Key → blood_requests)
- donation_date, scheduled_date
- status, notes
```

---

## 🚀 **API Endpoints**

### **Authentication**
```
POST /api/auth/register  - Register new user
POST /api/auth/login     - Login user
```

### **Blood Requests**
```
GET    /api/requests           - Get all requests
POST   /api/requests           - Create request (Hospital/Manager)
PUT    /api/requests/:id       - Update request
DELETE /api/requests/:id       - Delete request
```

### **Inventory**
```
GET /api/inventory           - Get blood inventory
PUT /api/inventory           - Update inventory (Manager only)
GET /api/inventory/low-stock - Get low stock alerts
```

### **Donor**
```
GET  /api/donor/eligibility        - Check donation eligibility
GET  /api/donor/matching-requests  - Get matching blood requests
POST /api/donor/schedule           - Schedule donation
```

---

## 🎯 **What I Learned**

### **Technical Skills**
- Full-stack web development from scratch
- AWS cloud architecture and deployment
- RESTful API design principles
- Database schema design and normalization
- Production deployment best practices
- Linux server administration
- Nginx configuration and reverse proxy setup

### **Challenges Overcome**
- Configured CORS for cross-origin requests
- Implemented secure JWT authentication
- Designed scalable database schema
- Set up production-grade deployment pipeline
- Managed AWS security groups and VPC
- Configured systemd for auto-restart

---

## 📈 **Future Enhancements**

- [ ] HTTPS/SSL certificate setup
- [ ] Email notifications for urgent requests
- [ ] SMS alerts via AWS SNS
- [ ] Admin analytics dashboard
- [ ] Geolocation-based donor matching
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Automated testing suite
- [ ] Mobile app (React Native)
- [ ] Multi-language support
- [ ] Integration with hospital systems

---

## 🛠️ **Local Development**

### **Prerequisites**
- Node.js 18+
- Python 3.11+
- PostgreSQL 15+

### **Backend Setup**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your configuration
python scripts/migrate_db.py
python app.py
```

### **Frontend Setup**
```bash
cd frontend
npm install
npm run dev
```

---

## 📦 **Deployment**

Complete deployment guides available:
- [`DEPLOYMENT_AMAZON_LINUX.md`](DEPLOYMENT_AMAZON_LINUX.md) - Backend deployment
- [`FRONTEND_S3_CLOUDFRONT.md`](FRONTEND_S3_CLOUDFRONT.md) - Frontend deployment
- [`SETUP_HTTPS_BACKEND.md`](SETUP_HTTPS_BACKEND.md) - HTTPS configuration

---

## 🔐 **Environment Variables**

### **Backend (.env)**
```bash
FLASK_ENV=production
SECRET_KEY=your-secret-key
JWT_SECRET=your-jwt-secret
DATABASE_URL=postgresql://user:pass@host:5432/dbname
CORS_ORIGIN=http://your-frontend-url
```

### **Frontend (.env.production)**
```bash
VITE_API_URL=http://your-backend-url/api
```

---

## 📝 **License**

This project is for educational and portfolio purposes.

---

## 👨‍💻 **Author**

**[Your Name]**
- LinkedIn: [Your LinkedIn]
- GitHub: [Your GitHub]
- Email: [Your Email]

---

## 🙏 **Acknowledgments**

Built as a demonstration of full-stack development and AWS cloud deployment skills.

---

## 📸 **Screenshots**

### Landing Page
![Landing Page](screenshots/landing.png)

### Donor Dashboard
![Donor Dashboard](screenshots/donor-dashboard.png)

### Hospital Dashboard
![Hospital Dashboard](screenshots/hospital-dashboard.png)

### Manager Dashboard
![Manager Dashboard](screenshots/manager-dashboard.png)

---

**⭐ If you found this project interesting, please give it a star!**

---

## 📊 **Project Stats**

- **Lines of Code**: ~5,000+
- **Development Time**: [Your timeframe]
- **AWS Services Used**: 4 (EC2, RDS, S3, CloudFront)
- **API Endpoints**: 12+
- **Database Tables**: 4
- **User Roles**: 3

---

**Built with ❤️ for saving lives through technology**
