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
      <section className="section">
        <div className="container">Loading product...</div>
      </section>
    );
  }

  if (error && !products.length) {
    return (
      <section className="section">
        <div className="container">{error}</div>
      </section>
    );
  }

  return (
    <section id="review_page" className="section">
      <div className="container">
        <div
          style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            marginBottom: '24px',
            gap: '16px',
            flexWrap: 'wrap',
          }}
        >
          <div>
            <h2 style={{ marginBottom: '8px' }}>
              {product ? `${product.title} Reviews` : 'Product Reviews'}
            </h2>
            <p style={{ margin: 0 }}>
              Sort reviews by rating
            </p>
          </div>

          <select
            value={reviewSortValue}
            onChange={(e) => setReviewSortedValue(e.target.value)}
          >
            <option value="Highest Rating">Highest Rating</option>
            <option value="Lowest Rating">Lowest Rating</option>
          </select>
        </div>

        {reviewsLoading ? (
          <p>Loading reviews...</p>
        ) : reviewsError ? (
          <p>{reviewsError}</p>
        ) : reviews.length ? (
          <ul style={{ padding: 0, margin: 0, listStyle: 'none' }}>
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