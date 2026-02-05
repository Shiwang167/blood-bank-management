# BloodBridge - Complete Testing Guide

## 🧪 Manual Testing Procedures

This guide provides step-by-step instructions to test all features of your deployed BloodBridge application.

---

## 📋 Pre-Testing Checklist

Before starting tests, verify:
- [ ] Backend is running: `http://43.204.234.177/health` returns healthy
- [ ] Frontend is accessible via CloudFront URL
- [ ] Browser console is open (F12) to monitor errors
- [ ] Network tab is open to monitor API calls

---

## 1️⃣ Backend API Testing

### Test 1.1: Health Check

**Endpoint**: `GET http://43.204.234.177/health`

**Using Browser:**
1. Open: `http://43.204.234.177/health`

**Expected Response:**
```json
{
  "status": "healthy",
  "service": "BloodBridge API",
  "database": "connected"
}
```

**Using cURL:**
```bash
curl http://43.204.234.177/health
```

✅ **Pass Criteria**: Status is "healthy" and database is "connected"

---

### Test 1.2: API Root Endpoint

**Endpoint**: `GET http://43.204.234.177/`

**Expected Response:**
```json
{
  "message": "BloodBridge API",
  "version": "1.0.0",
  "endpoints": {
    "auth": "/api/auth",
    "requests": "/api/requests",
    "inventory": "/api/inventory",
    "donor": "/api/donor"
  }
}
```

---

## 2️⃣ Authentication Testing

### Test 2.1: User Registration - Donor

**Endpoint**: `POST http://43.204.234.177/api/auth/register`

**Using Browser Console:**
```javascript
fetch('http://43.204.234.177/api/auth/register', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    name: "Test Donor",
    email: "donor1@test.com",
    password: "Test123!",
    role: "donor",
    blood_type: "A+"
  })
})
.then(r => r.json())
.then(console.log);
```

**Expected Response:**
```json
{
  "message": "User registered successfully",
  "user": {
    "user_id": "...",
    "name": "Test Donor",
    "email": "donor1@test.com",
    "role": "donor",
    "blood_type": "A+"
  },
  "token": "eyJ..."
}
```

✅ **Pass Criteria**: 
- Status 201
- Returns JWT token
- User object contains correct data

---

### Test 2.2: User Registration - Hospital

**Body:**
```json
{
  "name": "City Hospital",
  "email": "hospital1@test.com",
  "password": "Test123!",
  "role": "hospital",
  "blood_type": "O+"
}
```

---

### Test 2.3: User Registration - Manager

**Body:**
```json
{
  "name": "Blood Bank Manager",
  "email": "manager1@test.com",
  "password": "Test123!",
  "role": "manager",
  "blood_type": "B+"
}
```

---

### Test 2.4: User Login

**Endpoint**: `POST http://43.204.234.177/api/auth/login`

**Using Browser Console:**
```javascript
fetch('http://43.204.234.177/api/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: "donor1@test.com",
    password: "Test123!"
  })
})
.then(r => r.json())
.then(data => {
  console.log(data);
  localStorage.setItem('token', data.token); // Save for next tests
});
```

**Expected Response:**
```json
{
  "message": "Login successful",
  "token": "eyJ...",
  "user": {
    "user_id": "...",
    "name": "Test Donor",
    "email": "donor1@test.com",
    "role": "donor",
    "blood_type": "A+"
  }
}
```

✅ **Pass Criteria**: Returns valid JWT token

---

### Test 2.5: Invalid Login

**Body:**
```json
{
  "email": "donor1@test.com",
  "password": "WrongPassword"
}
```

**Expected**: Status 401, error message

---

## 3️⃣ Blood Requests Testing

### Test 3.1: Create Blood Request (Hospital)

**Endpoint**: `POST http://43.204.234.177/api/requests`

**Prerequisites**: Login as hospital user first

**Using Browser Console:**
```javascript
const token = localStorage.getItem('token'); // From hospital login

fetch('http://43.204.234.177/api/requests', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  },
  body: JSON.stringify({
    blood_type: "O-",
    quantity: 2,
    urgency: "high",
    hospital_name: "City Hospital",
    patient_name: "John Doe",
    contact_number: "9876543210",
    required_by: "2026-02-10"
  })
})
.then(r => r.json())
.then(console.log);
```

**Expected Response:**
```json
{
  "message": "Blood request created successfully",
  "request": {
    "request_id": "...",
    "blood_type": "O-",
    "quantity": 2,
    "urgency": "high",
    "status": "open",
    ...
  }
}
```

✅ **Pass Criteria**: Status 201, request created

---

### Test 3.2: Get All Blood Requests

**Endpoint**: `GET http://43.204.234.177/api/requests`

**Using Browser Console:**
```javascript
const token = localStorage.getItem('token');

fetch('http://43.204.234.177/api/requests', {
  headers: { 'Authorization': `Bearer ${token}` }
})
.then(r => r.json())
.then(console.log);
```

