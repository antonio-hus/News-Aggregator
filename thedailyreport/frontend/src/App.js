import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Link, Navigate } from 'react-router-dom';
import axios from 'axios';

import {NewsFeed, FollowingFeed} from './NewsFeed';
import PublisherProfile from './PublisherProfile';
import { Login, Logout, Register } from './Authentication';
import Sidebar from './Sidebar';
import './App.css';

function App() {
    const [user, setUser] = useState({
        isAuthenticated: false,
        username: ''
    });

    const [isSidebarOpen, setIsSidebarOpen] = useState(true);

    const toggleSidebar = () => {
        setIsSidebarOpen(!isSidebarOpen);
    };

    useEffect(() => {
        const token = localStorage.getItem('token');
        if (token) {
            axios.get('http://localhost:8000/api/user/', {
                headers: {
                    'Authorization': `Token ${token}`
                }
            })
            .then(response => {
                setUser({
                    isAuthenticated: response.data.is_authenticated,
                    username: response.data.username
                });
            })
            .catch(error => {
                console.error('There was an error fetching the user data!', error);
            });
    }
}, []);

    return (
        <Router>
            <div className="container-fluid">
                <div className="row flex-nowrap">
                    <Sidebar user={user} isOpen={isSidebarOpen} toggleSidebar={toggleSidebar} />
                    <main className={`main-content ${isSidebarOpen ? 'sidebar-open' : 'sidebar-closed'}`}>
                        <Routes>
                            <Route exact path="/" element={<NewsFeed />} />
                            <Route exact path="/following" element={<FollowingFeed />} />
                            <Route path="/publisher/:name" element={<PublisherProfile />} />
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
