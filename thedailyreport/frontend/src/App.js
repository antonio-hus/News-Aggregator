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
            <div className="container-fluid">
                <div className="row">
                    <nav className="col-md-3 col-lg-2 d-md-block bg-light sidebar">
                        <div className="position-sticky pt-3">
                            <ul className="nav flex-column">
                                <li className="nav-item">
                                    <Link className="navbar-brand nav-link" to="/">The Daily Report</Link>
                                </li>
                                {user.isAuthenticated && (
                                    <li className="nav-item">
                                        <Link className="nav-link" to="/user"><strong>{user.username}</strong></Link>
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
                    <main className="col-md-9 ms-sm-auto col-lg-10 px-md-4">
                        <Routes>
                            <Route exact path="/" element={<AllNews />} />
                            <Route path="/login" element={<Login setUser={setUser} />} />
                            <Route path="/logout" element={user.isAuthenticated ? <Logout setUser={setUser} /> : <Navigate to="/" />} />
                            <Route path="/register" element={<Register setUser={setUser} />} />
                        </Routes>
                    </main>
                </div>
            </div>
        </Router>
    );
}

export default App;
