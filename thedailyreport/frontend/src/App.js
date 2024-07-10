import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Link, Navigate } from 'react-router-dom';
import axios from 'axios';

import AllNews from './NewsFeed';
import { Login, Logout, Register } from './Authentication';
import './App.css';

function App() {
    const [user, setUser] = useState({
        isAuthenticated: false,
        username: ''
    });

    useEffect(() => {
        axios.get('http://localhost:8000/api/user/')
            .then(response => {
                setUser({
                    isAuthenticated: response.data.is_authenticated,
                    username: response.data.username
                });
            })
            .catch(error => {
                console.error('There was an error fetching the user data!', error);
            });
    }, []);

    return (
        <Router>
            <nav className="navbar navbar-expand-lg navbar-light bg-light">
                <Link className="navbar-brand" to="/">The Daily Report</Link>
                <div>
                    <ul className="navbar-nav mr-auto">
                        { user.isAuthenticated && (
                            <li className="nav-item">
                                <Link className="nav-link" to="/user"><strong>{ user.username }</strong></Link>
                            </li>
                        )}
                        <li className="nav-item">
                            <Link className="nav-link" to="/">All News</Link>
                        </li>
                        {user.isAuthenticated ? (
                            <>
                                <li className="nav-item">
                                    <Link className="nav-link" to="#">For You</Link>
                                </li>
                                <li className="nav-item">
                                    <Link className="nav-link" to="/logout">Log Out</Link>
                                </li>
                            </>
                        ) : (
                            <>
                                <li className="nav-item">
                                    <Link className="nav-link" to="/login">Log In</Link>
                                </li>
                                <li className="nav-item">
                                    <Link className="nav-link" to="/register">Register</Link>
                                </li>
                            </>
                        )}
                    </ul>
                </div>
            </nav>
            <div className="body">
                <Routes>
                    <Route exact path="/" element={<AllNews />} />
                    <Route path="/login" element={<Login setUser={setUser} />} />
                    <Route path="/logout" element={user.isAuthenticated ? <Logout setUser={setUser} /> : <Navigate to="/" />} />
                    <Route path="/register" element={<Register setUser={setUser} />} />
                </Routes>
            </div>
        </Router>
    );
}

export default App;
