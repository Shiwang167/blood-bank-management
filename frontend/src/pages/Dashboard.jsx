import { useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext';
import Navbar from '../components/Navbar';
import DonorDashboard from './DonorDashboard';
import HospitalDashboard from './HospitalDashboard';
import ManagerDashboard from './ManagerDashboard';
import './Dashboard.css';

const Dashboard = () => {
    const { user } = useAuth();

    const renderDashboard = () => {
        switch (user?.role) {
            case 'donor':
                return <DonorDashboard />;
            case 'hospital':
                return <HospitalDashboard />;
            case 'manager':
                return <ManagerDashboard />;
            default:
                return <div>Invalid role</div>;
        }
    };

    return (
        <div className="dashboard-page">
            <Navbar />
            <div className="dashboard-container">
                {renderDashboard()}
            </div>
        </div>
    );
};

export default Dashboard;
