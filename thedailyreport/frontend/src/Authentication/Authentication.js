/////////////////////
// IMPORTS SECTION //
/////////////////////
// JavaScript Libraries
import axios from 'axios';
// React Libraries
import React, { useState } from 'react';


//////////////////////
// CODE/JSX SECTION //
//////////////////////
// LOGIN ROUTE
const Login = ({ setUser }) => {

    // Get User Data
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    // Authenticate user via API Route
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

    // JSX Section
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

// LOGOUT ROUTE
const Logout = ({ setUser }) => {

    // Deauthenticate User ( Remove stored session Token )
    const handleLogout = () => {
        localStorage.removeItem('token');
        setUser({
            isAuthenticated: false,
            username: ''
        });
    };

    // JSX Section
    return (
        <>
            <h2 style={{ margin: '20px' }}>Logout</h2>
            <p style={{ margin: '20px' }}>Are you sure you want to logout?</p>
            <button className="btn btn-primary" style={{ margin: '20px' }} onClick={handleLogout}>Logout</button>
        </>
    );
};


// REGISTER ROUTE
const Register = ({ setUser }) => {

    // Get User Data
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmation, setConfirmation] = useState('');
    const [message, setMessage] = useState('');

    // Authenticate user via API Route
    const handleRegister = async (e) => {

        // User must enter the necessary data to register
        e.preventDefault();

        // Password must match confirmation
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

    // JSX Section
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
