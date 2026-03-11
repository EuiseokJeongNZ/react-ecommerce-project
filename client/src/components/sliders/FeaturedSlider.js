import React from 'react';
import { Link } from 'react-router-dom';
import { Swiper, SwiperSlide } from 'swiper/react';
import { EffectCoverflow, Pagination, A11y, Autoplay } from 'swiper';
import { displayMoney } from '../../helpers/utils';

import 'swiper/scss';
import 'swiper/scss/autoplay';
import 'swiper/scss/pagination';
import 'swiper/scss/effect-coverflow';

const FeaturedSlider = ({ products = [] }) => {
  const featuredProducts = Array.isArray(products)
    ? products.filter((item) => item.tag === 'featured-product')
    : [];

  // do not render swiper if there are no featured products
  if (featuredProducts.length === 0) {
    return null;
  }

  // enable loop only when there are enough slides
  const shouldLoop = featuredProducts.length > 1;

  return (
    <Swiper
      key={featuredProducts.length}
      modules={[EffectCoverflow, Pagination, A11y, Autoplay]}
      loop={shouldLoop}
      speed={400}
      spaceBetween={100}
      slidesPerView="auto"
      pagination={{ clickable: true }}
      effect="coverflow"
      centeredSlides={true}
      coverflowEffect={{
        rotate: 0,
        stretch: 0,
        depth: 70,
        modifier: 3,
        slideShadows: false,
      }}
      autoplay={
        shouldLoop
          ? {
              delay: 3500,
              disableOnInteraction: false,
            }
          : false
      }
      breakpoints={{
        768: { slidesPerView: 2, spaceBetween: 200 },
        992: { slidesPerView: 3, spaceBetween: 250 },
      }}
      className="featured_swiper"
    >
      {featuredProducts.map((item) => {
        const id = item?.id;
        const title = item?.title || 'Untitled Product';

        const finalPrice = Number(item?.finalPrice ?? item?.final_price ?? 0);
        const originalPrice = Number(item?.originalPrice ?? item?.original_price ?? 0);

        const images =
          Array.isArray(item?.images) && item.images.length > 0
            ? item.images
            : ['/images/placeholder.png'];

        const path = '/product-details/';

        const newPrice = displayMoney(finalPrice);
        const oldPrice = displayMoney(originalPrice);

        return (
          <SwiperSlide key={id} className="featured_slides">
            <div className="featured_title">{title}</div>

            <figure className="featured_img">
              <Link to={`${path}${id}`}>
                <img src={images[0]} alt={title} />
              </Link>
            </figure>

            <h2 className="products_price">
              {newPrice} &nbsp;
              <small>
                <del>{oldPrice}</del>
              </small>
            </h2>
          </SwiperSlide>
        );
      })}
    </Swiper>
  );
};

export default FeaturedSlider;