**Expected**: Array of blood requests

---

### Test 3.3: Update Blood Request Status

**Endpoint**: `PUT http://43.204.234.177/api/requests/{request_id}`

**Body:**
```json
{
  "status": "fulfilled"
}
```

---

## 4️⃣ Inventory Testing

### Test 4.1: Get Inventory

**Endpoint**: `GET http://43.204.234.177/api/inventory`

**Using Browser Console:**
```javascript
const token = localStorage.getItem('token');

fetch('http://43.204.234.177/api/inventory', {
  headers: { 'Authorization': `Bearer ${token}` }
})
.then(r => r.json())
.then(console.log);
```

**Expected**: Array of blood inventory by type

---

### Test 4.2: Update Inventory (Manager Only)

**Endpoint**: `PUT http://43.204.234.177/api/inventory`

**Prerequisites**: Login as manager

**Body:**
```json
{
  "blood_type": "A+",
  "units_available": 15
}
```

**Expected**: Inventory updated successfully

---

### Test 4.3: Get Low Stock Alerts (Manager Only)

**Endpoint**: `GET http://43.204.234.177/api/inventory/low-stock`

**Expected**: Array of blood types with low stock (< 5 units)

---

## 5️⃣ Donor Features Testing

### Test 5.1: Check Eligibility

**Endpoint**: `GET http://43.204.234.177/api/donor/eligibility`

**Prerequisites**: Login as donor

**Expected Response:**
```json
{
  "eligible": true,
  "days_since_last_donation": 95,
  "next_eligible_date": null,
  "message": "You are eligible to donate blood"
}
```

---

### Test 5.2: Get Matching Requests

**Endpoint**: `GET http://43.204.234.177/api/donor/matching-requests`

**Expected**: Array of blood requests matching donor's blood type

---

### Test 5.3: Schedule Donation

**Endpoint**: `POST http://43.204.234.177/api/donor/schedule`

**Body:**
```json
{
  "request_id": "...",
  "scheduled_date": "2026-02-05"
}
```

---

## 6️⃣ Frontend Testing

### Test 6.1: Landing Page

1. Open CloudFront URL
2. Verify:
   - [ ] Dark theme loads
   - [ ] Hero section visible
   - [ ] "Save Lives, Donate Blood" heading
   - [ ] Login/Register buttons work
   - [ ] 3-step flow section
   - [ ] No console errors

---

### Test 6.2: Registration Flow

1. Click "Get Started" or "Register"
2. Fill registration form:
   - Name: Test User
   - Email: test@example.com
   - Password: Test123!
   - Role: Donor
   - Blood Type: A+
3. Click Register
4. Verify:
   - [ ] Success message appears
   - [ ] Redirected to dashboard
   - [ ] User info displayed in navbar
   - [ ] No CORS errors in console

---

### Test 6.3: Login Flow

1. Click "Login"
2. Enter credentials
3. Click Login
4. Verify:
   - [ ] Redirected to role-based dashboard
   - [ ] Token stored in localStorage
   - [ ] User name displayed
   - [ ] Logout button visible

---

### Test 6.4: Donor Dashboard

Login as donor user, verify:
- [ ] Dashboard loads
- [ ] "Matching Blood Requests" section visible
- [ ] Eligibility status shown
- [ ] Can view request details
- [ ] Can schedule donation

---

### Test 6.5: Hospital Dashboard

Login as hospital user, verify:
- [ ] Dashboard loads
- [ ] "Create New Request" button visible
- [ ] Can create blood request
- [ ] Active requests displayed
- [ ] Can update request status

**Create Request Test:**
1. Click "Create New Request"
2. Fill form:
   - Blood Type: O-
   - Quantity: 2
   - Urgency: High
   - Hospital: City Hospital
   - Patient: John Doe
   - Contact: 9876543210
3. Submit
4. Verify request appears in list

---

### Test 6.6: Manager Dashboard

Login as manager user, verify:
- [ ] Dashboard loads
- [ ] All blood requests visible
- [ ] Inventory management accessible
- [ ] Low stock alerts shown
- [ ] Can update inventory

**Update Inventory Test:**
1. Navigate to Inventory page
2. Select blood type: A+
3. Set units: 20
4. Click Update
5. Verify inventory updated

---

### Test 6.7: Navigation & Routing

Test all navigation links:
- [ ] Dashboard link works
- [ ] Requests page accessible
- [ ] Inventory page accessible (manager)
- [ ] Profile/Settings (if implemented)
- [ ] Logout works and redirects to landing

Test direct URL access:
- [ ] `/dashboard` - redirects if not logged in
- [ ] `/requests` - accessible when logged in
- [ ] `/inventory` - accessible for managers

---

## 7️⃣ Security Testing

### Test 7.1: Protected Routes

