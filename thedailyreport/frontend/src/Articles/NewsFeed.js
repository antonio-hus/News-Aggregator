import React, { useState, useEffect } from "react";
import ArticleFeed from "./ArticleFeed";
import {useParams} from "react-router-dom";

function NewsFeed() {
    return <ArticleFeed endpoint="http://localhost:8000/api/articles_all/" title="Discover Recent Articles:" permission="any"/>;
}

function FollowingFeed() {
    return <ArticleFeed endpoint="http://localhost:8000/api/articles_following/" title="From your Favourite News Sources:" permission="auth" />;
}

function FavoriteFeed() {
    return <ArticleFeed endpoint="http://localhost:8000/api/articles_favorite/" title="From your Favorite Articles List:" permission="auth" />;
}

function ReadLaterFeed() {
    return <ArticleFeed endpoint="http://localhost:8000/api/articles_read_later/" title="From your Read Later List:" permission="auth" />;
}

function CategoryFeed() {
    const { title } = useParams();
    return <ArticleFeed endpoint={`http://localhost:8000/api/articles_category/${title}`} title={`Articles from ${title} Category:`} permission="any" />;
}

function TagFeed() {
    const { title } = useParams();
    return <ArticleFeed endpoint={`http://localhost:8000/api/articles_tag/${title}`} title={`Articles tagged with ${title}:`} permission="any" />;
}

export {NewsFeed, FollowingFeed, FavoriteFeed, ReadLaterFeed, CategoryFeed, TagFeed};
