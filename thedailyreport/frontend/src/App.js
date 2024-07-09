import logo from './logo.svg';
import './App.css';
import {useState, useEffect} from "react";
import AllNews from './NewsFeed';
import axios from 'axios';

function App() {

    const [user, setUser] = useState({
        isAuthenticated: false,
        username: ''
    });

    useEffect(() => {
        axios.get('http://localhost:8000/api/user/')
            .then(response => {
                setUser({
                    isAuthenticated: response.data.is_authenticated,
                    username: response.data.username
                });
            })
            .catch(error => {
                console.error('There was an error fetching the user data!', error);
            });
    }, []);

    return (
        <>
            <nav className="navbar navbar-expand-lg navbar-light bg-light">

                <a className="navbar-brand" href="/">The Daily Report</a>
                <div>
                  <ul className="navbar-nav mr-auto">

                    { user.isAuthenticated && (
                        <li className="nav-item">
                            <a className="nav-link" href="/user"><strong>{ user.username }</strong></a>
                        </li>
                    )}

                    <li className="nav-item">
                      <a className="nav-link" href="/">All News</a>
                    </li>

                    {user.isAuthenticated ? (
                          <>
                            <li className="nav-item">
                              <a className="nav-link" href="#">For You</a>
                            </li>
                            <li className="nav-item">
                              <a className="nav-link" href="/logout">Log Out</a>
                            </li>
                          </>
                    ) : (
                          <>
                            <li className="nav-item">
                              <a className="nav-link" href="/login">Log In</a>
                            </li>
                            <li className="nav-item">
                              <a className="nav-link" href="/register">Register</a>
                            </li>
                          </>
                    )}

                  </ul>
                </div>
            </nav>

            <div className="body">
                <AllNews/>
            </div>
          </>
    );
}

export default App;
