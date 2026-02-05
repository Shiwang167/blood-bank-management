# AWS VPC and Subnet Architecture Guide

## Recommended Architecture for Blood Bank Application

### ✅ Best Practice Configuration

**YES - This is the recommended setup:**

```
┌─────────────────────────────────────────────────────────┐
│                      AWS VPC                            │
│                  (Same VPC for both)                    │
│                                                         │
│  ┌──────────────────────┐  ┌──────────────────────┐   │
│  │   Public Subnet      │  │   Private Subnet     │   │
│  │                      │  │                      │   │
│  │  ┌──────────────┐   │  │  ┌──────────────┐   │   │
│  │  │  EC2 Instance│   │  │  │  RDS Database│   │   │
│  │  │  (Backend)   │◄──┼──┼──┤  (PostgreSQL)│   │   │
│  │  └──────────────┘   │  │  └──────────────┘   │   │
│  │         ▲            │  │                      │   │
│  └─────────┼────────────┘  └──────────────────────┘   │
│            │                                            │
└────────────┼────────────────────────────────────────────┘
             │
        ┌────▼────┐
        │ Internet│
        │ Gateway │
        └─────────┘
             ▲
             │
        Users/Clients
```

### Configuration Details

#### 1. **VPC Configuration**
- **Use the SAME VPC** for both EC2 and RDS
- VPC CIDR: `10.0.0.0/16` (or use default VPC)
- Region: Same region for both (e.g., `us-east-1`)

#### 2. **EC2 Instance - Public Subnet**
- **Subnet**: Public subnet
- **Public IP**: Yes (Auto-assign)
- **Internet Access**: Via Internet Gateway
- **Ports Open**: 22 (SSH), 80 (HTTP), 443 (HTTPS)
- **Why Public?**: Needs to receive HTTP/HTTPS requests from users

#### 3. **RDS Database - Private Subnet**
- **Subnet**: Private subnet (or DB subnet group)
- **Public IP**: No
- **Internet Access**: Not needed
- **Ports Open**: Only 5432 from EC2 security group
- **Why Private?**: Security - database should not be accessible from internet

---

## Security Group Configuration

### EC2 Security Group (`bloodbank-backend-sg`)

**Inbound Rules:**
```
Type        Protocol    Port    Source              Description
SSH         TCP         22      Your IP             SSH access
HTTP        TCP         80      0.0.0.0/0          Public web access
HTTPS       TCP         443     0.0.0.0/0          Public web access (SSL)
```

**Outbound Rules:**
```
Type        Protocol    Port    Destination         Description
All         All         All     0.0.0.0/0          Allow all outbound
```

### RDS Security Group (`bloodbank-db-sg`)

**Inbound Rules:**
```
Type        Protocol    Port    Source                      Description
PostgreSQL  TCP         5432    bloodbank-backend-sg        From EC2 only
```

**Outbound Rules:**
```
Type        Protocol    Port    Destination         Description
All         All         All     0.0.0.0/0          Allow all outbound
```

---

## Step-by-Step Setup

### Option 1: Using Default VPC (Simplest)

#### Step 1: Create RDS in Default VPC

1. Go to **RDS → Create database**
2. **Connectivity:**
   - VPC: **Default VPC**
   - Subnet group: **Default**
   - Public access: **No** ✅ (Keep private)
   - VPC security group: Create new → `bloodbank-db-sg`
   - Availability Zone: No preference

#### Step 2: Create EC2 in Same VPC

1. Go to **EC2 → Launch Instance**
2. **Network settings:**
   - VPC: **Default VPC** (same as RDS)
   - Subnet: **Any public subnet**
   - Auto-assign public IP: **Enable** ✅
   - Security group: Create new → `bloodbank-backend-sg`

#### Step 3: Configure Security Groups

1. **RDS Security Group** (`bloodbank-db-sg`):
   - Edit Inbound rules
   - Add rule:
     - Type: PostgreSQL
     - Port: 5432
     - Source: Custom → Select `bloodbank-backend-sg`
     - Description: "Allow from EC2"

2. **EC2 Security Group** (`bloodbank-backend-sg`):
   - Should already have SSH, HTTP, HTTPS

---

### Option 2: Custom VPC with Public/Private Subnets (Production)

#### Step 1: Create VPC

```bash
VPC CIDR: 10.0.0.0/16

Subnets:
├── Public Subnet 1:  10.0.1.0/24 (us-east-1a)
├── Public Subnet 2:  10.0.2.0/24 (us-east-1b)
├── Private Subnet 1: 10.0.11.0/24 (us-east-1a)
└── Private Subnet 2: 10.0.12.0/24 (us-east-1b)

Internet Gateway: Attached to VPC
Route Tables:
├── Public RT: 0.0.0.0/0 → Internet Gateway
└── Private RT: No internet route
```

#### Step 2: Create DB Subnet Group

1. Go to **RDS → Subnet groups → Create**
2. Name: `bloodbank-db-subnet-group`
3. VPC: Your custom VPC
4. Add subnets:
   - Private Subnet 1 (us-east-1a)
   - Private Subnet 2 (us-east-1b)

#### Step 3: Create RDS

