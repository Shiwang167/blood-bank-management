import { useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext';
import api from '../api/axios';

const HospitalDashboard = () => {
    const { user } = useAuth();
    const [requests, setRequests] = useState([]);
    const [loading, setLoading] = useState(true);
    const [showForm, setShowForm] = useState(false);
    const [formData, setFormData] = useState({
        blood_type: 'A+',
        quantity: 1,
        urgency: 'normal',
        hospital_name: user?.hospital_name || '',
        location: user?.location || '',
        notes: ''
    });
    const [submitting, setSubmitting] = useState(false);

    useEffect(() => {
        fetchRequests();
    }, []);

    const fetchRequests = async () => {
        try {
            const response = await api.get('/requests');
            // Filter to show only this hospital's requests
            const myRequests = response.data.requests.filter(
                r => r.created_by === user.user_id
            );
            setRequests(myRequests);
        } catch (error) {
            console.error('Error fetching requests:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setSubmitting(true);

        try {
            await api.post('/requests', formData);
            setShowForm(false);
            setFormData({
                blood_type: 'A+',
                quantity: 1,
                urgency: 'normal',
                hospital_name: user?.hospital_name || '',
                location: user?.location || '',
                notes: ''
            });
            fetchRequests();
        } catch (error) {
            console.error('Error creating request:', error);
            alert(error.response?.data?.error || 'Failed to create request');
        } finally {
            setSubmitting(false);
        }
    };

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
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

    const activeRequests = requests.filter(r => r.status === 'open');
    const fulfilledRequests = requests.filter(r => r.status === 'fulfilled');

    return (
        <div className="container">
            <div className="dashboard-header fade-in">
                <h1 className="dashboard-welcome">Welcome back, {user?.name} 👋</h1>
                <p className="dashboard-subtitle">{user?.hospital_name || 'Hospital Admin'}</p>
            </div>

            <div className="widgets-grid">
                {/* Quick Request Widget */}
                <div className="widget fade-in">
                    <div className="widget-header">
                        <span className="widget-icon">➕</span>
                        <h3 className="widget-title">Create Blood Request</h3>
                    </div>
                    <div className="widget-content">
                        <p>Need blood urgently? Create a request now.</p>
                    </div>
                    <div className="widget-action">
                        <button className="btn btn-primary" onClick={() => setShowForm(true)}>
                            New Request
                        </button>
                    </div>
                </div>

                {/* Active Requests Widget */}
                <div className="widget fade-in">
                    <div className="widget-header">
                        <span className="widget-icon">📋</span>
                        <h3 className="widget-title">Active Requests</h3>
                    </div>
                    <div className="widget-content">
                        <div className="widget-stat">{activeRequests.length}</div>
                        <p className="widget-label">Requests awaiting fulfillment</p>
                    </div>
                </div>

                {/* Fulfilled Widget */}
                <div className="widget fade-in">
                    <div className="widget-header">
                        <span className="widget-icon">✅</span>
                        <h3 className="widget-title">Fulfilled Requests</h3>
                    </div>
                    <div className="widget-content">
                        <div className="widget-stat">{fulfilledRequests.length}</div>
                        <p className="widget-label">Successfully completed</p>
                    </div>
                </div>
            </div>

            {/* Create Request Form */}
            {showForm && (
                <div className="content-section fade-in mb-3">
                    <div className="section-header">
                        <h2 className="section-title">Create Blood Request</h2>
                        <button className="btn btn-secondary" onClick={() => setShowForm(false)}>
                            Cancel
                        </button>
                    </div>

                    <form onSubmit={handleSubmit} style={{ display: 'grid', gap: '1rem', maxWidth: '600px' }}>
                        <div>
                            <label>Blood Type *</label>
                            <select name="blood_type" value={formData.blood_type} onChange={handleChange} required>
                                <option value="A+">A+</option>
                                <option value="A-">A-</option>
                                <option value="B+">B+</option>
                                <option value="B-">B-</option>
                                <option value="O+">O+</option>
                                <option value="O-">O-</option>
                                <option value="AB+">AB+</option>
                                <option value="AB-">AB-</option>
                            </select>
                        </div>

                        <div>
                            <label>Quantity (units) *</label>
                            <input
                                type="number"
                                name="quantity"
                                min="1"
                                value={formData.quantity}
                                onChange={handleChange}
                                required
                            />
                        </div>

                        <div>
                            <label>Urgency *</label>
                            <select name="urgency" value={formData.urgency} onChange={handleChange} required>
                                <option value="normal">Normal</option>
                                <option value="high">🚨 Emergency</option>
                            </select>
                        </div>

                        <div>
                            <label>Hospital Name</label>
                            <input
                                type="text"
                                name="hospital_name"
                                value={formData.hospital_name}
                                onChange={handleChange}
                            />
                        </div>

                        <div>
                            <label>Location</label>
                            <input
                                type="text"
                                name="location"
                                value={formData.location}
                                onChange={handleChange}
                            />
                        </div>

                        <div>
                            <label>Notes</label>
                            <textarea
                                name="notes"
                                rows="3"
                                value={formData.notes}
                                onChange={handleChange}
                                placeholder="Additional information..."
                            />
                        </div>

                        <button type="submit" className="btn btn-primary" disabled={submitting}>
                            {submitting ? 'Creating...' : 'Create Request'}
                        </button>
                    </form>
                </div>
            )}

            {/* Requests List */}
            <div className="content-section fade-in">
                <div className="section-header">
                    <h2 className="section-title">Your Requests</h2>
                </div>

                {requests.length === 0 ? (
                    <div className="empty-state">
                        <div className="empty-state-icon">📋</div>
                        <p>No requests yet</p>
                        <p style={{ fontSize: '0.9rem', marginTop: '0.5rem' }}>
                            Create your first blood request to get started
                        </p>
                    </div>
                ) : (
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                        {requests.map(request => (
                            <div key={request.request_id} className="card">
                                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start' }}>
                                    <div style={{ flex: 1 }}>
                                        <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center', marginBottom: '0.5rem' }}>
                                            <span className={`badge ${request.urgency === 'high' ? 'badge-danger' : 'badge-warning'}`}>
                                                {request.urgency === 'high' ? '🚨 EMERGENCY' : 'Normal'}
                                            </span>
                                            <span className="badge badge-primary">{request.blood_type}</span>
                                            <span className={`badge ${request.status === 'open' ? 'badge-warning' : 'badge-success'}`}>
                                                {request.status}
                                            </span>
                                        </div>
                                        <h3 style={{ marginBottom: '0.5rem' }}>{request.quantity} units needed</h3>
                                        <p style={{ color: 'var(--text-light)', fontSize: '0.9rem' }}>
                                            Created: {new Date(request.timestamp).toLocaleString()}
                                        </p>
                                        {request.notes && (
                                            <p style={{ marginTop: '0.5rem', fontSize: '0.9rem' }}>{request.notes}</p>
                                        )}
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
};

export default HospitalDashboard;
