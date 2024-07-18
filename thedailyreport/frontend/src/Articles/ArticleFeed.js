/////////////////////
// IMPORTS SECTION //
/////////////////////
// JavaScript Libraries
import axios from 'axios';
// React Libraries
import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
// Style Sheets
import './ArticleFeed.css';


//////////////////////
// CODE/JSX SECTION //
//////////////////////
// Get User Authentication Status based on token
function isAuthenticated() {
  const token = localStorage.getItem('token');
  return token && token !== "";
}

// Article Feed View
function ArticleFeed({ endpoint, title, permission }) {

  // Article List
  const [articles, setArticles] = useState([]);
  const [sortedArticles, setSortedArticles] = useState([]);

  // Filter Options
  const [sortOption, setSortOption] = useState("");
  const [sortOrder, setSortOrder] = useState("asc");

  // Feed Pagination
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);
  const [totalPages, setTotalPages] = useState(1);

  // Get and Sort Articles
  useEffect(() => {
    fetchAndSortArticles(endpoint, page);
  }, [endpoint, page]);
  useEffect(() => {
    sortArticles();
  }, [sortOption, sortOrder, articles]);
  const fetchAndSortArticles = (endpoint, page) => {
    const token = localStorage.getItem('token');
    const url = `${endpoint}?page=${page}&page_size=${pageSize}`;
    const config = (token && token !== "") || permission === "auth" ? {
      headers: { 'Authorization': `Token ${token}` }
    } : {};

    axios.get(url, config)
      .then(response => {
        setArticles(response.data.results);
        setSortedArticles(response.data.results);
        setTotalPages(Math.ceil(response.data.count / pageSize));
      })
      .catch(error => {
        console.error('Error fetching articles:', error);
      });
  };

  // Sort Articles based on Filter
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


  // Handle User Interactions - Favorite
  const handleFavorite = (articleId) => {
    const token = localStorage.getItem('token');
    axios.post(`http://localhost:8000/api/articles/${articleId}/favorite`, {}, {
      headers: { 'Authorization': `Token ${token}` }
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
      headers: { 'Authorization': `Token ${token}` }
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


  // Handle User Interactions - Read Later
  const handleReadLater = (articleId) => {
    const token = localStorage.getItem('token');
    axios.post(`http://localhost:8000/api/articles/${articleId}/readlater`, {}, {
      headers: { 'Authorization': `Token ${token}` }
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
      headers: { 'Authorization': `Token ${token}` }
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

  // JSX Section
  // Handle Empty Article List Case
  if (articles.length === 0 || sortedArticles.length === 0) {
    return (
      <>
        <h2 style={{ margin: '30px' }}>{title}</h2>
        <p style={{ margin: '30px' }}>There is nothing to show here!</p>
      </>
    );
  }
  // Handle Article List View
  return (
    <div id="news-feed" className="container">

      {/* Display Feed Title*/}
      <h2>{title}</h2>
      <br />

      {/* Display Filtering Options*/}
      <div className="sort-options mb-4">
        <div className="row">

          {/* Display Select Options*/}
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

          {/* Display Ascending / Descending Filter Options*/}
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

      {/* Display News Articles*/}
      {sortedArticles && sortedArticles.length > 0 ? (
        sortedArticles.map((article, index) => (
          <div key={index} className="article row mb-3">

            {/* Media Preview */}
            <div className="col-md-4 d-flex align-items-center justify-content-center">
              {article.media_preview && <img src={article.media_preview.url} className="img-fluid" alt="Article Media Preview" />}
            </div>

            <div className="col-md-8">
              <div className="card-body">

                {/* Title */}
                <h3 className="card-title">{article.title}</h3>

                {/* Summary */}
                <p className="card-text">{article.provided_summary}</p>

                {/* Publish Date */}
                <p className="card-text"><small className="text-muted">Published: {new Date(article.publish_date).toLocaleString('en-US', {
                  year: 'numeric', month: '2-digit', day: '2-digit',
                  hour: '2-digit', minute: '2-digit',
                })}</small></p>

                {/* Publisher */}
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

                {/* Category */}
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

                {/* Tags */}
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

                <a href={article.url} className="btn btn-outline-primary" style={{ marginRight: '5px' }}>Source</a>
                <a href={`/articles/${article.id}`} className="btn btn-primary">Read More</a>

                {/* User Interaction Widgets */}
                {isAuthenticated() && (
                  <div className="article-actions">
                    {article.is_favorited ? (
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
                    {article.is_read_later ? (
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

      {/* Article Pagination */}
      <div className="pagination">
          <ul className="pagination justify-content-center">

            <li className={`page-item ${page === 1 ? 'disabled' : ''}`}>
              <button className="page-link" onClick={() => setPage(page => Math.max(page - 1, 1))} disabled={page === 1}>
                Previous
              </button>
            </li>
            <li className="page-item">
              <span className="page-link">{page} of {totalPages}</span>
            </li>
            <li className={`page-item ${page === totalPages ? 'disabled' : ''}`}>
              <button className="page-link" onClick={() => setPage(page => Math.min(page + 1, totalPages))} disabled={page === totalPages}>
                Next
              </button>
            </li>

          </ul>
      </div>

    </div>
  );
}

export default ArticleFeed;
