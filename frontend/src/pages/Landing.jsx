import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './Landing.css';

const Landing = () => {
    const [showAuth, setShowAuth] = useState(false);
    const [isLogin, setIsLogin] = useState(true);
    const [formData, setFormData] = useState({
        name: '',
        email: '',
        password: '',
        role: 'donor',
        blood_type: 'A+',
        phone: '',
        hospital_name: '',
        location: ''
    });
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const { login, register, user } = useAuth();
    const navigate = useNavigate();

    // Redirect if already logged in
    if (user) {
        navigate('/dashboard');
        return null;
    }

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        const result = isLogin
            ? await login(formData.email, formData.password)
            : await register(formData);

        setLoading(false);

        if (result.success) {
            navigate('/dashboard');
        } else {
            setError(result.error);
        }
    };

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    return (
        <div className="landing">
            {/* Hero Section */}
            <section className="hero">
                <div className="hero-content container">
                    <h1 className="hero-title fade-in">
                        🩸 One Click Can Save a Life
                    </h1>
                    <p className="hero-subtitle fade-in">
                        Connect donors, hospitals, and blood banks in real-time to ensure no emergency goes unanswered
                    </p>
                    <div className="hero-buttons fade-in">
                        <button className="btn btn-primary" onClick={() => setShowAuth(true)}>
                            Open App
                        </button>
                        <button className="btn btn-ghost" onClick={() => document.getElementById('how-it-works').scrollIntoView({ behavior: 'smooth' })}>
                            How It Works
                        </button>
                    </div>
                </div>
                <div className="hero-gradient"></div>
            </section>

            {/* How It Works */}
            <section id="how-it-works" className="how-it-works">
                <div className="container">
                    <h2 className="section-title">How BloodBridge Works</h2>
                    <div className="steps">
                        <div className="step-card glass-card fade-in">
                            <div className="step-number">1</div>
                            <div className="step-icon">🏥</div>
                            <h3>Request Created</h3>
                            <p>Hospital creates emergency blood request with urgency level</p>
                        </div>
                        <div className="step-arrow">→</div>
                        <div className="step-card glass-card fade-in">
                            <div className="step-number">2</div>
                            <div className="step-icon">🔔</div>
                            <h3>Donors Notified</h3>
                            <p>Matching donors get instant alert based on blood type</p>
                        </div>
                        <div className="step-arrow">→</div>
                        <div className="step-card glass-card fade-in">
                            <div className="step-number">3</div>
                            <div className="step-icon">🚑</div>
                            <h3>Blood Delivered</h3>
                            <p>Blood reaches patient in time, saving lives</p>
                        </div>
                    </div>
                </div>
            </section>

            {/* Impact Stats */}
            <section className="impact-stats">
                <div className="container">
                    <h2 className="section-title">Lives Saved Today</h2>
                    <div className="stats-grid">
                        <div className="stat-card fade-in">
                            <div className="stat-number">1,247</div>
                            <div className="stat-label">Donors Active</div>
                        </div>
                        <div className="stat-card fade-in">
                            <div className="stat-number">342</div>
                            <div className="stat-label">Requests Fulfilled</div>
                        </div>
                        <div className="stat-card fade-in">
                            <div className="stat-number">89</div>
                            <div className="stat-label">Hospitals Connected</div>
                        </div>
                        <div className="stat-card fade-in">
                            <div className="stat-number">24</div>
                            <div className="stat-label">Emergency Alerts</div>
                        </div>
                    </div>
                </div>
            </section>

            {/* Auth Modal */}
            {showAuth && (
                <div className="modal-backdrop" onClick={() => setShowAuth(false)}>
                    <div className="modal-content glass-card" onClick={(e) => e.stopPropagation()}>
                        <button className="modal-close" onClick={() => setShowAuth(false)}>×</button>

                        <h2 className="modal-title">🩸 BloodBridge</h2>

                        <div className="auth-tabs">
                            <button
                                className={`auth-tab ${isLogin ? 'active' : ''}`}
                                onClick={() => { setIsLogin(true); setError(''); }}
                            >
                                Sign In
                            </button>
                            <button
                                className={`auth-tab ${!isLogin ? 'active' : ''}`}
                                onClick={() => { setIsLogin(false); setError(''); }}
                            >
                                Sign Up
                            </button>
                        </div>

                        <form onSubmit={handleSubmit} className="auth-form">
                            {error && <div className="error-message">{error}</div>}

                            {!isLogin && (
                                <div className="form-group">
                                    <label>Name</label>
                                    <input
                                        type="text"
                                        name="name"
                                        value={formData.name}
                                        onChange={handleChange}
                                        required={!isLogin}
                                    />
                                </div>
                            )}

                            <div className="form-group">
                                <label>Email</label>
                                <input
                                    type="email"
                                    name="email"
                                    value={formData.email}
                                    onChange={handleChange}
                                    required
                                />
                            </div>

                            <div className="form-group">
                                <label>Password</label>
                                <input
                                    type="password"
                                    name="password"
                                    value={formData.password}
                                    onChange={handleChange}
                                    required
                                />
                            </div>

                            {!isLogin && (
                                <>
                                    <div className="form-group">
                                        <label>I am a:</label>
                                        <div className="radio-group">
                                            <label className="radio-label">
                                                <input
                                                    type="radio"
                                                    name="role"
                                                    value="donor"
                                                    checked={formData.role === 'donor'}
                                                    onChange={handleChange}
                                                />
                                                <span>Donor</span>
                                            </label>
                                            <label className="radio-label">
                                                <input
                                                    type="radio"
                                                    name="role"
                                                    value="hospital"
                                                    checked={formData.role === 'hospital'}
                                                    onChange={handleChange}
                                                />
                                                <span>Hospital / Emergency Admin</span>
                                            </label>
                                            <label className="radio-label">
                                                <input
                                                    type="radio"
                                                    name="role"
                                                    value="manager"
                                                    checked={formData.role === 'manager'}
                                                    onChange={handleChange}
                                                />
                                                <span>Blood Bank Manager</span>
                                            </label>
                                        </div>
                                    </div>

                                    {formData.role === 'donor' && (
                                        <div className="form-group">
                                            <label>Blood Type</label>
                                            <select name="blood_type" value={formData.blood_type} onChange={handleChange}>
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
                                    )}

                                    {formData.role === 'hospital' && (
                                        <>
                                            <div className="form-group">
                                                <label>Hospital Name</label>
                                                <input
                                                    type="text"
                                                    name="hospital_name"
                                                    value={formData.hospital_name}
                                                    onChange={handleChange}
                                                />
                                            </div>
                                            <div className="form-group">
                                                <label>Location</label>
                                                <input
                                                    type="text"
                                                    name="location"
                                                    value={formData.location}
                                                    onChange={handleChange}
                                                />
                                            </div>
                                        </>
                                    )}

                                    <div className="form-group">
                                        <label>Phone (optional)</label>
                                        <input
                                            type="tel"
                                            name="phone"
                                            value={formData.phone}
                                            onChange={handleChange}
                                        />
                                    </div>
                                </>
                            )}

                            <button type="submit" className="btn btn-primary" disabled={loading} style={{ width: '100%' }}>
                                {loading ? 'Please wait...' : (isLogin ? 'Sign In' : 'Create Account')}
                            </button>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Landing;
