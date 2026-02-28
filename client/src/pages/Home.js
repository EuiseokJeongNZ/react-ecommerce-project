import React, { useContext } from 'react';
import HeroSlider from '../components/sliders/HeroSlider';
import FeaturedSlider from '../components/sliders/FeaturedSlider';
import SectionsHead from '../components/common/SectionsHead';
import TopProducts from '../components/product/TopProducts';
import Services from '../components/common/Services';
import filtersContext from "../contexts/filters/filtersContext";

const Home = () => {

  const { products } = useContext(filtersContext);

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
          <TopProducts products={products} />
        </div>
      </section>

      <Services />
    </main>
  );
};

export default Home;