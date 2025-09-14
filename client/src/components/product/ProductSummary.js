import React from 'react';
import reviewsData from '../../data/reviewsData';
import useActive from '../../hooks/useActive';
import ProductReviews from './ProductReviews';


const ProductSummary = (props) => {

    const { brand, title, info, category, flavor, weight, qty, serve } = props;

    const { active, handleActive, activeClass } = useActive('specs');


    return (
        <>
            <section id="product_summary" className="section">
                <div className="container">

                    {/*===== Product-Summary-Tabs =====*/}
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

                    {/*===== Product-Summary-Details =====*/}
                    <div className="prod_summary_details">
                        {
                            active === 'specs' ? (
                                <div className="prod_specs">
                                    <ul>
                                        <li>
                                            <span>Brand</span>
                                            <span>{brand}</span>
                                        </li>
                                        <li>
                                            <span>Name</span>
                                            <span>{title}</span>
                                        </li>
                                        <li>
                                            <span>Type</span>
                                            <span>{category}</span>
                                        </li>
                                        <li>
                                            <span>Flavor</span>
                                            <span>{flavor}</span>
                                        </li>
                                        {weight && (
                                        <li>
                                            <span>Weight</span>
                                            <span>{weight}</span>
                                        </li>
                                        )}
                                        {qty && (
                                        <li>
                                            <span>Qty</span>
                                            <span>{qty}</span>
                                        </li>
                                        )}
                                        {serve && (
                                        <li>
                                            <span>Serve</span>
                                            <span>{serve}</span>
                                        </li>
                                        )}

                                    </ul>
                                </div>
                            ) : active === 'overview' ? (
                                <div className="prod_overview">
                                    <h3>The <span>{title}</span> {info} provides with fabulous sound quality</h3>
                                    <ul>
                                        <li>High-quality protein for muscle growth</li>
                                        <li>Delicious and smooth mixability</li>
                                        <li>Supports faster recovery after workouts</li>
                                    </ul>
                                    <p>
                                    Buy the <b>{title} {info}</b> which fuels your body with high-quality nutrition
                                    for energy, muscle growth, and faster recovery. Enjoy the delicious taste and
                                    smooth mixability of this {category}, making it easy to add to your daily routine.
                                    It blends premium ingredients with essential nutrients for an unrivalled protein experience.
                                    </p>
                                </div>
                            ) : (
                                <div className="prod_reviews">
                                    <ul>
                                        {
                                            reviewsData.map(item => (
                                                <ProductReviews
                                                    key={item.id}
                                                    {...item}
                                                />
                                            ))
                                        }
                                    </ul>
                                </div>
                            )

                        }

                    </div>

                </div>
            </section>
        </>
    );
};

export default ProductSummary;