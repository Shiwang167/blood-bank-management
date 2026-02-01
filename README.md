# BloodBridge - AWS Blood Donation Management System

A production-ready web application that connects blood donors, hospitals, and blood banks in real-time using AWS services.

## 🏗️ Architecture

- **Frontend**: React + Vite (hosted on AWS S3)
- **Backend**: Python Flask REST API (AWS EC2/Elastic Beanstalk)
- **Database**: Amazon DynamoDB (NoSQL)
- **Authentication**: JWT-based with role-based access control
- **AWS SDK**: boto3

## 👥 User Roles

1. **Donor**: View requests, check eligibility, schedule donations
2. **Hospital/Admin**: Create blood requests with emergency priority
3. **Blood Bank Manager**: Update inventory, view low-stock alerts

## 🚀 Quick Start

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env with your configuration

# Create DynamoDB tables (requires AWS credentials or DynamoDB Local)
python scripts/create_tables.py

# Run the server
python app.py
```

The backend will run on `http://localhost:5000`

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Setup environment variables
cp .env.example .env

# Run development server
npm run dev
```

The frontend will run on `http://localhost:5173`

## 📁 Project Structure

```
BloodBridge/
├── backend/
│   ├── app.py                 # Main Flask application
│   ├── config.py              # Configuration
│   ├── requirements.txt       # Python dependencies
│   ├── routes/                # API endpoints
│   │   ├── auth.py
│   │   ├── requests.py
│   │   ├── inventory.py
│   │   └── donor.py
│   ├── services/              # Business logic
│   │   ├── dynamodb_service.py
│   │   └── auth_service.py
│   ├── middleware/            # JWT & RBAC
│   │   └── auth_middleware.py
│   └── scripts/
│       └── create_tables.py   # DynamoDB setup
│
└── frontend/
    ├── src/
    │   ├── pages/             # React pages
    │   │   ├── Landing.jsx    # Dark landing page
    │   │   ├── Dashboard.jsx
    │   │   ├── DonorDashboard.jsx
    │   │   ├── HospitalDashboard.jsx
    │   │   ├── ManagerDashboard.jsx
    │   │   ├── Requests.jsx
    │   │   └── Inventory.jsx
    │   ├── components/        # Reusable components
    │   │   ├── Navbar.jsx
    │   │   └── ProtectedRoute.jsx
    │   ├── context/           # State management
    │   │   └── AuthContext.jsx
    │   ├── api/               # API client
    │   │   └── axios.js
    │   └── styles/            # CSS
    │       └── index.css
    └── package.json

```

## 🔑 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user

### Blood Requests
- `GET /api/requests` - Get all requests
- `POST /api/requests` - Create request (Hospital/Manager)
- `PUT /api/requests/:id` - Update request (Hospital/Manager)

### Inventory
- `GET /api/inventory` - Get blood inventory
- `PUT /api/inventory` - Update inventory (Manager only)
- `GET /api/inventory/low-stock` - Get low stock alerts (Manager)

### Donor
- `GET /api/donor/eligibility` - Check donation eligibility
- `GET /api/donor/matching-requests` - Get matching blood requests
- `POST /api/donor/schedule` - Schedule donation

## 🎨 UI Features

### Landing Page (Dark Theme)
- Cinematic gradient hero section
- 3-step flow visualization
- Impact statistics
- Glass-morphism authentication modal

### Dashboard (Light Theme)
- Role-based widgets
- Blood inventory visualization
- Emergency request indicators
- Real-time stock alerts

## 🔒 Security

- JWT authentication with 24-hour expiration
- Password hashing with bcrypt (12 rounds)
- Role-based access control (RBAC)
- Environment-based configuration
- CORS protection
- No hardcoded credentials

## ☁️ AWS Deployment

### DynamoDB Tables
- `BloodBridge_Users` - User accounts
- `BloodBridge_BloodRequests` - Blood requests
- `BloodBridge_Inventory` - Blood inventory

### Backend Deployment (EC2)
```bash
# Install dependencies
sudo yum update -y
sudo yum install python3 python3-pip nginx -y

# Clone and setup
git clone <repository>
cd backend
pip3 install -r requirements.txt

# Configure Gunicorn + Nginx
# See deployment documentation
```

### Frontend Deployment (S3)
```bash
# Build
npm run build

# Upload to S3
aws s3 sync dist/ s3://bloodbridge-frontend --delete
```

## 📊 DynamoDB Schema

### Users Table
```json
{
  "user_id": "uuid",
  "name": "John Doe",
  "email": "john@email.com",
  "role": "donor|hospital|manager",
  "blood_type": "A+",
  "last_donation": "ISO-8601"
}
```

### BloodRequests Table
```json
{
  "request_id": "uuid",
  "blood_type": "O-",
  "quantity": 2,
  "urgency": "high|normal",
  "status": "open|fulfilled|cancelled",
  "created_by": "user_id",
  "timestamp": "ISO-8601"
}
```

### Inventory Table
```json
{
  "blood_type": "B+",
  "units_available": 12,
  "last_updated": "ISO-8601"
}
```

## 🧪 Testing

### Backend
```bash
# Run with DynamoDB Local
docker run -p 8000:8000 amazon/dynamodb-local

# Test endpoints with curl or Postman
curl http://localhost:5000/health
```

### Frontend
```bash
npm run dev
# Test in browser at http://localhost:5173
```

## 📝 Environment Variables

### Backend (.env)
```
FLASK_ENV=development
SECRET_KEY=your-secret-key
JWT_SECRET=your-jwt-secret
AWS_REGION=us-east-1
DYNAMODB_ENDPOINT=http://localhost:8000  # For local dev
CORS_ORIGIN=http://localhost:5173
```

### Frontend (.env)
```
VITE_API_URL=http://localhost:5000/api
```

## 🤝 Contributing

This is an academic project. For production use:
1. Implement proper error handling
2. Add comprehensive logging
3. Set up monitoring (CloudWatch)
4. Implement rate limiting
5. Add automated tests
6. Setup CI/CD pipeline

## 📄 License

Academic project - All rights reserved

## 👨‍💻 Author

Built for academic evaluation as a cloud-based healthcare solution.
