/////////////////////
// IMPORTS SECTION //
/////////////////////
// React Libraries
import React from 'react';


/////////////////
// JSX SECTION //
/////////////////
const NotFound = ({ message }) => {
  return (
    <div className="container text-center mt-5">

      <h1 className="display-1">404</h1>
      <p className="lead">Page Not Found</p>

      {/* Display custom error message*/}
      <p>{message || 'The page you are looking for does not exist.'}</p>

      <a href="/" className="btn btn-primary">Go to Home</a>

    </div>
  );
};

export default NotFound;