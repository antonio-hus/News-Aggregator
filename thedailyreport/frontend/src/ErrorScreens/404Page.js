import React from 'react';

const NotFound = ({ message }) => {
  return (
    <div className="container text-center mt-5">
      <h1 className="display-1">404</h1>
      <p className="lead">Page Not Found</p>
      <p>{message || 'The page you are looking for does not exist.'}</p>
      <a href="/" className="btn btn-primary">Go to Home</a>
    </div>
  );
};

export default NotFound;