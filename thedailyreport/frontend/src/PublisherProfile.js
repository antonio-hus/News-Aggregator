import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';

const PublisherProfile = () => {
    const { name } = useParams();
    const [publisher, setPublisher] = useState(null);
    const [articles, setArticles] = useState([]);
    const [sortedArticles, setSortedArticles] = useState([]);
    const [sortOption, setSortOption] = useState("");
    const [sortOrder, setSortOrder] = useState("asc");

    useEffect(() => {
        axios.get(`http://localhost:8000/api/articles_publisher/${name}/`)
            .then(response => {
                setPublisher(response.data.publisher);
                setArticles(response.data.article_list);
                setSortedArticles(response.data.article_list);
            })
            .catch(error => {
                console.error('There was an error fetching the publisher data!', error);
            });
    }, [name]);

    useEffect(() => {
        sortArticles();
    }, [sortOption, sortOrder, articles]);

    const sortArticles = () => {
        let sorted = [...articles];

        if (sortOption === "title") {
            sorted.sort((a, b) => {
                if (a.title < b.title) return sortOrder === "asc" ? -1 : 1;
                if (a.title > b.title) return sortOrder === "asc" ? 1 : -1;
                return 0;
            });
        } else if (sortOption === "publish_date") {
            sorted.sort((a, b) => {
                if (new Date(a.publish_date) < new Date(b.publish_date)) return sortOrder === "asc" ? -1 : 1;
                if (new Date(a.publish_date) > new Date(b.publish_date)) return sortOrder === "asc" ? 1 : -1;
                return 0;
            });
        } else if (sortOption === "category") {
            sorted.sort((a, b) => {
                if (a.category.title < b.category.title) return sortOrder === "asc" ? -1 : 1;
                if (a.category.title > b.category.title) return sortOrder === "asc" ? 1 : -1;
                return 0;
            });
        }

        setSortedArticles(sorted);
    };

    if (!publisher) return <div>Loading...</div>;

    return (
        <>
            <div id="news-feed" className="container">
                <h4>Discover Recent Articles from {publisher.name}:</h4>
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
        </>
    );
};

export default PublisherProfile;