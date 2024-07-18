/////////////////////
// IMPORTS SECTION //
/////////////////////
// JavaScript Libraries
import axios from 'axios';
// React Libraries
import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
// Project Libraries
import ArticleFeed from "../Articles/ArticleFeed";
import NotFound from "../Errors/404Page";
// Style Sheets
import './PublisherProfile.css';


//////////////////////
// CODE/JSX SECTION //
//////////////////////
// Get User Authentication Status based on token
function isAuthenticated() {
    const token = localStorage.getItem('token');
    return token && token !== "";
}

// Publisher Profile
const PublisherProfile = () => {

    // Get Publisher Data
    const { name } = useParams();
    const [publisher, setPublisher] = useState(null);
    const [isFollowing, setIsFollowing] = useState(false);
    useEffect(() => {
        const token = localStorage.getItem('token');
        const headers = token ? { 'Authorization': `Token ${token}` } : {};
        axios.get(`http://localhost:8000/api/publisher/${name}/`, {headers})
            .then(response => {
                setPublisher(response.data.publisher);
                setIsFollowing(response.data.is_following);
            })
            .catch(error => {
                console.error('There was an error fetching the publisher data!', error);
            });
    }, [name]);

    // Follow / Unfollow Logic Handler
    const handleFollowToggle = () => {
        const token = localStorage.getItem('token');
        const url = isFollowing
            ? `http://localhost:8000/api/publisher/${name}/unfollow/`
            : `http://localhost:8000/api/publisher/${name}/follow/`;

        axios.post(url, {}, {
                headers: {
                    'Authorization': `Token ${token}`
                }
            })
            .then(response => {
                setIsFollowing(!isFollowing);
            })
            .catch(error => {
                console.error('There was an error updating the follow status!', error);
            });
    };

    // JSX SECTION
    // Handle publisher not found case
    if (!publisher) return <NotFound message="Publisher not found." />;
    return (
        <div className="container mt-5">
            <div className="card mb-5">

                <div className="card-header d-flex justify-content-between align-items-center">
                    <h2>{publisher.name}</h2>

                    {/* Display Follow / Unfollow button conditionally to authenticated users */}
                    {isAuthenticated() && (
                        <button
                            className={`btn ${isFollowing ? 'btn-danger' : 'btn-success'}`}
                            onClick={handleFollowToggle}
                        >
                            {isFollowing ? 'Unfollow' : 'Follow'}
                        </button>
                    )}

                </div>

                {/* Display Publisher's data */}
                <div className="card-body">
                    <p><strong>City:</strong> {publisher.city}</p>
                    <p><strong>Address:</strong> {publisher.address}</p>
                    <p><strong>Phone Number:</strong> {publisher.phone_number}</p>
                    <p><strong>Email Address:</strong> {publisher.email_address}</p>
                </div>

            </div>

            {/* Display Publisher's articles */}
            <ArticleFeed
                endpoint={`http://localhost:8000/api/articles_publisher/${name}`}
                title={`Discover Recent Articles from ${publisher.name}:`}
                permission="any"
            />

        </div>
    );
};

export default PublisherProfile;
