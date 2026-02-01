import { useEffect, useState } from 'react';
import Navbar from '../components/Navbar';
import api from '../api/axios';
import './Requests.css';

const Requests = () => {
    const [requests, setRequests] = useState([]);
    const [loading, setLoading] = useState(true);
    const [filter, setFilter] = useState('all');

    useEffect(() => {
        fetchRequests();
    }, []);

    const fetchRequests = async () => {
        try {
            const response = await api.get('/requests');
            setRequests(response.data.requests || []);
        } catch (error) {
            console.error('Error fetching requests:', error);
        } finally {
            setLoading(false);
        }
    };

    const filteredRequests = requests.filter(request => {
        if (filter === 'all') return true;
        if (filter === 'emergency') return request.urgency === 'high';
        if (filter === 'open') return request.status === 'open';
        return true;
    });

    return (
        <div className="requests-page">
            <Navbar />
            <div className="container" style={{ paddingTop: '2rem', paddingBottom: '2rem' }}>
                <div className="page-header fade-in">
                    <h1 className="page-title">Blood Requests</h1>
                    <p className="page-subtitle">View and respond to blood donation requests</p>
                </div>

                {/* Filters */}
                <div className="filters fade-in">
                    <button
                        className={`filter-btn ${filter === 'all' ? 'active' : ''}`}
                        onClick={() => setFilter('all')}
                    >
                        All Requests ({requests.length})
                    </button>
                    <button
                        className={`filter-btn ${filter === 'emergency' ? 'active' : ''}`}
                        onClick={() => setFilter('emergency')}
                    >
                        🚨 Emergency ({requests.filter(r => r.urgency === 'high').length})
                    </button>
                    <button
                        className={`filter-btn ${filter === 'open' ? 'active' : ''}`}
                        onClick={() => setFilter('open')}
                    >
                        Open ({requests.filter(r => r.status === 'open').length})
                    </button>
                </div>

                {/* Requests List */}
                {loading ? (
                    <div className="loading-state">
                        <div className="spinner"></div>
                    </div>
                ) : filteredRequests.length === 0 ? (
                    <div className="empty-state fade-in">
                        <div className="empty-state-icon">🩸</div>
                        <p>No requests found</p>
                    </div>
                ) : (
                    <div className="requests-grid fade-in">
                        {filteredRequests.map(request => (
                            <div key={request.request_id} className="request-card card">
                                <div className="request-header">
                                    <div className="request-badges">
                                        <span className={`badge ${request.urgency === 'high' ? 'badge-danger emergency-pulse' : 'badge-warning'}`}>
                                            {request.urgency === 'high' ? '🚨 EMERGENCY' : 'Normal'}
                                        </span>
                                        <span className="badge badge-primary">{request.blood_type}</span>
                                        <span className={`badge ${request.status === 'open' ? 'badge-warning' : 'badge-success'}`}>
                                            {request.status}
                                        </span>
                                    </div>
                                    <div className="request-quantity">
                                        {request.quantity} units
                                    </div>
                                </div>

                                <h3 className="request-hospital">{request.hospital_name || 'Hospital'}</h3>

                                <div className="request-details">
                                    <div className="detail-item">
                                        <span className="detail-icon">📍</span>
                                        <span>{request.location || 'Location not specified'}</span>
                                    </div>
                                    <div className="detail-item">
                                        <span className="detail-icon">🕒</span>
                                        <span>{new Date(request.timestamp).toLocaleString()}</span>
                                    </div>
                                </div>

                                {request.notes && (
                                    <p className="request-notes">{request.notes}</p>
                                )}

                                {request.status === 'open' && (
                                    <button className="btn btn-primary" style={{ width: '100%', marginTop: '1rem' }}>
                                        Respond to Request
                                    </button>
                                )}
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
};

export default Requests;
