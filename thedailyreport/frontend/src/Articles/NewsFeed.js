/////////////////////
// IMPORTS SECTION //
/////////////////////
// React Libraries
import React from "react";
import {useParams} from "react-router-dom";
// Project Libraries
import ArticleFeed from "./ArticleFeed";

//////////////////////
// CODE/JSX SECTION //
//////////////////////
// All News Feed - Based on all articles data
function NewsFeed() {
    return <ArticleFeed endpoint="http://localhost:8000/api/articles_all/" title="Discover Recent Articles:" permission="any"/>;
}

// Following News Feed - Based on all articles from the user's followed publisher list
function FollowingFeed() {
    return <ArticleFeed endpoint="http://localhost:8000/api/articles_following/" title="From your Favourite News Sources:" permission="auth" />;
}

// Favorite News Feed - Based on all articles from the user's favorite list
function FavoriteFeed() {
    return <ArticleFeed endpoint="http://localhost:8000/api/articles_favorite/" title="From your Favorite Articles List:" permission="auth" />;
}

// Read Later News Feed - Based on all articles from the user's read later list
function ReadLaterFeed() {
    return <ArticleFeed endpoint="http://localhost:8000/api/articles_read_later/" title="From your Read Later List:" permission="auth" />;
}

// Category News Feed - Based on all articles under the Category given by the title parameter
function CategoryFeed() {
    const { title } = useParams();
    return <ArticleFeed endpoint={`http://localhost:8000/api/articles_category/${title}`} title={`Articles from ${title} Category:`} permission="any" />;
}

// Tag News Feed - Based on all articles under the Tag given by the title parameter
function TagFeed() {
    const { title } = useParams();
    return <ArticleFeed endpoint={`http://localhost:8000/api/articles_tag/${title}`} title={`Articles tagged with ${title}:`} permission="any" />;
}

// Recommendation System News Feed - Based on all articles recommended to the user
// Collaborative Filtering - based on what similar users like
function CollaborativeFilteringFeed() {
    return <ArticleFeed endpoint={`http://localhost:8000/api/collaborative_filter_articles/`} title="Liked by users similar to you:" permission="auth" />;
}

// Content Filtering - based on previosuly liked categories / tags
function ContentFilteringFeed() {
    return <ArticleFeed endpoint={`http://localhost:8000/api/content_filter_articles/`} title="Based on what you liked:" permission="auth" />;
}

export {NewsFeed, FollowingFeed, FavoriteFeed, ReadLaterFeed, CategoryFeed, TagFeed, CollaborativeFilteringFeed, ContentFilteringFeed};
