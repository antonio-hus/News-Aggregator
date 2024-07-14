import React from 'react';
import { Link } from 'react-router-dom';
import 'bootstrap-icons/font/bootstrap-icons.css';

const Sidebar = ({ user, isOpen, toggleSidebar }) => (
    <nav className={`col-md-3 col-lg-2 d-md-block bg-light sidebar ${isOpen ? 'open' : 'closed'}`}>
        <div className="position-sticky pt-3 d-flex flex-column justify-content-center align-items-center h-100">
            <ul className="nav flex-column align-items-center">
                {user.isAuthenticated && (
                    <li className="nav-item">
                        <Link className="nav-link d-flex" to="/user">
                            <i className="bi bi-person me-2 fs-5 align-items-center"></i> {isOpen && user.username}
                        </Link>
                    </li>
                )}
                <li className="nav-item">
                    <Link className="nav-link d-flex" to="/">
                        <i className="bi bi-fire me-2 fs-5 align-items-center"></i> {isOpen && 'Newest Articles'}
                    </Link>
                </li>
                {user.isAuthenticated && (
                <li className="nav-item">
                    <Link className="nav-link d-flex" to="/">
                        <i className="bi bi-broadcast me-2 fs-5 align-items-center"></i> {isOpen && 'Following Articles'}
                    </Link>
                </li>
                )}
                {user.isAuthenticated && (
                <li className="nav-item">
                    <Link className="nav-link d-flex" to="/">
                        <i className="bi bi-heart me-2 fs-5 align-items-center"></i> {isOpen && 'Favorite Articles'}
                    </Link>
                </li>
                )}
                {user.isAuthenticated && (
                <li className="nav-item">
                    <Link className="nav-link d-flex" to="/">
                        <i className="bi bi-clock me-2 fs-5 align-items-center"></i> {isOpen && 'Read Later Articles'}
                    </Link>
                </li>
                )}
                {user.isAuthenticated ? (
                    <li className="nav-item">
                        <Link className="nav-link d-flex" to="/logout">
                            <i className="bi bi-box-arrow-right me-2 fs-5 align-items-center"></i> {isOpen && 'Log Out'}
                        </Link>
                    </li>
                ) : (
                    <>
                        <li className="nav-item">
                            <Link className="nav-link d-flex" to="/login">
                                <i className="bi bi-box-arrow-in-right me-2 fs-5 align-items-center"></i> {isOpen && 'Log In'}
                            </Link>
                        </li>
                        <li className="nav-item">
                            <Link className="nav-link d-flex" to="/register">
                                <i className="bi bi-person-plus me-2 fs-5 align-items-center"></i> {isOpen && 'Register'}
                            </Link>
                        </li>
                    </>
                )}
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
