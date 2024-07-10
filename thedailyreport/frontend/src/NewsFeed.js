import React, { useState, useEffect } from "react";
import axios from 'axios';
import './NewsFeed.css'

function NewsFeed() {
    const [articles, setArticles] = useState([]);

    useEffect(() => {
        axios.get('http://localhost:8000/api/articles_all/')
            .then(response => {
                // Assuming response.data.article_list is the array of articles from your API response
                setArticles(response.data.article_list);
            })
            .catch(error => {
                console.error('Error fetching articles:', error);
            });
    }, []);

    return (
        <div id="news-feed">
            {Array.isArray(articles) && articles.map((article, index) => (
                <div key={index} className="article">
                    <img src={article.img_src} alt="Article Image Source" />
                    <h3>{article.title}</h3>
                    <p>{article.summary}</p>
                    <a href={article.url}>Link</a>
                </div>
            ))}
        </div>
    );
}

export default NewsFeed;
