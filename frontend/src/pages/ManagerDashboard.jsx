import { useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext';
import api from '../api/axios';

const ManagerDashboard = () => {
    const { user } = useAuth();
    const [inventory, setInventory] = useState([]);
    const [loading, setLoading] = useState(true);
    const [updating, setUpdating] = useState(null);

    useEffect(() => {
        fetchInventory();
    }, []);

    const fetchInventory = async () => {
        try {
            const response = await api.get('/inventory');
            setInventory(response.data.inventory || []);
        } catch (error) {
            console.error('Error fetching inventory:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleUpdateInventory = async (bloodType, newValue) => {
        setUpdating(bloodType);
        try {
            await api.put('/inventory', {
                blood_type: bloodType,
                units_available: parseInt(newValue)
            });
            fetchInventory();
        } catch (error) {
            console.error('Error updating inventory:', error);
            alert('Failed to update inventory');
        } finally {
            setUpdating(null);
        }
    };

    if (loading) {
        return (
            <div className="container">
                <div className="loading-state">
                    <div className="spinner"></div>
                </div>
            </div>
        );
    }

    const lowStockItems = inventory.filter(item => item.stock_status === 'low' || item.stock_status === 'critical');
    const criticalItems = inventory.filter(item => item.stock_status === 'critical');

    return (
        <div className="container">
            <div className="dashboard-header fade-in">
                <h1 className="dashboard-welcome">Welcome back, {user?.name} 👋</h1>
                <p className="dashboard-subtitle">Blood Bank Manager</p>
            </div>

            <div className="widgets-grid">
                {/* Inventory Overview Widget */}
                <div className="widget fade-in">
                    <div className="widget-header">
                        <span className="widget-icon">🩸</span>
                        <h3 className="widget-title">Blood Inventory</h3>
                    </div>
                    <div className="widget-content">
                        <p>Total blood types tracked: <strong>{inventory.length}</strong></p>
                        <p className="mt-1">Manage inventory levels below</p>
                    </div>
                </div>

                {/* Low Stock Alerts Widget */}
                <div className="widget fade-in">
                    <div className="widget-header">
                        <span className="widget-icon">⚠️</span>
                        <h3 className="widget-title">Low Stock Alerts</h3>
                    </div>
                    <div className="widget-content">
                        <div className="widget-stat" style={{ color: criticalItems.length > 0 ? 'var(--danger)' : 'var(--warning)' }}>
                            {lowStockItems.length}
                        </div>
                        <p className="widget-label">
                            {criticalItems.length > 0 ? `${criticalItems.length} critical` : 'Items need attention'}
                        </p>
                    </div>
                </div>

                {/* Today's Activity Widget */}
                <div className="widget fade-in">
                    <div className="widget-header">
                        <span className="widget-icon">📊</span>
                        <h3 className="widget-title">Today's Activity</h3>
                    </div>
                    <div className="widget-content">
                        <p>Donations received: <strong>-</strong></p>
                        <p>Units distributed: <strong>-</strong></p>
                        <p>Requests fulfilled: <strong>-</strong></p>
                    </div>
                </div>
            </div>

            {/* Blood Inventory Grid */}
            <div className="content-section fade-in">
                <div className="section-header">
                    <h2 className="section-title">Blood Type Availability</h2>
                </div>

                <div style={{ display: 'grid', gap: '1rem' }}>
                    {inventory.map(item => {
                        const percentage = Math.min((item.units_available / 20) * 100, 100);
                        const statusColor =
                            item.stock_status === 'critical' ? 'var(--danger)' :
                                item.stock_status === 'low' ? 'var(--warning)' :
                                    'var(--success)';

                        return (
                            <div key={item.blood_type} className="card">
                                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: '2rem' }}>
                                    <div style={{ flex: 1 }}>
                                        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '0.75rem' }}>
                                            <h3 style={{ fontSize: '1.5rem', fontWeight: '700', minWidth: '60px' }}>
                                                {item.blood_type}
                                            </h3>
                                            <div style={{ flex: 1, height: '12px', background: '#e9ecef', borderRadius: '6px', overflow: 'hidden' }}>
                                                <div
                                                    style={{
                                                        height: '100%',
                                                        width: `${percentage}%`,
                                                        background: statusColor,
                                                        transition: 'width 0.3s ease'
                                                    }}
                                                />
                                            </div>
                                            <span style={{ fontWeight: '700', fontSize: '1.2rem', minWidth: '80px', textAlign: 'right' }}>
                                                {item.units_available} units
                                            </span>
                                            <span style={{ fontSize: '1.5rem' }}>
                                                {item.stock_status === 'critical' ? '🚨' :
                                                    item.stock_status === 'low' ? '⚠️' : '✅'}
                                            </span>
                                        </div>
                                        <p style={{ color: 'var(--text-light)', fontSize: '0.85rem' }}>
                                            Last updated: {new Date(item.last_updated).toLocaleString()}
                                        </p>
                                    </div>
                                    <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
                                        <input
                                            type="number"
                                            min="0"
                                            defaultValue={item.units_available}
                                            style={{ width: '80px' }}
                                            onKeyPress={(e) => {
                                                if (e.key === 'Enter') {
                                                    handleUpdateInventory(item.blood_type, e.target.value);
                                                }
                                            }}
                                            id={`input-${item.blood_type}`}
                                        />
                                        <button
                                            className="btn btn-primary"
                                            onClick={() => {
                                                const input = document.getElementById(`input-${item.blood_type}`);
                                                handleUpdateInventory(item.blood_type, input.value);
                                            }}
                                            disabled={updating === item.blood_type}
                                        >
                                            {updating === item.blood_type ? '...' : 'Update'}
                                        </button>
                                    </div>
                                </div>
                            </div>
                        );
                    })}
                </div>
            </div>

            {/* Low Stock Details */}
            {lowStockItems.length > 0 && (
                <div className="content-section fade-in mt-3">
                    <div className="section-header">
                        <h2 className="section-title">⚠️ Low Stock Details</h2>
                    </div>

                    <div style={{ display: 'grid', gap: '1rem' }}>
                        {lowStockItems.map(item => (
                            <div key={item.blood_type} className="card" style={{ borderLeft: `4px solid ${item.stock_status === 'critical' ? 'var(--danger)' : 'var(--warning)'}` }}>
                                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                    <div>
                                        <h3 style={{ marginBottom: '0.25rem' }}>
                                            {item.blood_type} - {item.units_available} units
                                        </h3>
                                        <p style={{ color: 'var(--text-light)', fontSize: '0.9rem' }}>
                                            {item.stock_status === 'critical' ? '🚨 Critical - Immediate action required' : '⚠️ Low stock - Please restock soon'}
                                        </p>
                                    </div>
                                    <span className={`badge ${item.stock_status === 'critical' ? 'badge-danger' : 'badge-warning'}`}>
                                        {item.stock_status}
                                    </span>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
};

export default ManagerDashboard;
