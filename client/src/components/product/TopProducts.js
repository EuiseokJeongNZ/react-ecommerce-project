import React, { useState, useMemo, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { BsArrowRight } from 'react-icons/bs';
import useActive from '../../hooks/useActive';
// import productsData from '../../data/productsData'; // dummy datas from productsDat.js
import ProductCard from './ProductCard';


const TopProducts = ({ products = [] }) => {

    // const [products, setProducts] = useState(productsData);
    const [filteredProducts, setFilteredProducts] = useState(products);
    const { activeClass, handleActive } = useActive(0);

    // making a unique set of product's category
    // const productsCategory = [
    //     'All',
    //     ...new Set(productsData.map(item => item.category))
    // ];

    // handling product's filtering
    // const handleProducts = (category, i) => {
    //     if (category === 'All') {
    //         setProducts(productsData);
    //         handleActive(i);
    //         return;
    //     }

    //     const filteredProducts = productsData.filter(item => item.category === category);
    //     setProducts(filteredProducts);
    //     handleActive(i);
    // };

    React.useEffect(() => {
    setFilteredProducts(products);
    }, [products]);

    const productsCategory = useMemo(() => {
        return ['All', ...new Set(products.map((item) => item.category).filter(Boolean))];
    }, [products]);

    const handleProducts = (category, i) => {
        if (category === 'All') {
            setFilteredProducts(products);
            handleActive(i);
            return;
        }

        const filtered = products.filter((item) => item.category === category);
        setFilteredProducts(filtered);
        handleActive(i);
    };


    return (
        <>
            <div className="products_filter_tabs">
                <ul className="tabs">
                    {
                        productsCategory.map((item, i) => (
                            <li
                                key={i}
                                className={`tabs_item ${activeClass(i)}`}
                                onClick={() => handleProducts(item, i)}
                            >
                                {item}
                            </li>
                        ))
                    }
                </ul>
            </div>
            <div className="wrapper products_wrapper">
                {
                    filteredProducts.slice(0, 11).map((item) => (
                        <ProductCard
                        key={item.id}
                        id={item.id}
                        images={item.images || ["/images/placeholder.png"]}
                        title={item.title}
                        info={item.info}
                        category={item.category}
                        finalPrice={Number(item.finalPrice)}
                        originalPrice={Number(item.originalPrice ?? item.final_price)}
                        rateCount={Math.max(0, Math.min(5, Math.round(Number(item.rate_count ?? 5))))}
                        path="/product-details/"
                        />
                    ))
                }
                <div className="card products_card browse_card">
                    <Link to="/all-products">
                        Browse All <br /> Products <BsArrowRight />
                    </Link>
                </div>
            </div>
        </>
    );
};

export default TopProducts;