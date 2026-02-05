# Quick Reference: RDS and EC2 Configuration

## ✅ Correct Configuration

### RDS PostgreSQL Settings

```
┌─────────────────────────────────────────────┐
│         RDS CONFIGURATION                   │
├─────────────────────────────────────────────┤
│ VPC:                  Default VPC           │
│ Subnet:               Private (or default)  │
│ Public Access:        NO ✅                 │
│ Security Group:       bloodbank-db-sg       │
│ Port:                 5432                  │
├─────────────────────────────────────────────┤
│ Security Group Inbound Rules:               │
│   Type: PostgreSQL                          │
│   Port: 5432                                │
│   Source: bloodbank-backend-sg ✅           │
└─────────────────────────────────────────────┘
```

### EC2 Instance Settings

```
┌─────────────────────────────────────────────┐
│         EC2 CONFIGURATION                   │
├─────────────────────────────────────────────┤
│ VPC:                  Default VPC (SAME!)   │
│ Subnet:               Public                │
│ Auto-assign Public IP: YES ✅               │
│ Security Group:       bloodbank-backend-sg  │
├─────────────────────────────────────────────┤
│ Security Group Inbound Rules:               │
│   SSH:    Port 22   from Your IP           │
│   HTTP:   Port 80   from 0.0.0.0/0         │
│   HTTPS:  Port 443  from 0.0.0.0/0         │
└─────────────────────────────────────────────┘
```

---

## Key Points

✅ **SAME VPC** - Both EC2 and RDS must be in the same VPC  
✅ **EC2 in PUBLIC subnet** - Needs internet access for users  
✅ **RDS in PRIVATE subnet** - Security best practice  
✅ **RDS Public Access = NO** - Never expose database to internet  
✅ **RDS allows ONLY EC2** - Security group references EC2's SG  

---

## Why This Matters

| Configuration | Result |
|--------------|--------|
| Same VPC | ✅ Low latency, no extra costs |
| Different VPCs | ❌ Complex setup, higher costs |
| RDS in Private | ✅ Secure, best practice |
| RDS in Public | ❌ Security risk |
| RDS Public Access = No | ✅ Protected from internet |
| RDS Public Access = Yes | ❌ Vulnerable to attacks |

---

## During AWS Setup

### When Creating RDS:

1. **Connectivity section:**
   - VPC: Choose "Default VPC" ✅
   - Subnet group: Default
   - **Public access: NO** ✅ ← IMPORTANT!
   - VPC security group: Create new → `bloodbank-db-sg`

2. **After creation:**
   - Go to Security Groups
   - Edit `bloodbank-db-sg` inbound rules
   - Add: PostgreSQL (5432) from `bloodbank-backend-sg`

### When Creating EC2:

1. **Network settings:**
   - VPC: "Default VPC" (same as RDS) ✅
   - Subnet: Any public subnet
   - **Auto-assign public IP: Enable** ✅ ← IMPORTANT!
   - Security group: Create new → `bloodbank-backend-sg`
   - Add rules: SSH (22), HTTP (80), HTTPS (443)

---

## Verification Commands

### Test from EC2 (Should Work ✅)

```bash
# SSH into EC2
ssh -i key.pem ubuntu@your-ec2-public-ip

# Test database connection
psql -h your-rds-endpoint.rds.amazonaws.com -U dbadmin -d bloodbank
# Should connect successfully!
```

### Test from Internet (Should Fail ✅)

```bash
# From your local computer
psql -h your-rds-endpoint.rds.amazonaws.com -U dbadmin -d bloodbank
# Should timeout (this is good - means DB is protected!)
```

---

## Common Mistakes

❌ **Mistake 1:** Different VPCs
```
EC2: VPC-A
RDS: VPC-B
Result: Can't connect
```

❌ **Mistake 2:** RDS Public Access = Yes
```
RDS: Public access enabled
Result: Security vulnerability
```

❌ **Mistake 3:** Wrong security group
```
RDS allows: 0.0.0.0/0
Result: Anyone can try to connect
```

✅ **Correct:**
```
EC2: Default VPC, Public subnet, Public IP
RDS: Default VPC, Private subnet, No public access
RDS Security: Only allows EC2 security group
```

---

## Quick Decision Tree

```
Question: Should I use the same VPC?
Answer: YES ✅

Question: Should EC2 be in public subnet?
Answer: YES ✅ (needs internet access)

Question: Should RDS be in private subnet?
Answer: YES ✅ (security best practice)

Question: Should RDS have public access?
Answer: NO ✅ (never expose database)

Question: What should RDS security group allow?
Answer: Only EC2 security group on port 5432 ✅
```

---

## Summary

**Your understanding is 100% correct!** ✅

- ✅ Same VPC for both
- ✅ EC2 in public subnet
- ✅ RDS in private subnet
- ✅ RDS not publicly accessible

This is the **standard architecture** for web applications on AWS.
