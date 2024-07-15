import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import ArticleFeed from "../Articles/ArticleFeed";
import NotFound from "../ErrorScreens/404Page";
import './PublisherProfile.css';

function isAuthenticated() {
    const token = localStorage.getItem('token');
    return token && token !== "";
}

const PublisherProfile = () => {
    const { name } = useParams();
    const [publisher, setPublisher] = useState(null);
    const [isFollowing, setIsFollowing] = useState(false);

    useEffect(() => {
        const token = localStorage.getItem('token');
        if (token && token !== ""){
            axios.get(`http://localhost:8000/api/publisher/${name}/`, {
                headers: {
                    'Authorization': `Token ${token}`
                }
            })
                .then(response => {
                    setPublisher(response.data.publisher);
                    setIsFollowing(response.data.is_following);
                })
                .catch(error => {
                    console.error('There was an error fetching the publisher data!', error);
                });
        } else {
            axios.get(`http://localhost:8000/api/publisher/${name}/`)
                .then(response => {
                    setPublisher(response.data.publisher);
                    setIsFollowing(response.data.is_following);
                })
                .catch(error => {
                    console.error('There was an error fetching the publisher data!', error);
                });
        }
    }, [name]);

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

    if (!publisher) return <NotFound message="Publisher not found." />;

    return (
        <div className="container mt-5">
            <div className="card mb-5">
                <div className="card-header d-flex justify-content-between align-items-center">
                    <h2>{publisher.name}</h2>
                    {isAuthenticated() && (
                        <button
                            className={`btn ${isFollowing ? 'btn-danger' : 'btn-success'}`}
                            onClick={handleFollowToggle}
                        >
                            {isFollowing ? 'Unfollow' : 'Follow'}
                        </button>
                    )}
                </div>
                <div className="card-body">
                    <p><strong>City:</strong> {publisher.city}</p>
                    <p><strong>Address:</strong> {publisher.address}</p>
                    <p><strong>Phone Number:</strong> {publisher.phone_number}</p>
                    <p><strong>Email Address:</strong> {publisher.email_address}</p>
                </div>
            </div>
            <ArticleFeed
                endpoint={`http://localhost:8000/api/articles_publisher/${name}`}
                title={`Discover Recent Articles from ${publisher.name}:`}
                permission="any"
            />
        </div>
    );
};

export default PublisherProfile;
