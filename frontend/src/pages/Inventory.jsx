import { useEffect, useState } from 'react';
import Navbar from '../components/Navbar';
import api from '../api/axios';

const Inventory = () => {
    const [inventory, setInventory] = useState([]);
    const [loading, setLoading] = useState(true);

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

    return (
        <div style={{ minHeight: '100vh', background: 'var(--light-bg)' }}>
            <Navbar />
            <div className="container" style={{ paddingTop: '2rem', paddingBottom: '2rem' }}>
                <div className="page-header fade-in">
                    <h1 className="page-title">Blood Inventory</h1>
                    <p className="page-subtitle">Current blood stock levels across all blood types</p>
                </div>

                {loading ? (
                    <div className="loading-state">
                        <div className="spinner"></div>
                    </div>
                ) : (
                    <div className="content-section fade-in">
                        <div style={{ display: 'grid', gap: '1.5rem' }}>
                            {inventory.map(item => {
                                const percentage = Math.min((item.units_available / 20) * 100, 100);
                                const statusColor =
                                    item.stock_status === 'critical' ? 'var(--danger)' :
                                        item.stock_status === 'low' ? 'var(--warning)' :
                                            'var(--success)';

                                return (
                                    <div key={item.blood_type} className="card">
                                        <div style={{ display: 'flex', alignItems: 'center', gap: '2rem' }}>
                                            <div style={{ minWidth: '80px' }}>
                                                <h2 style={{ fontSize: '2rem', fontWeight: '700', color: 'var(--primary-red)' }}>
                                                    {item.blood_type}
                                                </h2>
                                            </div>

                                            <div style={{ flex: 1 }}>
                                                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                                                    <span style={{ fontWeight: '600' }}>{item.units_available} units available</span>
                                                    <span className={`badge ${item.stock_status === 'critical' ? 'badge-danger' :
                                                            item.stock_status === 'low' ? 'badge-warning' :
                                                                'badge-success'
                                                        }`}>
                                                        {item.stock_status}
                                                    </span>
                                                </div>
                                                <div style={{ height: '16px', background: '#e9ecef', borderRadius: '8px', overflow: 'hidden' }}>
                                                    <div
                                                        style={{
                                                            height: '100%',
                                                            width: `${percentage}%`,
                                                            background: statusColor,
                                                            transition: 'width 0.3s ease'
                                                        }}
                                                    />
                                                </div>
                                                <p style={{ fontSize: '0.85rem', color: 'var(--text-light)', marginTop: '0.5rem' }}>
                                                    Last updated: {new Date(item.last_updated).toLocaleString()}
                                                </p>
                                            </div>

                                            <div style={{ fontSize: '2rem' }}>
                                                {item.stock_status === 'critical' ? '🚨' :
                                                    item.stock_status === 'low' ? '⚠️' : '✅'}
                                            </div>
                                        </div>
                                    </div>
                                );
                            })}
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default Inventory;
