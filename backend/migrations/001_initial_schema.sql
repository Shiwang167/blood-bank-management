-- BloodBridge Database Schema for PostgreSQL
-- Migration: 001_initial_schema.sql

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table
CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('donor', 'hospital', 'manager')),
    blood_type VARCHAR(5),
    phone VARCHAR(20),
    last_donation TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Blood requests table
CREATE TABLE blood_requests (
    request_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    blood_type VARCHAR(5) NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    urgency VARCHAR(20) NOT NULL CHECK (urgency IN ('high', 'normal')),
    status VARCHAR(20) NOT NULL DEFAULT 'open' CHECK (status IN ('open', 'fulfilled', 'cancelled')),
    hospital_name VARCHAR(255),
    patient_name VARCHAR(255),
    contact_number VARCHAR(20),
    notes TEXT,
    created_by UUID REFERENCES users(user_id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fulfilled_at TIMESTAMP
);

-- Inventory table
CREATE TABLE inventory (
    blood_type VARCHAR(5) PRIMARY KEY,
    units_available INTEGER NOT NULL DEFAULT 0 CHECK (units_available >= 0),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by UUID REFERENCES users(user_id) ON DELETE SET NULL
);

-- Donation schedule table (for tracking donor appointments)
CREATE TABLE donation_schedule (
    schedule_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    donor_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    request_id UUID REFERENCES blood_requests(request_id) ON DELETE SET NULL,
    scheduled_date TIMESTAMP NOT NULL,
    status VARCHAR(20) DEFAULT 'scheduled' CHECK (status IN ('scheduled', 'completed', 'cancelled')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance optimization
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_blood_type ON users(blood_type);

CREATE INDEX idx_requests_blood_type ON blood_requests(blood_type);
CREATE INDEX idx_requests_status ON blood_requests(status);
CREATE INDEX idx_requests_urgency ON blood_requests(urgency);
CREATE INDEX idx_requests_created_at ON blood_requests(created_at DESC);
CREATE INDEX idx_requests_created_by ON blood_requests(created_by);

CREATE INDEX idx_schedule_donor_id ON donation_schedule(donor_id);
CREATE INDEX idx_schedule_scheduled_date ON donation_schedule(scheduled_date);

-- Initialize inventory with all blood types
INSERT INTO inventory (blood_type, units_available) VALUES
    ('A+', 0),
    ('A-', 0),
    ('B+', 0),
    ('B-', 0),
    ('AB+', 0),
    ('AB-', 0),
    ('O+', 0),
    ('O-', 0);

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers to auto-update updated_at
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_requests_updated_at BEFORE UPDATE ON blood_requests
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
