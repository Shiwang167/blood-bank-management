import { useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import api from '../api/axios';

const DonorDashboard = () => {
    const { user } = useAuth();
    const navigate = useNavigate();
    const [eligibility, setEligibility] = useState(null);
    const [matchingRequests, setMatchingRequests] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchData();
    }, []);

    const fetchData = async () => {
        try {
            const [eligibilityRes, requestsRes] = await Promise.all([
                api.get('/donor/eligibility'),
                api.get('/donor/matching-requests')
            ]);

            setEligibility(eligibilityRes.data);
            setMatchingRequests(requestsRes.data.matching_requests || []);
        } catch (error) {
            console.error('Error fetching data:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleRespond = async (requestId) => {
        if (!eligibility?.eligible) {
            alert('You are not currently eligible to donate. Please check your eligibility status.');
            return;
        }

        if (!confirm('Are you sure you want to schedule a donation for this request?')) {
            return;
        }

        try {
            await api.post('/donor/schedule', {
                request_id: requestId,
                scheduled_date: new Date().toISOString()
            });

            alert('✅ Donation scheduled successfully! The hospital will contact you soon.');

            // Refresh data to update the list
            fetchData();
        } catch (error) {
            console.error('Error scheduling donation:', error);
            alert(error.response?.data?.error || 'Failed to schedule donation. Please try again.');
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

    const emergencyRequests = matchingRequests.filter(r => r.urgency === 'high');

    return (
        <div className="container">
            <div className="dashboard-header fade-in">
                <h1 className="dashboard-welcome">Welcome back, {user?.name} 👋</h1>
                <p className="dashboard-subtitle">Blood Type: {user?.blood_type}</p>
            </div>

            <div className="widgets-grid">
                {/* Eligibility Widget */}
                <div className="widget fade-in">
                    <div className="widget-header">
                        <span className="widget-icon">{eligibility?.eligible ? '✅' : '⏳'}</span>
                        <h3 className="widget-title">
                            {eligibility?.eligible ? 'Eligible to Donate' : 'Not Eligible Yet'}
                        </h3>
                    </div>
                    <div className="widget-content">
                        {eligibility?.last_donation && (
                            <p>Last donation: {new Date(eligibility.last_donation).toLocaleDateString()}</p>
                        )}
                        {!eligibility?.eligible && (
                            <p>Next eligible: {new Date(eligibility?.next_eligible_date).toLocaleDateString()}</p>
                        )}
                        {eligibility?.eligible && (
                            <p className="mt-1">You can donate blood now!</p>
                        )}
                    </div>
                    {eligibility?.eligible && (
                        <div className="widget-action">
                            <button className="btn btn-primary" onClick={() => navigate('/requests')}>
                                Schedule Donation
                            </button>
                        </div>
                    )}
                </div>

                {/* Emergency Requests Widget */}
                <div className="widget fade-in">
                    <div className="widget-header">
                        <span className="widget-icon">🚨</span>
                        <h3 className="widget-title">Emergency Requests</h3>
                    </div>
                    <div className="widget-content">
                        <div className="widget-stat">{emergencyRequests.length}</div>
                        <p className="widget-label">Your blood type ({user?.blood_type}) needed</p>
                        {emergencyRequests.length > 0 && (
                            <p className="mt-1">Urgent requests waiting for donors</p>
                        )}
                    </div>
                    <div className="widget-action">
                        <button className="btn btn-secondary" onClick={() => navigate('/requests')}>
                            View Requests
                        </button>
                    </div>
                </div>

                {/* Impact Widget */}
                <div className="widget fade-in">
                    <div className="widget-header">
                        <span className="widget-icon">💉</span>
                        <h3 className="widget-title">Your Impact</h3>
                    </div>
                    <div className="widget-content">
                        <p>Total donations: <strong>-</strong></p>
                        <p>Lives potentially saved: <strong>-</strong></p>
                        <p className="mt-1" style={{ fontSize: '0.9rem', fontStyle: 'italic' }}>
                            Start donating to track your impact!
                        </p>
                    </div>
                </div>
            </div>

            {/* Matching Requests Section */}
            <div className="content-section fade-in">
                <div className="section-header">
                    <h2 className="section-title">Matching Blood Requests</h2>
                    <span className="badge badge-primary">{matchingRequests.length} requests</span>
                </div>

                {matchingRequests.length === 0 ? (
                    <div className="empty-state">
                        <div className="empty-state-icon">🩸</div>
                        <p>No matching requests at the moment</p>
                        <p style={{ fontSize: '0.9rem', marginTop: '0.5rem' }}>
                            We'll notify you when someone needs {user?.blood_type} blood
                        </p>
                    </div>
                ) : (
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                        {matchingRequests.map(request => (
                            <div key={request.request_id} className="card">
                                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start' }}>
                                    <div>
                                        <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center', marginBottom: '0.5rem' }}>
                                            <span className={`badge ${request.urgency === 'high' ? 'badge-danger emergency-pulse' : 'badge-warning'}`}>
                                                {request.urgency === 'high' ? '🚨 EMERGENCY' : 'Normal'}
                                            </span>
                                            <span className="badge badge-primary">{request.blood_type}</span>
                                        </div>
                                        <h3 style={{ marginBottom: '0.5rem' }}>{request.hospital_name || 'Hospital'}</h3>
                                        <p style={{ color: 'var(--text-light)', fontSize: '0.9rem' }}>
                                            {request.location || 'Location not specified'} • {request.quantity} units needed
                                        </p>
                                        {request.notes && (
                                            <p style={{ marginTop: '0.5rem', fontSize: '0.9rem' }}>{request.notes}</p>
                                        )}
                                    </div>
                                    <button
                                        className="btn btn-primary"
                                        onClick={() => handleRespond(request.request_id)}
                                    >
                                        Respond
                                    </button>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
};

export default DonorDashboard;
