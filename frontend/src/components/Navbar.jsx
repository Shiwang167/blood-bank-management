import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './Navbar.css';

const Navbar = () => {
    const { user, logout } = useAuth();
    const navigate = useNavigate();

    const handleLogout = () => {
        logout();
        navigate('/');
    };

    const getRoleBadge = (role) => {
        const badges = {
            donor: { text: 'Donor', class: 'badge-success' },
            hospital: { text: 'Hospital', class: 'badge-primary' },
            manager: { text: 'Manager', class: 'badge-warning' }
        };
        return badges[role] || badges.donor;
    };

    const badge = getRoleBadge(user?.role);

    return (
        <nav className="navbar">
            <div className="container navbar-content">
                <Link to="/dashboard" className="navbar-brand">
                    🩸 BloodBridge
                </Link>

                <div className="navbar-links">
                    <Link to="/dashboard" className="nav-link">Dashboard</Link>
                    <Link to="/requests" className="nav-link">Requests</Link>
                    <Link to="/inventory" className="nav-link">Inventory</Link>
                </div>

                <div className="navbar-user">
                    <span className="user-name">{user?.name}</span>
                    <span className={`badge ${badge.class}`}>{badge.text}</span>
                    <button onClick={handleLogout} className="btn-logout">Logout</button>
                </div>
            </div>
        </nav>
    );
};

export default Navbar;
