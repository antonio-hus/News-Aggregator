import React, { useEffect, useState } from 'react';
import axios from 'axios';

const UserProfile = () => {
    const [userData, setUserData] = useState({});
    const [editMode, setEditMode] = useState(false);
    const [formData, setFormData] = useState({});

    useEffect(() => {
        const fetchUserProfile = async () => {
            try {
                const response = await axios.get('http://localhost:8000/api/user/profile/', {
                    headers: {
                        'Authorization': `Token ${localStorage.getItem('token')}`
                    }
                });
                setUserData(response.data);
                setFormData(response.data);
            } catch (error) {
                console.error('Error fetching user profile:', error);
            }
        };

        fetchUserProfile();
    }, []);

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData({
            ...formData,
            [name]: value,
        });
    };

    const handleEditClick = () => {
        setEditMode(true);
    };

    const handleCancelClick = () => {
        setEditMode(false);
        setFormData(userData); // Reset form data to original
    };

    const handleSubmit = async () => {
        try {
            const response = await axios.put('http://localhost:8000/api/user/profile/update/', formData, {
                headers: {
                    'Authorization': `Token ${localStorage.getItem('token')}`
                },
            });
            setUserData(response.data);
            setEditMode(false);
        } catch (error) {
            console.error('Error updating user profile:', error);
        }
    };

    return (
        <div className="container mt-5">
            <h2>User Profile</h2>
            <div className="card">
                <div className="card-body">
                    <div className="form-group">
                        <label>Username:</label>
                        {editMode ? (
                            <input type="text" className="form-control" name="username" value={formData.username} onChange={handleInputChange} disabled />
                        ) : (
                            <p>{userData.username}</p>
                        )}
                    </div>
                    <div className="form-group">
                        <label>Email:</label>
                        {editMode ? (
                            <input type="email" className="form-control" name="email" value={formData.email} onChange={handleInputChange} disabled />
                        ) : (
                            <p>{userData.email}</p>
                        )}
                    </div>
                    <div className="form-group">
                        <label>First Name:</label>
                        {editMode ? (
                            <input type="text" className="form-control" name="first_name" value={formData.first_name} onChange={handleInputChange} />
                        ) : (
                            <p>{userData.first_name}</p>
                        )}
                    </div>
                    <div className="form-group">
                        <label>Last Name:</label>
                        {editMode ? (
                            <input type="text" className="form-control" name="last_name" value={formData.last_name} onChange={handleInputChange} />
                        ) : (
                            <p>{userData.last_name}</p>
                        )}
                    </div>
                    <div className="form-group">
                        <label>Date Joined:</label>
                        <p>{new Date(userData.date_joined).toLocaleDateString()}</p>
                    </div>
                    <div className="form-group">
                        <label>Last Login:</label>
                        <p>{userData.last_login ? new Date(userData.last_login).toLocaleString() : '-'}</p>
                    </div>
                    <div className="form-group">
                        <label>Date of Birth:</label>
                        {editMode ? (
                            <input type="date" className="form-control" name="date_of_birth" value={formData.date_of_birth} onChange={handleInputChange} />
                        ) : (
                            <p>{userData.date_of_birth ? new Date(userData.date_of_birth).toLocaleDateString() : '-'}</p>
                        )}
                    </div>
                    <div className="form-group">
                        <label>Address:</label>
                        {editMode ? (
                            <input type="text" className="form-control" name="address" value={formData.address} onChange={handleInputChange} />
                        ) : (
                            <p>{userData.address ? userData.address : '-'}</p>
                        )}
                    </div>
                    <div className="form-group">
                        <label>Phone Number:</label>
                        {editMode ? (
                            <input type="text" className="form-control" name="phone_number" value={formData.phone_number} onChange={handleInputChange} />
                        ) : (
                            <p>{userData.phone_number ? userData.phone_number : '-'}</p>
                        )}
                    </div>
                    <div className="form-group">
                        <label>Gender:</label>
                        {editMode ? (
                            <select className="form-control" name="gender" value={formData.gender} onChange={handleInputChange}>
                                <option value="">Select</option>
                                <option value="male">Male</option>
                                <option value="female">Female</option>
                                <option value="other">Other</option>
                            </select>
                        ) : (
                            <p>{userData.gender ? userData.gender : '-'}</p>
                        )}
                    </div>
                    <div className="form-group">
                        <label>Biography:</label>
                        {editMode ? (
                            <textarea className="form-control" name="biography" value={formData.biography} onChange={handleInputChange} />
                        ) : (
                            <p>{userData.biography ? userData.biography : '-'}</p>
                        )}
                    </div>
                    <div className="form-group">
                        <label>Social Media Links:</label>
                        {editMode ? (
                            <input type="text" className="form-control" name="social_media_links" value={formData.social_media_links} onChange={handleInputChange} />
                        ) : (
                            <p>{userData.social_media_links ? userData.social_media_links : '-'}</p>
                        )}
                    </div>

                    {editMode ? (
                        <div>
                            <button className="btn btn-primary mr-2" onClick={handleSubmit}>Save</button>
                            <button className="btn btn-secondary" onClick={handleCancelClick}>Cancel</button>
                        </div>
                    ) : (
                        <button className="btn btn-primary" onClick={handleEditClick}>Edit Profile</button>
                    )}
                </div>
            </div>
        </div>
    );
};

export default UserProfile;