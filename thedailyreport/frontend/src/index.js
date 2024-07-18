/////////////////////
// IMPORTS SECTION //
/////////////////////
// React Libraries
import React from 'react';
import ReactDOM from 'react-dom/client';
// Bootstrap Libraries
import 'bootstrap-icons/font/bootstrap-icons.css';
import 'bootstrap/dist/css/bootstrap.min.css';
// Project Libraries
import App from './App';
// Stylesheets
import './Stylesheet.scss';
import './index.css';

/////////////////
// JSX SECTION //
/////////////////
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
