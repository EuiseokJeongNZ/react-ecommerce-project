import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { IoMdStar } from "react-icons/io";
import axios from "../api/axios";

const MyReviews = () => {
    const [reviews, setReviews] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    const [editingReviewId, setEditingReviewId] = useState(null);
    const [editRating, setEditRating] = useState(5);
    const [hoverRating, setHoverRating] = useState(0);
    const [editContent, setEditContent] = useState("");

    useEffect(() => {
        fetchMyReviews();
    }, []);

    const fetchMyReviews = async () => {
        try {
            setLoading(true);
            setError("");

            const response = await axios.get("/api/reviews/my/");
            setReviews(response.data.reviews || []);
        } catch (err) {
            console.error("Failed to fetch my reviews:", err);
            setError("Failed to load your reviews.");
        } finally {
            setLoading(false);
        }
    };

    const handleDeleteReview = async (reviewId) => {
        const isConfirmed = window.confirm(
            "Are you sure you want to delete this review?"
        );

        if (!isConfirmed) return;

        try {
            await axios.delete(`/api/reviews/${reviewId}/delete/`);

            setReviews((prevReviews) =>
                prevReviews.filter((review) => review.id !== reviewId)
            );
        } catch (err) {
            console.error("Failed to delete review:", err);
            alert("Failed to delete review.");
        }
    };

    const handleStartEdit = (review) => {
        setEditingReviewId(review.id);
        setEditRating(review.rating);
        setHoverRating(0);
        setEditContent(review.content);
    };

    const handleCancelEdit = () => {
        setEditingReviewId(null);
        setEditRating(5);
        setHoverRating(0);
        setEditContent("");
    };

    const handleSaveEdit = async (reviewId) => {
        try {
            const response = await axios.put(`/api/reviews/${reviewId}/update/`, {
                rating: editRating,
                content: editContent,
            });

            const updatedReview = response.data.review;

            setReviews((prevReviews) =>
                prevReviews.map((review) =>
                    review.id === reviewId
                        ? {
                              ...review,
                              rating: updatedReview.rating,
                              content: updatedReview.content,
                              updated_at: updatedReview.updated_at,
                          }
                        : review
                )
            );

            handleCancelEdit();
        } catch (err) {
            console.error("Failed to update review:", err);
            alert("Failed to update review.");
        }
    };

    const formatDateTime = (dateString) => {
        if (!dateString) return "";

        return new Date(dateString).toLocaleString("en-NZ", {
            day: "2-digit",
            month: "short",
            year: "numeric",
            hour: "2-digit",
            minute: "2-digit",
            hour12: false,
        });
    };

    if (loading) {
        return (
            <section id="my_reviews">
                <div className="container">
                    <h2 className="section_title">My Reviews</h2>
                    <div className="reviews_empty">
                        <p>Loading...</p>
                    </div>
                </div>
            </section>
        );
    }

    if (error) {
        return (
            <section id="my_reviews">
                <div className="container">
                    <h2 className="section_title">My Reviews</h2>
                    <div className="reviews_empty">
                        <p>{error}</p>
                    </div>
                </div>
            </section>
        );
    }

    return (
        <section id="my_reviews">
            <div className="container">
                <h2 className="section_title">My Reviews</h2>

                {reviews.length === 0 ? (
                    <div className="reviews_empty">
                        <p>You have not written any reviews yet.</p>
                    </div>
                ) : (
                    <div className="reviews_list">
                        {reviews.map((review) => (
                            <div className="review_card" key={review.id}>
                                <div className="review_card_top">
                                    <div className="review_product">
                                        <img
                                            src={review.product_image}
                                            alt={review.product_title}
                                            className="review_product_image"
                                        />

                                        <div>
                                            <h4>
                                                <Link to={`/product-details/${review.product_id}`}>
                                                    {review.product_title}
                                                </Link>
                                            </h4>

                                            {editingReviewId === review.id ? (
                                                <p>Editing review...</p>
                                            ) : (
                                                <div className="review_meta">
                                                    <span className="review_stars">
                                                        {[...Array(review.rating || 0)].map((_, i) => (
                                                            <IoMdStar
                                                                key={i}
                                                                className="star active"
                                                            />
                                                        ))}
                                                    </span>

                                                    <span>|</span>

                                                    <p>{formatDateTime(review.created_at)}</p>
                                                </div>
                                            )}
                                        </div>
                                    </div>
                                </div>

                                <div className="review_card_bottom">
                                    {editingReviewId === review.id ? (
                                        <div className="review_edit_form">
                                            <label>Rating</label>

                                            <div className="review_star_input">
                                                {[1, 2, 3, 4, 5].map((star) => (
                                                    <IoMdStar
                                                        key={star}
                                                        className={
                                                            star <= (hoverRating || editRating)
                                                                ? "star active"
                                                                : "star"
                                                        }
                                                        onMouseEnter={() => setHoverRating(star)}
                                                        onMouseLeave={() => setHoverRating(0)}
                                                        onClick={() => setEditRating(star)}
                                                    />
                                                ))}
                                            </div>

                                            <label>Review</label>

                                            <textarea
                                                value={editContent}
                                                onChange={(e) =>
                                                    setEditContent(e.target.value)
                                                }
                                                rows="4"
                                            />

                                            <div className="review_actions">
                                                <button
                                                    className="btn"
                                                    onClick={() => handleSaveEdit(review.id)}
                                                >
                                                    Save
                                                </button>

                                                <button
                                                    className="btn"
                                                    onClick={handleCancelEdit}
                                                >
                                                    Cancel
                                                </button>
                                            </div>
                                        </div>
                                    ) : (
                                        <>
                                            <p className="review_text">{review.content}</p>

                                            <div className="review_actions">
                                                <button
                                                    className="btn"
                                                    onClick={() => handleStartEdit(review)}
                                                >
                                                    Edit
                                                </button>

                                                <button
                                                    className="btn"
                                                    onClick={() =>
                                                        handleDeleteReview(review.id)
                                                    }
                                                >
                                                    Delete
                                                </button>
                                            </div>
                                        </>
                                    )}
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </section>
    );
};

export default MyReviews;