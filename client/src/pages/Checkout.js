import React, { useEffect, useState, useContext } from 'react';
import { BsGeoAlt } from 'react-icons/bs';
import api from '../api/axios';
import useDocTitle from '../hooks/useDocTitle';
import SectionsHead from '../components/common/SectionsHead';
import EmptyView from '../components/common/EmptyView';
import Services from '../components/common/Services';
import cartContext from '../contexts/cart/cartContext';

const Checkout = () => {
  useDocTitle('Checkout');

  const { cartItems, clearCart } = useContext(cartContext);
  const [addresses, setAddresses] = useState([]);
  const [selectedAddressId, setSelectedAddressId] = useState(null);

  const fetchAddresses = async () => {
    try {
      const res = await api.get('/api/address/');
      setAddresses(res.data.addresses);

      const defaultAddress = res.data.addresses.find((item) => item.is_default);

      if (defaultAddress) {
        setSelectedAddressId(defaultAddress.id);
      }
    } catch (err) {
      console.log(err.response?.data || err);
    }
  };

  useEffect(() => {
    fetchAddresses();
  }, []);

  const subtotal = cartItems.reduce((acc, item) => {
    return acc + item.finalPrice * item.quantity;
  }, 0);

    const shippingFee = subtotal >= 50 ? 0 : 7;
    const total = subtotal + shippingFee;

    const handlePlaceOrder = async () => {
        if (!selectedAddressId || cartItems.length === 0) return;

        try {
            const payload = {
            address_id: selectedAddressId,
            items: cartItems.map((item) => ({
                product_id: item.id,
                quantity: item.quantity,
            })),
            };

            await api.post('/api/orders/', payload, {
            withCredentials: true,
            });

            clearCart();
            window.location.href = '/orders';
        } catch (err) {
            console.log(err.response?.data || err);
            alert(err.response?.data?.message || 'Failed to place order');
        }
    };

  return (
    <>
      <section id="checkout" className="section">
        <div className="container">
          <SectionsHead heading="Checkout" />

          <div className="wrapper checkout_wrapper">
            <div className="checkout_left_col">
              <div className="checkout_card">
                <div className="checkout_card_head">
                  <h3>Select Delivery Address</h3>
                  <p>Choose where you want your order delivered.</p>
                </div>

                {addresses.length === 0 ? (
                  <div className="checkout_empty">
                    <EmptyView icon={<BsGeoAlt />} msg="No Saved Addresses" />
                  </div>
                ) : (
                  <div className="checkout_address_list">
                    {addresses.map((address) => (
                      <label className="checkout_address_item" key={address.id}>
                        <input
                          type="radio"
                          name="selectedAddress"
                          checked={selectedAddressId === address.id}
                          onChange={() => setSelectedAddressId(address.id)}
                        />

                        <div>
                          <h4>
                            {address.recipient}
                            {address.is_default && (
                              <span className="checkout_badge">Default</span>
                            )}
                          </h4>
                          <p>{address.phone}</p>
                          <p>{address.addr1}</p>
                          {address.addr2 && <p>{address.addr2}</p>}
                          <p>{address.zip}</p>
                        </div>
                      </label>
                    ))}
                  </div>
                )}
              </div>
            </div>

            <div className="checkout_right_col">
              <div className="checkout_card">
                <div className="checkout_card_head">
                  <h3>Order Summary</h3>
                  <p>{cartItems.length} items</p>
                </div>

                <div className="checkout_summary_list">
                  {cartItems.map((item) => (
                    <div className="checkout_summary_item" key={item.id}>
                      <div>
                        <h4>{item.title}</h4>
                        <p>Qty: {item.quantity}</p>
                      </div>

                      <strong>NZ${item.finalPrice * item.quantity}</strong>
                    </div>
                  ))}
                </div>

                <div className="separator"></div>

                <div className="checkout_total_box">
                  <div>
                    <span>Subtotal</span>
                    <strong>NZ${subtotal}</strong>
                  </div>

                  <div>
                    <span>Delivery</span>
                    <strong>Free</strong>
                  </div>

                  <div className="checkout_total_final">
                    <span>Total</span>
                    <strong>NZ${total}</strong>
                  </div>
                </div>
                <button
                    type="button"
                    className="btn checkout_btn"
                    disabled={!selectedAddressId || cartItems.length === 0}
                    onClick={handlePlaceOrder}
                    >
                    Place Order
                </button>
              </div>
            </div>
          </div>
        </div>
      </section>

      <Services />
    </>
  );
};

export default Checkout;
