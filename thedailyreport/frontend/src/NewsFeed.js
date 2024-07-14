import React, { useState, useEffect } from "react";
import axios from 'axios';
import './NewsFeed.css'

function ArticleFeed({ endpoint, title }) {
    const [articles, setArticles] = useState([]);
    const [sortedArticles, setSortedArticles] = useState([]);
    const [sortOption, setSortOption] = useState("");
    const [sortOrder, setSortOrder] = useState("asc");

    useEffect(() => {
        fetchAndSortArticles(endpoint);
    }, []);

    useEffect(() => {
        sortArticles();
    }, [sortOption, sortOrder, articles]);

    const fetchAndSortArticles = (endpoint) => {
        axios.get(endpoint)
            .then(response => {
                setArticles(response.data);
                setSortedArticles(response.data); // Initialize sorted articles
            })
            .catch(error => {
                console.error('Error fetching articles:', error);
            });
    };

    const sortArticles = () => {
        let sorted = [...articles];

        if (sortOption === "title") {
            sorted.sort((a, b) => {
                return sortOrder === "asc" ? a.title.localeCompare(b.title) : b.title.localeCompare(a.title);
            });
        } else if (sortOption === "publish_date") {
            sorted.sort((a, b) => {
                return sortOrder === "asc" ? new Date(a.publish_date) - new Date(b.publish_date) : new Date(b.publish_date) - new Date(a.publish_date);
            });
        } else if (sortOption === "category") {
            sorted.sort((a, b) => {
                return sortOrder === "asc" ? a.category.title.localeCompare(b.category.title) : b.category.title.localeCompare(a.category.title);
            });
        } else if (sortOption === "publisher") {
            sorted.sort((a, b) => {
                return sortOrder === "asc" ? a.publisher.name.localeCompare(b.publisher.name) : b.publisher.name.localeCompare(a.publisher.name);
            });
        }

        setSortedArticles(sorted);
    };

    if (articles.length === 0) {
        return (
            <>
                <h2 style={{ margin: '30px' }}>{title}</h2>
                <p style={{ margin: '30px' }}>There is nothing to show here!</p>
            </>
        );
    }

    return (
        <div id="news-feed" className="container">
            <h2>{title}</h2>
            <br/>
            <div className="sort-options mb-4">
                <div className="row">
                    <p>Filter Content by:</p>
                    <div className="col-md-3">
                        <select
                            className="form-control"
                            value={sortOption}
                            onChange={e => setSortOption(e.target.value)}
                        >
                            <option value="">Sort by</option>
                            <option value="title">Title</option>
                            <option value="publish_date">Publish Date</option>
                            <option value="category">Category</option>
                            <option value="publisher">Publisher</option>
                        </select>
                    </div>
                    <div className="col-md-3">
                        <select
                            className="form-control"
                            value={sortOrder}
                            onChange={e => setSortOrder(e.target.value)}
                        >
                            <option value="asc">Ascending</option>
                            <option value="desc">Descending</option>
                        </select>
                    </div>
                </div>
            </div>
            {sortedArticles.map((article, index) => (
                <div key={index} className="article row mb-3">
                    <div className="col-md-4 d-flex align-items-center justify-content-center">
                        {article.media_preview && <img src={article.media_preview.url} className="img-fluid" alt="Article Media Preview" />}
                    </div>
                    <div className="col-md-8">
                        <div className="card-body">
                            <h3 className="card-title">{article.title}</h3>
                            <p className="card-text">{article.provided_summary}</p>
                            <p className="card-text"><small className="text-muted">Published: {new Date(article.publish_date).toLocaleString('en-US', {
                                year: 'numeric', month: '2-digit', day: '2-digit',
                                hour: '2-digit', minute: '2-digit',
                            })}</small></p>
                            <div className="mb-2">
                                <strong>Publisher:</strong> {article.publisher ? article.publisher.name : 'Unknown Publisher'}
                            </div>
                            <div className="mb-2">
                                <strong>Category:</strong> {article.category ? article.category.title : 'Uncategorized'}
                            </div>
                            <div className="mb-2">
                                <strong>Tags:</strong> {article.tags.map(tag => (
                                    <span key={tag.id} className="badge bg-primary mr-5">{tag.title}</span>
                                ))}
                            </div>
                            <a href={article.url} className="btn btn-primary">Read More</a>
                        </div>
                    </div>
                </div>
            ))}
        </div>
    );
}

function NewsFeed() {
    return <ArticleFeed endpoint="http://localhost:8000/api/articles_all/" title="Discover Recent Articles:" />;
}

function FollowingFeed() {
    return <ArticleFeed endpoint="http://localhost:8000/api/articles_following/" title="From your Favourite News Sources:" />;
}

export {NewsFeed, FollowingFeed};
