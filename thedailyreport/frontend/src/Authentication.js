import React, { useState } from 'react';
import axios from 'axios';

const Login = ({ setUser }) => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const handleLogin = (e) => {
        e.preventDefault();
        axios.post('http://localhost:8000/api/login/', { username, password })
            .then(response => {
                const token = response.data.token;
                localStorage.setItem('token', token);
                setUser({
                    isAuthenticated: true,
                    username: username
                });
            })
            .catch(error => {
                console.error('Login error:', error);
            });
    };

    return (
        <>
            <h2 style={{ margin: '20px' }}>Login</h2>
            <form onSubmit={handleLogin}>
                <div className="form-group">
                    <input
                        type="text"
                        placeholder="Username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        className="form-control" style={{ margin: '20px' }}
                    />
                </div>
                <div className="form-group">
                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="form-control" style={{ margin: '20px' }}
                />
                </div>
                <button className="btn btn-primary" style={{ margin: '20px' }} type="submit">Login</button>
            </form>
        </>
    );
};

const Logout = ({ setUser }) => {
    const handleLogout = () => {
        localStorage.removeItem('token');
        setUser({
            isAuthenticated: false,
            username: ''
        });
    };

    return (
        <>
            <h2 style={{ margin: '20px' }}>Logout</h2>
            <p style={{ margin: '20px' }}>Are you sure you want to logout?</p>
            <button className="btn btn-primary" style={{ margin: '20px' }} onClick={handleLogout}>Logout</button>
        </>
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
            localStorage.setItem('token', response.data.token);
            setUser({
                isAuthenticated: true,
                username: response.data.username
            });
        } catch (error) {
            setMessage('Username or email already taken.');
        }
    };

    return (
        <div>
            <h2 style={{ margin: '20px' }}>Register</h2>
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
            <p style={{ margin: '20px' }}>Already have an account? <a href="/login">Log In here.</a></p>
        </div>
    );
};

export { Login, Logout, Register };