1. **Connectivity:**
   - VPC: Your custom VPC
   - DB subnet group: `bloodbank-db-subnet-group`
   - Public access: **No**
   - VPC security group: `bloodbank-db-sg`

#### Step 4: Create EC2

1. **Network settings:**
   - VPC: Your custom VPC
   - Subnet: **Public Subnet 1** (or 2)
   - Auto-assign public IP: **Enable**
   - Security group: `bloodbank-backend-sg`

---

## Why This Architecture?

### ✅ Security Benefits

1. **Database Isolation**
   - RDS in private subnet = no direct internet access
   - Only EC2 can connect to database
   - Reduces attack surface

2. **Defense in Depth**
   - Multiple layers of security
   - Security groups act as firewalls
   - Network isolation

3. **Compliance**
   - Follows AWS Well-Architected Framework
   - Industry best practice
   - Meets security standards

### ✅ Operational Benefits

1. **Same VPC = Low Latency**
   - EC2 ↔ RDS communication stays within VPC
   - No internet routing
   - Faster database queries

2. **No Data Transfer Costs**
   - Traffic within same VPC/AZ is free
   - Saves money on data transfer

3. **Easy Security Group Rules**
   - Reference security groups by ID
   - No need for IP addresses

---

## Common Mistakes to Avoid

### ❌ DON'T: Put RDS in Public Subnet

```
Bad Configuration:
├── RDS: Public subnet, Public access = Yes
└── Problem: Database exposed to internet
```

**Why it's bad:**
- Security risk - anyone can attempt to connect
- Vulnerable to brute force attacks
- Violates security best practices

### ❌ DON'T: Use Different VPCs

```
Bad Configuration:
├── EC2: VPC A
└── RDS: VPC B
```

**Why it's bad:**
- Requires VPC peering (complex)
- Higher latency
- Additional costs
- More configuration

### ❌ DON'T: Allow 0.0.0.0/0 to RDS

```
Bad Security Group:
RDS Inbound: 0.0.0.0/0 on port 5432
```

**Why it's bad:**
- Allows entire internet to attempt connections
- Major security vulnerability
- Easy target for attacks

---

## Verification Checklist

After setup, verify:

- [ ] EC2 and RDS in **same VPC** ✅
- [ ] EC2 in **public subnet** with public IP ✅
- [ ] RDS in **private subnet** (or DB subnet group) ✅
- [ ] RDS **public access = No** ✅
- [ ] RDS security group allows **only EC2 security group** ✅
- [ ] EC2 can connect to RDS:
  ```bash
  psql -h your-rds-endpoint.rds.amazonaws.com -U dbuser -d bloodbank
  ```
- [ ] RDS **not** accessible from internet ✅

---

## Testing Connectivity

### From EC2 to RDS (Should Work ✅)

```bash
# SSH into EC2
ssh -i key.pem ubuntu@ec2-public-ip

# Test database connection
psql -h bloodbank-db.xxxxx.us-east-1.rds.amazonaws.com -U dbadmin -d bloodbank

# Should connect successfully
```

### From Internet to RDS (Should Fail ✅)

```bash
# From your local machine
psql -h bloodbank-db.xxxxx.us-east-1.rds.amazonaws.com -U dbadmin -d bloodbank

# Should timeout or refuse connection (this is good!)
```

---

## Quick Setup Summary

**For Beginners (Use Default VPC):**

1. ✅ Create RDS in **Default VPC**, **Private subnet**, **Public access = No**
2. ✅ Create EC2 in **Default VPC**, **Public subnet**, **Public IP = Yes**
3. ✅ Configure RDS security group to allow EC2 security group on port 5432
4. ✅ Test connection from EC2 to RDS

**For Production (Custom VPC):**

1. ✅ Create VPC with public and private subnets
2. ✅ Create DB subnet group with private subnets
3. ✅ Create RDS in private subnets
4. ✅ Create EC2 in public subnet
5. ✅ Configure security groups properly
6. ✅ Test connectivity

---

## Cost Considerations

**Same VPC vs Different VPCs:**

- **Same VPC**: No additional costs ✅
- **Different VPCs**: VPC peering costs + data transfer costs ❌

**Public vs Private Subnet for RDS:**

- **Private subnet**: Best practice, no additional cost ✅
- **Public subnet**: Security risk, same cost ❌

---

## Summary

**Your Question:** Should DB be in private subnet and EC2 in public subnet?

**Answer:** **YES! Absolutely correct!** ✅

**Configuration:**
- ✅ Same VPC for both
- ✅ EC2 in public subnet (needs internet access)
- ✅ RDS in private subnet (security)
- ✅ RDS security group allows only EC2

This is the **industry standard** and **AWS best practice** for web applications with databases.

---

## Need Help?

If you're setting this up and run into issues:

1. **Can't connect from EC2 to RDS:**
   - Check security groups
   - Verify both in same VPC
   - Check RDS endpoint is correct

2. **RDS accessible from internet:**
   - Check "Public access" is set to "No"
   - Verify RDS is in private subnet
   - Check security group rules

3. **High latency:**
   - Ensure both in same availability zone (optional)
   - Verify both in same VPC
