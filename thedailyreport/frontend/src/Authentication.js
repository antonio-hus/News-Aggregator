import React, { useState } from 'react';
import axios from 'axios';

const Login = ({ setUser }) => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [message, setMessage] = useState('');

    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('http://localhost:8000/api/login/', {
                username,
                password
            });
            setUser({
                isAuthenticated: true,
                username: response.data.username
            });
        } catch (error) {
            setMessage('Invalid username and/or password.');
        }
    };

    return (
        <div>
            <h2>Login</h2>
            {message && <div>{message}</div>}
            <form onSubmit={handleLogin}>
                <div className="form-group">
                    <input className="form-control" style={{ margin: '20px' }} type="text" value={username} onChange={(e) => setUsername(e.target.value)} placeholder="Username" required />
                </div>
                <div className="form-group">
                    <input className="form-control" style={{ margin: '20px' }} type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" required />
                </div>
                <button className="btn btn-primary" style={{ margin: '20px' }} type="submit">Login</button>
            </form>
            <p>Don't have an account? <a href="/register">Register here.</a></p>
        </div>
    );
};

const Logout = ({ setUser }) => {
    const handleLogout = async () => {
        try {
            await axios.post('http://localhost:8000/api/logout/');
            setUser({
                isAuthenticated: false,
                username: ''
            });
        } catch (error) {
            console.error('Logout error:', error);
        }
    };

    return (
        <div>
            <h2>Logout</h2>
            <button className="btn btn-primary" onClick={handleLogout}>Logout</button>
        </div>
    );
};


const Register = ({ setUser }) => {
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmation, setConfirmation] = useState('');
    const [message, setMessage] = useState('');

    const handleRegister = async (e) => {
        e.preventDefault();
        if (password !== confirmation) {
            setMessage('Passwords must match.');
            return;
        }
        try {
            const response = await axios.post('http://localhost:8000/api/register/', {
                username,
                email,
                password,
                confirmation
            });
            setUser({
                isAuthenticated: true,
                username: response.data.username
            });
        } catch (error) {
            setMessage('Username already taken.');
        }
    };

    return (
        <div>
            <h2>Register</h2>
            {message && <div>{message}</div>}
            <form onSubmit={handleRegister}>
                <div className="form-group">
                    <input className="form-control" style={{ margin: '20px' }} type="text" value={username} onChange={(e) => setUsername(e.target.value)} placeholder="Username" required />
                </div>
                <div className="form-group">
                    <input className="form-control" style={{ margin: '20px' }} type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email Address" required />
                </div>
                <div className="form-group">
                    <input className="form-control" style={{ margin: '20px' }} type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" required />
                </div>
                <div className="form-group">
                    <input className="form-control" style={{ margin: '20px' }} type="password" value={confirmation} onChange={(e) => setConfirmation(e.target.value)} placeholder="Confirm Password" required />
                </div>
                <button className="btn btn-primary" style={{ margin: '20px' }} type="submit">Register</button>
            </form>
            <p>Already have an account? <a href="/login">Log In here.</a></p>
        </div>
    );
};

export { Login, Logout, Register };
