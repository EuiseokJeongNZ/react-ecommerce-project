import React, { useContext, useMemo } from 'react';
import filtersContext from '../../contexts/filters/filtersContext';
import ProductCard from '../product/ProductCard';

const RelatedSlider = ({ category }) => {
  const { products } = useContext(filtersContext);

  const related = useMemo(() => {
    if (!category) return [];
    return products.filter(
      (p) => (p.category || '').toLowerCase() === category.toLowerCase()
    );
  }, [products, category]);

  if (!related.length) return null;

  return (
    <div className="wrapper products_wrapper">
      {related.map((item) => (
        <ProductCard key={item.id} {...item} />
      ))}
    </div>
  );
};

export default RelatedSlider;