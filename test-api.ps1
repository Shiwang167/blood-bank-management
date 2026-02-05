# BloodBridge API Testing Script for PowerShell
# Usage: .\test-api.ps1

$baseUrl = "http://43.204.234.177"

Write-Host "=== BloodBridge API Testing ===" -ForegroundColor Cyan
Write-Host ""

# Test 1: Health Check
Write-Host "1. Testing Health Endpoint..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "$baseUrl/health" -Method GET -UseBasicParsing
    $result = $response.Content | ConvertFrom-Json
    Write-Host "✅ Health Check: $($result.status)" -ForegroundColor Green
    Write-Host "   Database: $($result.database)" -ForegroundColor Green
} catch {
    Write-Host "❌ Health Check Failed: $_" -ForegroundColor Red
}
Write-Host ""

# Test 2: API Root
Write-Host "2. Testing API Root..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "$baseUrl/" -Method GET -UseBasicParsing
    $result = $response.Content | ConvertFrom-Json
    Write-Host "✅ API Root: $($result.message)" -ForegroundColor Green
    Write-Host "   Version: $($result.version)" -ForegroundColor Green
} catch {
    Write-Host "❌ API Root Failed: $_" -ForegroundColor Red
}
Write-Host ""

# Test 3: Register Donor
Write-Host "3. Testing User Registration (Donor)..." -ForegroundColor Yellow
$randomEmail = "donor_$(Get-Random -Minimum 1000 -Maximum 9999)@test.com"
$registerBody = @{
    name = "Test Donor"
    email = $randomEmail
    password = "Test123!"
    role = "donor"
    blood_type = "A+"
} | ConvertTo-Json

try {
    $response = Invoke-WebRequest -Uri "$baseUrl/api/auth/register" `
        -Method POST `
        -ContentType "application/json" `
        -Body $registerBody `
        -UseBasicParsing
    $result = $response.Content | ConvertFrom-Json
    Write-Host "✅ Registration Successful" -ForegroundColor Green
    Write-Host "   User: $($result.user.name)" -ForegroundColor Green
    Write-Host "   Email: $($result.user.email)" -ForegroundColor Green
    Write-Host "   Role: $($result.user.role)" -ForegroundColor Green
    $global:token = $result.token
    $global:userEmail = $result.user.email
    Write-Host "   Token saved for next tests" -ForegroundColor Cyan
} catch {
    Write-Host "❌ Registration Failed" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
}
Write-Host ""

# Test 4: Login
Write-Host "4. Testing User Login..." -ForegroundColor Yellow
if ($global:userEmail) {
    $loginBody = @{
        email = $global:userEmail
        password = "Test123!"
    } | ConvertTo-Json

    try {
        $response = Invoke-WebRequest -Uri "$baseUrl/api/auth/login" `
            -Method POST `
            -ContentType "application/json" `
            -Body $loginBody `
            -UseBasicParsing
        $result = $response.Content | ConvertFrom-Json
        Write-Host "✅ Login Successful" -ForegroundColor Green
        Write-Host "   User: $($result.user.name)" -ForegroundColor Green
        $global:token = $result.token
    } catch {
        Write-Host "❌ Login Failed: $($_.Exception.Message)" -ForegroundColor Red
    }
} else {
    Write-Host "⚠️  Skipped (no user registered)" -ForegroundColor Yellow
}
Write-Host ""

# Test 5: Get Blood Requests
Write-Host "5. Testing Get Blood Requests..." -ForegroundColor Yellow
if ($global:token) {
    try {
        $headers = @{
            "Authorization" = "Bearer $global:token"
        }
        $response = Invoke-WebRequest -Uri "$baseUrl/api/requests" `
            -Method GET `
            -Headers $headers `
            -UseBasicParsing
        $result = $response.Content | ConvertFrom-Json
        Write-Host "✅ Retrieved Blood Requests" -ForegroundColor Green
        if ($result -is [array]) {
            Write-Host "   Total Requests: $($result.Count)" -ForegroundColor Green
        } else {
            Write-Host "   Response: $result" -ForegroundColor Green
        }
    } catch {
        Write-Host "❌ Get Requests Failed: $($_.Exception.Message)" -ForegroundColor Red
    }
} else {
    Write-Host "⚠️  Skipped (no token available)" -ForegroundColor Yellow
}
Write-Host ""

# Test 6: Get Inventory
Write-Host "6. Testing Get Inventory..." -ForegroundColor Yellow
if ($global:token) {
    try {
        $headers = @{
            "Authorization" = "Bearer $global:token"
        }
        $response = Invoke-WebRequest -Uri "$baseUrl/api/inventory" `
            -Method GET `
            -Headers $headers `
            -UseBasicParsing
        $result = $response.Content | ConvertFrom-Json
        Write-Host "✅ Retrieved Inventory" -ForegroundColor Green
        if ($result -is [array]) {
            Write-Host "   Blood Types Available: $($result.Count)" -ForegroundColor Green
        } else {
            Write-Host "   Response: $result" -ForegroundColor Green
        }
    } catch {
        Write-Host "❌ Get Inventory Failed: $($_.Exception.Message)" -ForegroundColor Red
    }
} else {
    Write-Host "⚠️  Skipped (no token available)" -ForegroundColor Yellow
}
Write-Host ""

# Summary
Write-Host "=== Testing Complete ===" -ForegroundColor Cyan
Write-Host ""
if ($global:token) {
    Write-Host "✅ Backend API is working correctly!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Your saved token (for manual testing):" -ForegroundColor Yellow
    Write-Host $global:token -ForegroundColor Gray
    Write-Host ""
    Write-Host "To test more endpoints manually, use:" -ForegroundColor Cyan
    Write-Host '$headers = @{"Authorization" = "Bearer YOUR_TOKEN"}' -ForegroundColor Gray
    Write-Host 'Invoke-WebRequest -Uri "http://43.204.234.177/api/requests" -Headers $headers -UseBasicParsing' -ForegroundColor Gray
} else {
    Write-Host "⚠️  Some tests failed. Check the errors above." -ForegroundColor Yellow
}
Write-Host ""
Write-Host "Next Step: Test your frontend by opening your CloudFront URL in a browser!" -ForegroundColor Cyan
