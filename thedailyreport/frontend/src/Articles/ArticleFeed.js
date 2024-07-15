import React, { useState, useEffect } from "react";
import axios from 'axios';
import './ArticleFeed.css'
import {Link} from "react-router-dom";

function isAuthenticated() {
    const token = localStorage.getItem('token');
    return token && token !== "";
}

function ArticleFeed({ endpoint, title, permission }) {
    const [articles, setArticles] = useState([]);
    const [sortedArticles, setSortedArticles] = useState([]);
    const [sortOption, setSortOption] = useState("");
    const [sortOrder, setSortOrder] = useState("asc");

    useEffect(() => {
        fetchAndSortArticles(endpoint);
    }, [endpoint]);

    useEffect(() => {
        sortArticles();
    }, [sortOption, sortOrder, articles]);

    const fetchAndSortArticles = (endpoint) => {
        const token = localStorage.getItem('token');
        if ((token && token !== "") || permission === "auth") {
            axios.get(endpoint, {
                headers: {
                    'Authorization': `Token ${token}`
                }
            })
                .then(response => {
                    setArticles(response.data);
                    setSortedArticles(response.data);
                })
                .catch(error => {
                    console.error('Error fetching articles:', error);
                });
        }
        else if (permission === "any") {
            axios.get(endpoint)
                .then(response => {
                    setArticles(response.data);
                    setSortedArticles(response.data);
                })
                .catch(error => {
                    console.error('Error fetching articles:', error);
                });
        }
        else {
            console.error('Error fetching articles: Invalid Permission');
        }
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

    const handleFavorite = (articleId) => {
        const token = localStorage.getItem('token');
        axios.post(`http://localhost:8000/api/articles/${articleId}/favorite`, {}, {
            headers: {
                'Authorization': `Token ${token}`
            }
        })
        .then(response => {
            const updatedArticles = articles.map(article => {
                if (article.id === articleId) {
                    return { ...article, is_favorited: true };
                }
                return article;
            });
            setArticles(updatedArticles);
        })
        .catch(error => {
            console.error('Error changing article favorite status:', error);
        });
    };

    const handleUnfavorite = (articleId) => {
        const token = localStorage.getItem('token');
        axios.post(`http://localhost:8000/api/articles/${articleId}/unfavorite`, {}, {
            headers: {
                'Authorization': `Token ${token}`
            }
        })
        .then(response => {
            const updatedArticles = articles.map(article => {
                if (article.id === articleId) {
                    return { ...article, is_favorited: false };
                }
                return article;
            });
            setArticles(updatedArticles);
        })
        .catch(error => {
            console.error('Error changing article favorite status:', error);
        });
    };

    const handleReadLater = (articleId) => {
        const token = localStorage.getItem('token');
        axios.post(`http://localhost:8000/api/articles/${articleId}/readlater`, {}, {
            headers: {
                'Authorization': `Token ${token}`
            }
        })
        .then(response => {
            const updatedArticles = articles.map(article => {
                if (article.id === articleId) {
                    return { ...article, is_read_later: true };
                }
                return article;
            });
            setArticles(updatedArticles);
        })
        .catch(error => {
            console.error('Error changing article read later status:', error);
        });
    };

    const handleUnreadLater = (articleId) => {
        const token = localStorage.getItem('token');
        axios.post(`http://localhost:8000/api/articles/${articleId}/unreadlater`, {}, {
            headers: {
                'Authorization': `Token ${token}`
            }
        })
        .then(response => {
            const updatedArticles = articles.map(article => {
                if (article.id === articleId) {
                    return { ...article, is_read_later: false };
                }
                return article;
            });
            setArticles(updatedArticles);
        })
        .catch(error => {
            console.error('Error changing article read later status:', error);
        });
    };

    if (articles.length === 0 || sortedArticles.length === 0) {
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
            <br />
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
            {sortedArticles && sortedArticles.length > 0 ? (
                sortedArticles.map((article, index) => (
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
                                    <strong>Publisher:</strong> {' '}
                                    {article.publisher ? (
                                        <Link to={`/publisher/${encodeURIComponent(article.publisher.name)}`} className="link-no-underline">
                                            {article.publisher.name}
                                        </Link>
                                    ) : (
                                        'Unknown Publisher'
                                    )}
                                </div>
                                <div className="mb-2">
                                    <strong>Category:</strong>
                                    {article.category ? (
                                        <Link to={`/category/${encodeURIComponent(article.category.title)}`} className="link-no-underline">
                                            {article.category.title}
                                        </Link>
                                    ) : (
                                        'Uncategorized'
                                    )}
                                </div>
                                <div className="mb-2">
                                    <strong>Tags:</strong>{' '}
                                    {article.tags.map((tag, index) => (
                                      <React.Fragment key={tag.id}>
                                        <Link
                                          to={`/tag/${encodeURIComponent(tag.title)}`}
                                          className="badge bg-primary mr-3 link-no-underline"
                                        >
                                          {tag.title}
                                        </Link>
                                        {index !== article.tags.length - 1 && ' '}
                                      </React.Fragment>
                                    ))}
                                </div>
                                <a href={article.url} className="btn btn-outline-primary" style={{marginRight:'5px'}}>Source</a>
                                <a href="/" className="btn btn-primary">Read More</a>
                                { isAuthenticated() && (
                                    <div className="article-actions">
                                        { article.is_favorited ? (
                                            <i
                                                onClick={() => handleUnfavorite(article.id)}
                                                title="Unfavorite"
                                                className="bi bi-heart-fill me-2 fs-5 text-danger"
                                                style={{ cursor: 'pointer' }}
                                            ></i>
                                        ) : (
                                            <i
                                                onClick={() => handleFavorite(article.id)}
                                                title="Favorite"
                                                className="bi bi-heart me-2 fs-5"
                                                style={{ cursor: 'pointer' }}
                                            ></i>
                                        )}
                                        { article.is_read_later ? (
                                            <i
                                                onClick={() => handleUnreadLater(article.id)}
                                                title="Remove from Read Later"
                                                className="bi bi-clock-fill me-2 fs-5 text-danger"
                                                style={{ cursor: 'pointer' }}
                                            ></i>
                                        ) : (
                                            <i
                                                onClick={() => handleReadLater(article.id)}
                                                title="Read Later"
                                                className="bi bi-clock me-2 fs-5"
                                                style={{ cursor: 'pointer' }}
                                            ></i>
                                        )}
                                    </div>
                                )}
                            </div>
                        </div>
                    </div>
                ))
            ) : (
                <p>Loading articles...</p>
            )}
        </div>
    );
}

export default ArticleFeed;