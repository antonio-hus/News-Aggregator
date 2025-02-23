/////////////////////
// IMPORTS SECTION //
/////////////////////
// React Libraries
import React from 'react';
import { Link } from 'react-router-dom';


//////////////////////
// CODE/JSX SECTION //
//////////////////////
const Sidebar = ({ user, isOpen, toggleSidebar }) => (

    <nav className={`col-md-3 col-lg-2 d-md-block bg-light sidebar ${isOpen ? 'open' : 'closed'}`}>
        <div className="position-sticky pt-3 d-flex flex-column justify-content-center align-items-center h-100">

            <ul className="nav flex-column align-items-center">

                {/* Display routes conditionally based on authentication status*/}
                {/* Extended information provided on opened sidebar*/}
                {user.isAuthenticated && (
                    <li className="nav-item">
                        <Link className="nav-link d-flex align-items-center" to="/profile">
                            <i className="bi bi-person me-2 fs-5"></i> {isOpen && user.username}
                        </Link>
                    </li>
                )}
                <li className="nav-item">
                    <Link className="nav-link d-flex align-items-center" to="/search">
                        <i className="bi bi-search me-2 fs-5"></i> {isOpen && 'Search Articles'}
                    </Link>
                </li>
                <li className="nav-item">
                    <Link className="nav-link d-flex align-items-center" to="/">
                        <i className="bi bi-fire me-2 fs-5"></i> {isOpen && 'Newest Articles'}
                    </Link>
                </li>
                {user.isAuthenticated && (
                <li className="nav-item">
                    <Link className="nav-link d-flex align-items-center" to="/following">
                        <i className="bi bi-broadcast me-2 fs-5"></i> {isOpen && 'Following Articles'}
                    </Link>
                </li>
                )}
                {user.isAuthenticated && (
                <li className="nav-item">
                    <Link className="nav-link d-flex align-items-center" to="/favorite">
                        <i className="bi bi-heart me-2 fs-5"></i> {isOpen && 'Favorite Articles'}
                    </Link>
                </li>
                )}
                {user.isAuthenticated && (
                <li className="nav-item">
                    <Link className="nav-link d-flex align-items-center" to="/read-later">
                        <i className="bi bi-clock me-2 fs-5"></i> {isOpen && 'Read Later Articles'}
                    </Link>
                </li>
                )}
                {user.isAuthenticated ? (
                    <li className="nav-item">
                        <Link className="nav-link d-flex align-items-center" to="/logout">
                            <i className="bi bi-box-arrow-right me-2 fs-5"></i> {isOpen && 'Log Out'}
                        </Link>
                    </li>
                ) : (
                    <>
                        <li className="nav-item">
                            <Link className="nav-link d-flex align-items-center" to="/login">
                                <i className="bi bi-box-arrow-in-right me-2 fs-5"></i> {isOpen && 'Log In'}
                            </Link>
                        </li>
                        <li className="nav-item">
                            <Link className="nav-link d-flex align-items-center" to="/register">
                                <i className="bi bi-person-plus me-2 fs-5"></i> {isOpen && 'Register'}
                            </Link>
                        </li>
                    </>
                )}

                {/* Sidebar Toggle Button */}
                <li className="nav-item">
                    <div className="sidebar-toggle mt-auto" onClick={toggleSidebar}>
                        {isOpen ? (
                            <i className="bi bi-chevron-left fs-5"></i>
                        ) : (
                            <i className="bi bi-chevron-right fs-5"></i>
                        )}
                    </div>
                </li>

            </ul>

        </div>
    </nav>
);

export default Sidebar;
