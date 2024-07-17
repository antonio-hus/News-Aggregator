import React, { useState, useEffect } from "react";
import axios from 'axios';
import NotFound from "../ErrorScreens/404Page";
import {Link, useParams} from "react-router-dom";

function ArticleScreen() {
    const { articleId } = useParams();
    const [article, setArticle] = useState(null);

    useEffect(() => {
        fetchArticle(articleId);
    }, [articleId]);

    const fetchArticle = (id) => {
        const token = localStorage.getItem('token');
        const url = `http://localhost:8000/api/articles/${id}/`;

        axios.get(url, {
            headers: token ? { 'Authorization': `Token ${token}` } : {}
        })
        .then(response => {
            setArticle(response.data);
        })
        .catch(error => {
            console.error('Error fetching article:', error);
        });
    };

    const handleFavorite = (articleId) => {
        const token = localStorage.getItem('token');
        axios.post(`http://localhost:8000/api/articles/${articleId}/favorite`, {}, {
            headers: { 'Authorization': `Token ${token}` }
        })
        .then(response => {
            setArticle(prevArticle => ({ ...prevArticle, is_favorited: true }));
        })
        .catch(error => {
            console.error('Error changing article favorite status:', error);
        });
    };

    const handleUnfavorite = (articleId) => {
        const token = localStorage.getItem('token');
        axios.post(`http://localhost:8000/api/articles/${articleId}/unfavorite`, {}, {
            headers: { 'Authorization': `Token ${token}` }
        })
        .then(response => {
            setArticle(prevArticle => ({ ...prevArticle, is_favorited: false }));
        })
        .catch(error => {
            console.error('Error changing article favorite status:', error);
        });
    };

    const handleReadLater = (articleId) => {
        const token = localStorage.getItem('token');
        axios.post(`http://localhost:8000/api/articles/${articleId}/readlater`, {}, {
            headers: { 'Authorization': `Token ${token}` }
        })
        .then(response => {
            setArticle(prevArticle => ({ ...prevArticle, is_read_later: true }));
        })
        .catch(error => {
            console.error('Error changing article read later status:', error);
        });
    };

    const handleUnreadLater = (articleId) => {
        const token = localStorage.getItem('token');
        axios.post(`http://localhost:8000/api/articles/${articleId}/unreadlater`, {}, {
            headers: { 'Authorization': `Token ${token}` }
        })
        .then(response => {
            setArticle(prevArticle => ({ ...prevArticle, is_read_later: false }));
        })
        .catch(error => {
            console.error('Error changing article read later status:', error);
        });
    };

    if (!article) {
        return <NotFound message="Article not found!"/>;
    }

    const isAuthenticated = () => {
        const token = localStorage.getItem('token');
        return token !== null && token !== '';
    };

    return (
        <div className="container mt-4">
            <div className="card">
                <div className="card-body">
                    <img src={article.media_preview.url} alt="Article Media Preview" className="img-fluid card-img-top" />
                    <h2 className="card-title">{article.title}</h2>
                    <p className="card-text"><strong>Publish Date:</strong> {new Date(article.publish_date).toLocaleString()}</p>
                    <p className="card-text"><strong>Last Updated:</strong> {new Date(article.last_updated_date).toLocaleString()}</p>
                    <p className="card-text">
                        <strong>Category:</strong>
                        {article.category ? (
                            <Link to={`/category/${encodeURIComponent(article.category.title)}`} className="link-no-underline">
                                {article.category.title}
                            </Link>
                        ) : (
                            'Uncategorized'
                        )}
                    </p>
                    <p className="card-text">
                        <strong>Tags:</strong>
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
                    </p>
                    { isAuthenticated() && (
                        <div className="article-actions mb-3">
                            { article.is_favorited ? (
                                <i
                                    onClick={() => handleUnfavorite(article.id)}
                                    title="Unfavorite"
                                    className="bi bi-heart-fill me-2 fs-4 text-danger"
                                    style={{ cursor: 'pointer' }}
                                ></i>
                            ) : (
                                <i
                                    onClick={() => handleFavorite(article.id)}
                                    title="Favorite"
                                    className="bi bi-heart me-2 fs-4"
                                    style={{ cursor: 'pointer' }}
                                ></i>
                            )}
                            { article.is_read_later ? (
                                <i
                                    onClick={() => handleUnreadLater(article.id)}
                                    title="Remove from Read Later"
                                    className="bi bi-clock-fill me-2 fs-4 text-danger"
                                    style={{ cursor: 'pointer' }}
                                ></i>
                            ) : (
                                <i
                                    onClick={() => handleReadLater(article.id)}
                                    title="Read Later"
                                    className="bi bi-clock me-2 fs-4"
                                    style={{ cursor: 'pointer' }}
                                ></i>
                            )}
                        </div>
                    )}
                    <br/>
                    <p className="card-text"><
                        strong>Publisher:</strong>
                        {' '}
                        {article.publisher ? (
                        <Link to={`/publisher/${encodeURIComponent(article.publisher.name)}`} className="link-no-underline">
                            {article.publisher.name}
                        </Link>
                        ) : (
                            'Unknown Publisher'
                        )}
                    </p>
                    <p className="card-text"><strong>Writer:</strong> {article.writer}</p>
                    <p className="card-text"><strong>Content:</strong>
                        <br/>
                        <span dangerouslySetInnerHTML={{ __html: article.content.replace(/\n/g, '<br style="display: block; margin: margin: 0.5em 0;" />') }} />
                    </p>
                    <a href={article.url} className="btn btn-primary mt-3" target="_blank" rel="noopener noreferrer">Read Original</a>
                </div>
            </div>
        </div>
    );
}

export default ArticleScreen;
