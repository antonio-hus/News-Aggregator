import React, { useState, useEffect } from "react";
import axios from 'axios';
import ArticleFeed from "./ArticleFeed";

function SearchPage() {

    const [query, setQuery] = useState('');
    const [searchPerformed, setSearchPerformed] = useState(false);
    const [endpoint, setEndpoint] = useState('');

    const handleSearch = (e) => {
        e.preventDefault();
        setEndpoint(`http://localhost:8000/api/search/?q=${query}`);
        setSearchPerformed(true);
    }

    return (
        <>
            <h2 style={{ margin: '20px' }}>Search:</h2>
            <form onSubmit={handleSearch}>
                <div className="form-group">
                    <input
                        type="text"
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                        placeholder="Search articles..."
                        className="form-control" style={{ margin: '20px' }}
                    />
                </div>
                <button className="btn btn-primary" style={{ margin: '20px' }} type="submit">Search</button>
            </form>
            {searchPerformed && (
                <ArticleFeed endpoint={endpoint} title={`Articles related to your search:`} permission="any" />
            )}
        </>
    )
}

export default SearchPage;