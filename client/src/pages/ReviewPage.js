import React, { useState, useContext, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { BsExclamationCircle } from 'react-icons/bs';
import filtersContext from '../contexts/filters/filtersContext';
import ProductReviews from '../components/product/ProductReviews';
import EmptyView from '../components/common/EmptyView';
import useDocTitle from '../hooks/useDocTitle';
import axios from '../api/axios';
import { IoMdStar } from "react-icons/io";

const ReviewPage = () => {
  useDocTitle('Reviews');

  const { productId } = useParams();

  const [rating, setRating] = useState(5);
  const [hoverRating, setHoverRating] = useState(0);
  const [content, setContent] = useState("");
  const [submitLoading, setSubmitLoading] = useState(false);
  const [submitError, setSubmitError] = useState("");
  

  const {
    products,
    loading,
    error,
    fetchProducts,
    reviews,
    reviewsLoading,
    reviewsError,
    reviewSortValue,
    setReviewSortedValue,
  } = useContext(filtersContext);

  const { fetchProductReviews } = useContext(filtersContext);

  useEffect(() => {
    if (!products.length) {
      fetchProducts();
    }
  }, []);

  useEffect(() => {
    if (productId) {
      fetchProductReviews(productId);
    }
  }, [productId]);

  const product =
    products.find((item) => String(item.id) === String(productId)) || null;

  const formatDate = (value) => {
    if (!value) return '';
    return new Date(value).toLocaleDateString();
  };

  const handleSubmitReview = async (e) => {
    e.preventDefault();

    try {
      setSubmitLoading(true);
      setSubmitError("");

      await axios.post(`/api/products/${productId}/reviews/create/`, {
        rating,
        content,
      });

      setRating(5);
      setContent("");

      fetchProductReviews(productId);
    } catch (err) {
      console.error("Failed to create review:", err);
      setSubmitError(
        err?.response?.data?.message || "Failed to submit review."
      );
    } finally {
      setSubmitLoading(false);
    }
  };

  if (loading && !products.length) {
    return (
      <section id="review_page" className="section">
        <div className="container">
          <p className="review_page_state">Loading product...</p>
        </div>
      </section>
    );
  }

  if (error && !products.length) {
    return (
      <section id="review_page" className="section">
        <div className="container">
          <p className="review_page_state">{error}</p>
        </div>
      </section>
    );
  }

  return (
    <section id="review_page" className="section">
      <div className="container">
        <div className="review_page_top">
          <div className="review_page_heading">
            <h2>
              {product ? `${product.title} Reviews` : 'Product Reviews'}
            </h2>
            <p>Sort reviews by rating</p>
          </div>

          <div className="review_page_sort">
            <select
              value={reviewSortValue}
              onChange={(e) => setReviewSortedValue(e.target.value)}
            >
              <option value="Highest Rating">Highest Rating</option>
              <option value="Lowest Rating">Lowest Rating</option>
            </select>
          </div>
        </div>

        {reviewsLoading ? (
          <p className="review_page_state">Loading reviews...</p>
        ) : reviewsError ? (
          <p className="review_page_state">{reviewsError}</p>
        ) : reviews.length ? (
          <ul className="review_page_list">
            {reviews.map((item) => (
              <ProductReviews
                key={item.id}
                name={item.name}
                date={formatDate(item.date)}
                review={item.review}
                rateCount={item.rateCount}
              />
            ))}
          </ul>
        ) : (
          <EmptyView
            icon={<BsExclamationCircle />}
            msg="No reviews found"
          />
        )}

        <div className="review_write_box">
          <h3>Write a Review</h3>

          <form onSubmit={handleSubmitReview} className="review_write_form">
            <div className="review_form_group">
              <label>Rating</label>
              <div className="review_star_input">
                {[1, 2, 3, 4, 5].map((star) => (
                  <IoMdStar
                    key={star}
                    className={
                      star <= (hoverRating || rating) ? "star active" : "star"
                    }
                    onMouseEnter={() => setHoverRating(star)}
                    onMouseLeave={() => setHoverRating(0)}
                    onClick={() => setRating(star)}
                  />
                ))}
              </div>
            </div>

            <div className="review_form_group">
              <label>Review</label>
              <textarea
                value={content}
                onChange={(e) => setContent(e.target.value)}
                rows="5"
                placeholder="Write your review here"
              />
            </div>

            {submitError ? (
              <p className="review_form_error">{submitError}</p>
            ) : null}

            <button className="btn" type="submit" disabled={submitLoading}>
              {submitLoading ? "Submitting..." : "Submit Review"}
            </button>
          </form>
        </div>
      </div>
    </section>
  );
};

export default ReviewPage;