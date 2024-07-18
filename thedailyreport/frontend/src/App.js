/////////////////////
// IMPORTS SECTION //
/////////////////////
// JavaScript Libraries
import axios from 'axios';
// React Libraries
import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
// Project Libraries
import { NewsFeed, FollowingFeed, FavoriteFeed, ReadLaterFeed, CategoryFeed, TagFeed, CollaborativeFilteringFeed, ContentFilteringFeed} from './Articles/NewsFeed';
import ArticleScreen from "./Articles/ArticleScreen";
import PublisherFeed from "./Articles/PublisherFeed";
import SearchPage from "./Articles/SearchPage";
import { Login, Logout, Register } from './Authentication/Authentication';
import PublisherProfile from './Profiles/PublisherProfile';
import UserProfile from "./Profiles/UserProfile";
import Sidebar from './Components/Sidebar';
import Disclaimer from "./Components/Disclaimer";
import NotFound from './Errors/404Page';
// Style Sheets
import './App.css';


//////////////////////
// CODE/JSX SECTION //
//////////////////////
function App() {

    // Basic User Information Holder
    const [user, setUser] = useState({
        isAuthenticated: false,
        username: ''
    });

    // Get Basic User Information
    useEffect(() => {
        const token = localStorage.getItem('token');
        const headers = token ? { 'Authorization': `Token ${token}` } : {};

        axios.get('http://localhost:8000/api/user/', { headers })
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

    // Sidebar Functionality
    const [isSidebarOpen, setIsSidebarOpen] = useState(true);
    const toggleSidebar = () => {
        setIsSidebarOpen(!isSidebarOpen);
    };

    // JSX Code
    return (
        <Router>
            <Disclaimer />
            <div className="container-fluid">
                <div className="row flex-nowrap">

                    {/* Sidebar on the left */}
                    <Sidebar user={user} isOpen={isSidebarOpen} toggleSidebar={toggleSidebar} />
                    <main className={`main-content ${isSidebarOpen ? 'sidebar-open' : 'sidebar-closed'}`}>
                        <Routes>

                            {/* Home Route */}
                            <Route key="home" exact path="/" element={
                                <>
                                    <PublisherFeed />
                                    <NewsFeed />
                                    <ContentFilteringFeed />
                                    <CollaborativeFilteringFeed />
                                </>
                            } />

                            {/* Article Page Route */}
                            <Route key="article" path="/articles/:articleId" element={<ArticleScreen />} />

                            {/* Profile Routes */}
                            <Route key="user_profile" exact path="/profile" element={<UserProfile />} />
                            <Route key="publisher" path="/publisher/:name" element={<PublisherProfile />} />

                            {/* User's News Feed Route */}
                            <Route key="favorite" exact path="/favorite" element={<FavoriteFeed />} />
                            <Route key="read_later" exact path="/read-later" element={<ReadLaterFeed />} />
                            <Route key="following" exact path="/following" element={<FollowingFeed />} />

                            {/* Categorized News Feed Routes */}
                            <Route key="search" path="/search" element={<SearchPage />} />
                            <Route key="category" path="/category/:title" element={<CategoryFeed />} />
                            <Route key="tag" path="/tag/:title" element={<TagFeed />} />

                            {/* Authentication Routes */}
                            <Route key="login" path="/login" element={<Login setUser={setUser} />} />
                            <Route key="logout" path="/logout" element={user.isAuthenticated ? <Logout setUser={setUser} /> : <Navigate to="/" />} />
                            <Route key="register" path="/register" element={<Register setUser={setUser} />} />

                            {/* Bad Response Routes */}
                            <Route key="404" path="/404" element={<NotFound />} />

                        </Routes>
                    </main>
                </div>
            </div>
        </Router>
    );
}

export default App;
