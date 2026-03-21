import React, { useContext } from 'react';
import { BsArrowClockwise } from 'react-icons/bs';
import HeroSlider from '../components/sliders/HeroSlider';
import FeaturedSlider from '../components/sliders/FeaturedSlider';
import SectionsHead from '../components/common/SectionsHead';
import TopProducts from '../components/product/TopProducts';
import Services from '../components/common/Services';
import filtersContext from "../contexts/filters/filtersContext";

const Home = () => {
  const { products, loading, error, fetchProducts } = useContext(filtersContext);

  if (loading) {
    return (
      <main>
        <section id="products" className="section">
          <div className="container">
            <div className="products_status_center">
              <p className="products_status_text">
                Loading products... The server may take a few seconds to wake up.
              </p>
            </div>
          </div>
        </section>
      </main>
    );
  }

  if (error) {
    return (
      <main>
        <section id="products" className="section">
          <div className="container">
            <div className="products_status_center">
              <p className="products_status_text">
                Failed to fetch products.
              </p>

              <button
                type="button"
                className="btn products_status_btn"
                onClick={fetchProducts}
              >
                <BsArrowClockwise />
                <span>Try to fetch again</span>
              </button>
            </div>
          </div>
        </section>
      </main>
    );
  }

  return (
    <main>
      <section id="hero">
        <HeroSlider products={products} />
      </section>

      <section id="featured" className="section">
        <div className="container">
          <SectionsHead heading="Featured Products" />
          <FeaturedSlider products={products} />
        </div>
      </section>

      <section id="products" className="section">
        <div className="container">
          <SectionsHead heading="Top Products" />
          <TopProducts
            products={products}
            loading={loading}
            error={error}
            onRetry={fetchProducts}
          />
        </div>
      </section>

      <Services />
    </main>
  );
};

export default Home;