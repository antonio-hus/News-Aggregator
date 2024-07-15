import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Link, Navigate } from 'react-router-dom';
import axios from 'axios';

import NotFound from './ErrorScreens/404Page';
import UserProfile from "./Profiles/UserProfile";
import SearchPage from "./Articles/SearchPage";
import {NewsFeed, FollowingFeed, FavoriteFeed, ReadLaterFeed, CategoryFeed, TagFeed} from './Articles/NewsFeed';
import PublisherProfile from './Profiles/PublisherProfile';
import { Login, Logout, Register } from './Authentication';
import Sidebar from './WebComponents/Sidebar';
import Disclaimer from "./WebComponents/Disclaimer";

import './App.css';
import ArticleScreen from "./Articles/ArticleScreen";


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
        if (token && token !== "") {
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
        } else {
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
        }
    }, []);

    return (
        <Router>
            <Disclaimer />
            <div className="container-fluid">
                <div className="row flex-nowrap">
                    <Sidebar user={user} isOpen={isSidebarOpen} toggleSidebar={toggleSidebar} />
                    <main className={`main-content ${isSidebarOpen ? 'sidebar-open' : 'sidebar-closed'}`}>
                        <Routes>


                            <Route key="home" exact path="/" element={<NewsFeed />} />
                            <Route key="article" path="/articles/:articleId" element={<ArticleScreen />} />


                            <Route key="user_profile" exact path="/profile" element={<UserProfile />} />
                            <Route key="publisher" path="/publisher/:name" element={<PublisherProfile />} />


                            <Route key="favorite" exact path="/favorite" element={<FavoriteFeed />} />
                            <Route key="read_later" exact path="/read-later" element={<ReadLaterFeed />} />
                            <Route key="following" exact path="/following" element={<FollowingFeed />} />


                            <Route key="search" path="/search" element={<SearchPage />} />
                            <Route key="category" path="/category/:title" element={<CategoryFeed />} />
                            <Route key="tag" path="/tag/:title" element={<TagFeed />} />


                            <Route key="login" path="/login" element={<Login setUser={setUser} />} />
                            <Route key="logout" path="/logout" element={user.isAuthenticated ? <Logout setUser={setUser} /> : <Navigate to="/" />} />
                            <Route key="register" path="/register" element={<Register setUser={setUser} />} />


                            <Route key="404" path="/404" element={<NotFound />} />

                        </Routes>
                    </main>
                </div>
            </div>
        </Router>
    );
}

export default App;
