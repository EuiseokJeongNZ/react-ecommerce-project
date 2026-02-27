import React, { useMemo } from 'react';
import reviewsData from '../../data/reviewsData';
import useActive from '../../hooks/useActive';
import ProductReviews from './ProductReviews';

const ProductSummary = (props) => {
  const { brand, title, info, category, flavor, weight, qty, serve } = props;
  const { active, handleActive, activeClass } = useActive('specs');

  // ✅ 빈 값은 자동으로 제거해서 "깔끔한 스펙 리스트" 만들기
  const specItems = useMemo(() => {
    const items = [
      { label: 'Brand', value: brand },
      { label: 'Name', value: title },
      { label: 'Type', value: category },
      { label: 'Flavor', value: flavor },
      { label: 'Weight', value: weight },
      { label: 'Qty', value: qty },
      { label: 'Serve', value: serve },
    ];

    return items.filter((x) => x.value != null && String(x.value).trim() !== '');
  }, [brand, title, category, flavor, weight, qty, serve]);

  const shortTitle = title?.trim() || 'This product';
  const shortInfo = info?.trim() || '';

  return (
    <section id="product_summary" className="section">
      <div className="container">
        {/* Tabs */}
        <div className="prod_summary_tabs">
          <ul className="tabs">
            <li
              className={`tabs_item ${activeClass('specs')}`}
              onClick={() => handleActive('specs')}
            >
              Specifications
            </li>
            <li
              className={`tabs_item ${activeClass('overview')}`}
              onClick={() => handleActive('overview')}
            >
              Overview
            </li>
            <li
              className={`tabs_item ${activeClass('reviews')}`}
              onClick={() => handleActive('reviews')}
            >
              Reviews
            </li>
          </ul>
        </div>

        {/* Content */}
        <div className="prod_summary_details">
          {active === 'specs' && (
            <div className="prod_specs">
              <ul>
                {specItems.map((item) => (
                  <li key={item.label}>
                    <span>{item.label}</span>
                    <span>{item.value}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {active === 'overview' && (
            <div className="prod_overview">
              <h3>
                <span>{shortTitle}</span>
                {shortInfo ? ` — ${shortInfo}` : '' }
              </h3>

              <ul>
                <li>High-quality protein to support muscle recovery</li>
                <li>Easy to mix and great for daily routines</li>
                <li>Suitable for workouts and balanced nutrition</li>
              </ul>

              <p>
                Add <b>{shortTitle}</b>
                {category ? ` (${category})` : ''} to your routine for consistent,
                convenient nutrition. Ideal for post-workout recovery or as a
                protein boost throughout the day.
              </p>
            </div>
          )}

          {active === 'reviews' && (
            <div className="prod_reviews">
              <ul>
                {reviewsData.map((item) => (
                  <ProductReviews key={item.id} {...item} />
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>
    </section>
  );
};

export default ProductSummary;