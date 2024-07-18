/////////////////////
// IMPORTS SECTION //
/////////////////////
// React Libraries
import React, { useState } from 'react';


//////////////////////
// CODE/JSX SECTION //
//////////////////////
const Disclaimer = () => {

  // Close Disclaimer Bar Logic
  const [visible, setVisible] = useState(true);
  const handleClose = () => {
    setVisible(false);
  };

  //JSX Section
  return (
    visible && (
      <div className="sticky-top bg-danger text-white p-2 d-flex justify-content-between align-items-center">
        <span>This website is not meant for public or commercial use! - Made by Antonio Hus (https://www.linkedin.com/in/antonio-hus/) as part of CV</span>
        <button className="btn btn-light btn-sm" onClick={handleClose}>X</button>
      </div>
    )
  );
};

export default Disclaimer;
