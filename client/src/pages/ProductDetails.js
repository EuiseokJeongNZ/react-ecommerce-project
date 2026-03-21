// ProductDetails.js
import React, { useContext, useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import { IoMdStar, IoMdCheckmark } from 'react-icons/io';
import { calculateDiscount, displayMoney } from '../helpers/utils';
import useDocTitle from '../hooks/useDocTitle';
import useActive from '../hooks/useActive';
import cartContext from '../contexts/cart/cartContext';
import filtersContext from '../contexts/filters/filtersContext';
import SectionsHead from '../components/common/SectionsHead';
import RelatedSlider from '../components/sliders/RelatedSlider';
import ProductSummary from '../components/product/ProductSummary';
import Services from '../components/common/Services';

const ProductDetails = () => {
  useDocTitle('Product Details');

  const { addItem } = useContext(cartContext);
  const { products, allProducts, loading, error } = useContext(filtersContext);
  const { handleActive, activeClass } = useActive(0);

  const params = useParams();
  const id = params.id ?? params.productId;

  const source = products && products.length ? products : allProducts || [];

  const product = id
    ? source.find((item) => String(item.id) === String(id)) || null
    : null;

  const [previewImg, setPreviewImg] = useState('');

  useEffect(() => {
    if (!product) return;
    setPreviewImg(product.images?.[0] || '');
    handleActive(0);
  }, [product?.id]);

  const handleAddItem = () => {
    if (!product) return;
    addItem(product);
  };

  const handlePreviewImg = (i) => {
    if (!product) return;
    setPreviewImg(product.images[i]);
    handleActive(i);
  };

  if (loading) {
    return (
      <div className="section">
        <div className="container">Loading...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="section">
        <div className="container">{error}</div>
      </div>
    );
  }

  if (!id) {
    return (
      <div className="section">
        <div className="container">Invalid product URL (missing id)</div>
      </div>
    );
  }

  if (!product) {
    return (
      <div className="section">
        <div className="container">Product not found</div>
      </div>
    );
  }

  const {
    images = [],
    title,
    info,
    category,
    finalPrice,
    originalPrice,
    ratings,
    rateCount,
  } = product;

  const safeOriginal = originalPrice ?? finalPrice;
  const discountedPrice = safeOriginal - finalPrice;

  const newPrice = displayMoney(finalPrice);
  const oldPrice = displayMoney(safeOriginal);
  const savedPrice = displayMoney(discountedPrice);
  const savedDiscount = safeOriginal
    ? calculateDiscount(discountedPrice, safeOriginal)
    : 0;

  return (
    <>
      <section id="product_details" className="section">
        <div className="container">
          <div className="wrapper prod_details_wrapper">
            <div className="prod_details_left_col">
              <div className="prod_details_tabs">
                {images.map((img, i) => (
                  <div
                    key={i}
                    className={`tabs_item ${activeClass(i)}`}
                    onClick={() => handlePreviewImg(i)}
                  >
                    <img src={img} alt="product-img" />
                  </div>
                ))}
              </div>

              <figure className="prod_details_img">
                <img src={previewImg || images[0]} alt="product-img" />
              </figure>
            </div>

            <div className="prod_details_right_col">
              <h1 className="prod_details_title">{title}</h1>
              <h4 className="prod_details_info">{info}</h4>

              <div className="prod_details_ratings">
                <span className="rating_star">
                  {[...Array(rateCount || 0)].map((_, i) => (
                    <IoMdStar key={i} />
                  ))}
                </span>
                <span>|</span>
                <Link to="*">{ratings} Ratings</Link>
              </div>

              <div className="separator"></div>

              <div className="prod_details_price">
                <div className="price_box">
                  <h2 className="price">
                    {newPrice} &nbsp;
                    <small className="del_price">
                      <del>{oldPrice}</del>
                    </small>
                  </h2>
                  <p className="saved_price">
                    You save: {savedPrice} ({savedDiscount}%)
                  </p>
                  <span className="tax_txt">(Inclusive of all taxes)</span>
                </div>

                <div className="badge">
                  <span>
                    <IoMdCheckmark /> In Stock
                  </span>
                </div>
              </div>

              <div className="separator"></div>

              <div className="prod_details_offers">
                <h4>Offers and Discounts</h4>
                <ul>
                  <li>No Cost EMI on Credit Card</li>
                  <li>Pay Later & Avail Cashback</li>
                </ul>
              </div>

              <div className="separator"></div>

              <div className="prod_details_buy_btn">
                <button type="button" className="btn" onClick={handleAddItem}>
                  Add to cart
                </button>
              </div>
            </div>
          </div>
        </div>
      </section>

      <ProductSummary {...product} />

      <section id="related_products" className="section">
        <div className="container">
          <SectionsHead heading="Related Products" />
          <RelatedSlider category={category} />
        </div>
      </section>

      <Services />
    </>
  );
};

export default ProductDetails;