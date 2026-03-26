import React, { useContext, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { BsExclamationCircle } from 'react-icons/bs';
import filtersContext from '../contexts/filters/filtersContext';
import ProductReviews from '../components/product/ProductReviews';
import EmptyView from '../components/common/EmptyView';
import useDocTitle from '../hooks/useDocTitle';

const ReviewPage = () => {
  useDocTitle('Reviews');

  const { productId } = useParams();

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
      </div>
    </section>
  );
};

export default ReviewPage;