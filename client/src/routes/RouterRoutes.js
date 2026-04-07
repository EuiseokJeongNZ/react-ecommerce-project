import React from 'react';
import { Routes, Route } from 'react-router';
import useScrollRestore from '../hooks/useScrollRestore';
import AllProducts from '../pages/AllProducts';
import Cart from '../pages/Cart';
import Home from '../pages/Home';
import ProductDetails from '../pages/ProductDetails';
import ErrorPage from '../pages/ErrorPage';
import Addresses from '../pages/Addresses';
import Profile from "../pages/Profile";
import Orders from '../pages/Orders';
import Checkout from  "../pages/Checkout";
import MyReviews from '../pages/MyReviews';
import ReviewPage from '../pages/ReviewPage';
import ProtectedRoute from './ProtectedRoute';

const RouterRoutes = () => {

    useScrollRestore();

    return (
        <>
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/cart" element={<Cart />} />
                <Route path="/all-products" element={<AllProducts />} />
                <Route path="/product-details/:productId" element={<ProductDetails />} />
                <Route path="/checkout" element={<Checkout />} />
                <Route path="/product-details/:productId/reviews" element={<ReviewPage />} />
                {/* <Route path="/addresses" element={<Addresses />} />
                <Route path="/profile" element={<Profile />} />
                <Route path="/orders" element={<Orders />} />
                <Route path="/my-reviews" element={<MyReviews />} /> */}
                <Route path="*" element={<ErrorPage />} />

                <Route
                path="/addresses"
                element={
                    <ProtectedRoute>
                    <Addresses />
                    </ProtectedRoute>
                }
                />

                <Route
                path="/profile"
                element={
                    <ProtectedRoute>
                    <Profile />
                    </ProtectedRoute>
                }
                />

                <Route
                path="/orders"
                element={
                    <ProtectedRoute>
                    <Orders />
                    </ProtectedRoute>
                }
                />

                <Route
                path="/my-reviews"
                element={
                    <ProtectedRoute>
                    <MyReviews />
                    </ProtectedRoute>
                }
                />
            </Routes>
        </>
    );
};

export default RouterRoutes;