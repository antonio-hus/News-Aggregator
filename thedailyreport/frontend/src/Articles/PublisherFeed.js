/////////////////////
// IMPORTS SECTION //
/////////////////////
// JavaScript Libraries
import axios from 'axios';
// React Libraries
import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
// Style Sheets
import './PublisherFeed.css';


//////////////////////
// CODE/JSX SECTION //
//////////////////////
function PublisherFeed() {

    // Get Publisher List
    const [publishers, setPublishers] = useState([]);
    useEffect(() => {
        const token = localStorage.getItem('token');
        const headers = token ? { 'Authorization': `Token ${token}` } : {};
        axios.get('http://localhost:8000/api/get_publishers/', { headers })
            .then(response => {
                setPublishers(response.data);
            })
            .catch(error => {
                console.error('Error fetching publishers:', error);
            });
    }, []);


    // JSX Section
    return (
        <div id="publisher-feed" className="container">

            <h2>Discover News Sources:</h2>
            <div className="row row-cols-1 row-cols-sm-2 row-cols-md-3 g-4">

                {/* Display All Publishers */}
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