1. Logout
2. Try accessing: `YOUR_CLOUDFRONT_URL/dashboard`
3. Verify: Redirected to login page

---

### Test 7.2: Role-Based Access

1. Login as donor
2. Try accessing manager-only features
3. Verify: Access denied or hidden

---

### Test 7.3: Token Expiration

1. Login and get token
2. Wait 24 hours (or modify token)
3. Try API call with expired token
4. Verify: 401 Unauthorized

---

### Test 7.4: CORS Verification

1. Open CloudFront URL
2. Open browser console
3. Perform any API action
4. Check Network tab
5. Verify:
   - [ ] No CORS errors
   - [ ] Proper Access-Control headers
   - [ ] Requests succeed

---

## 8️⃣ Error Handling Testing

### Test 8.1: Invalid Input

Try registering with:
- Empty fields
- Invalid email format
- Weak password
- Duplicate email

Verify: Proper error messages displayed

---

### Test 8.2: Network Errors

1. Disconnect internet
2. Try any action
3. Verify: User-friendly error message

---

### Test 8.3: Backend Offline

1. Stop backend service
2. Try API call from frontend
3. Verify: Graceful error handling

---

## 9️⃣ Performance Testing

### Test 9.1: Page Load Time

1. Open CloudFront URL
2. Check Network tab
3. Verify:
   - [ ] Initial load < 3 seconds
   - [ ] Assets cached by CloudFront
   - [ ] Gzip compression enabled

---

### Test 9.2: API Response Time

1. Make API calls
2. Check Network tab timing
3. Verify:
   - [ ] Health check < 100ms
   - [ ] Login < 500ms
   - [ ] Get requests < 500ms

---

## 🔟 Cross-Browser Testing

Test on multiple browsers:
- [ ] Chrome
- [ ] Firefox
- [ ] Safari
- [ ] Edge

Verify all features work consistently.

---

## 📱 Responsive Design Testing

Test on different screen sizes:
- [ ] Desktop (1920x1080)
- [ ] Laptop (1366x768)
- [ ] Tablet (768x1024)
- [ ] Mobile (375x667)

Verify:
- [ ] Layout adapts properly
- [ ] All buttons clickable
- [ ] Forms usable
- [ ] No horizontal scroll

---

## ✅ Final Verification Checklist

### Backend
- [ ] Health endpoint returns healthy
- [ ] All API endpoints respond correctly
- [ ] Database queries execute successfully
- [ ] Authentication works
- [ ] Authorization enforced
- [ ] CORS configured properly

### Frontend
- [ ] Landing page loads
- [ ] Registration works
- [ ] Login works
- [ ] All dashboards accessible
- [ ] Navigation works
- [ ] No console errors
- [ ] No CORS errors

### Integration
- [ ] Frontend connects to backend
- [ ] API calls succeed
- [ ] Data persists in database
- [ ] Real-time updates work
- [ ] Error handling works

### Security
- [ ] HTTPS on frontend (CloudFront)
- [ ] JWT authentication working
- [ ] Protected routes enforced
- [ ] Role-based access working
- [ ] Passwords hashed

### Performance
- [ ] Page load < 3s
- [ ] API response < 500ms
- [ ] CloudFront caching works
- [ ] No memory leaks

---

## 📊 Test Results Template

Use this template to document your test results:

```
Test Date: ___________
Tester: ___________

Backend Tests:
- Health Check: ✅ / ❌
- API Root: ✅ / ❌
- Registration: ✅ / ❌
- Login: ✅ / ❌

Frontend Tests:
- Landing Page: ✅ / ❌
- Registration Flow: ✅ / ❌
- Login Flow: ✅ / ❌
- Donor Dashboard: ✅ / ❌
- Hospital Dashboard: ✅ / ❌
- Manager Dashboard: ✅ / ❌

Integration Tests:
- API Calls: ✅ / ❌
- CORS: ✅ / ❌
- Data Persistence: ✅ / ❌

Issues Found:
1. ___________
2. ___________

Overall Status: PASS / FAIL
```

---

## 🐛 Bug Reporting Template

If you find issues:

```
Bug ID: ___________
Severity: Critical / High / Medium / Low
Component: Backend / Frontend / Database

Description:
___________

Steps to Reproduce:
1. ___________
2. ___________
3. ___________

Expected Result:
___________

Actual Result:
___________

Screenshots:
[Attach if applicable]

Browser/Environment:
___________
```

---

## 🎯 Success Criteria

Your application passes testing if:

✅ All backend API endpoints return expected responses  
✅ All frontend pages load without errors  
✅ User registration and login work  
✅ All three role dashboards function correctly  
✅ Blood requests can be created and managed  
✅ Inventory can be updated  
✅ No CORS errors  
✅ No console errors  
✅ Protected routes are enforced  
✅ Role-based access works  

---

**Happy Testing! 🧪**
