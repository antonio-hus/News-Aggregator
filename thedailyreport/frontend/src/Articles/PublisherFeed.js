import React, { useState, useEffect } from "react";
import axios from 'axios';
import { Link } from "react-router-dom";
import './PublisherFeed.css';

function PublisherFeed() {
    const [publishers, setPublishers] = useState([]);

    useEffect(() => {
        const token = localStorage.getItem('token');
        if (token && token !== "") {
            axios.get('http://localhost:8000/api/get_publishers/', {
                headers: { 'Authorization': `Token ${token}` }
            })
                .then(response => {
                    setPublishers(response.data);
                })
                .catch(error => {
                    console.error('Error fetching publishers:', error);
                });
        } else {
            axios.get('http://localhost:8000/api/get_publishers/')
                .then(response => {
                    setPublishers(response.data);
                })
                .catch(error => {
                    console.error('Error fetching publishers:', error);
                });
        }
    }, []);

    return (
        <div id="publisher-feed" className="container">
            <h2>Discover News Sources:</h2>
            <div className="row row-cols-1 row-cols-sm-2 row-cols-md-3 g-4">
                {publishers.map(publisher => (
                    <div key={publisher.id} className="col">
                        <div className="card h-100">
                            <div className="card-body">
                                <Link to={`/publisher/${encodeURIComponent(publisher.name)}`} className="link-no-underline">
                                  <h5 className="card-title">{publisher.name}</h5>
                                </Link>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default PublisherFeed;
