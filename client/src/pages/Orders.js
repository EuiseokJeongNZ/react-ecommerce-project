import React, { useEffect, useState } from 'react';
import { BsBagCheck, BsBoxSeam, BsTruck, BsXCircle } from 'react-icons/bs';
import api from '../api/axios';
import useDocTitle from '../hooks/useDocTitle';
import SectionsHead from '../components/common/SectionsHead';
import EmptyView from '../components/common/EmptyView';
import Services from '../components/common/Services';

const Orders = () => {
  useDocTitle('Orders');

  const [orders, setOrders] = useState([]);

  const fetchOrders = async () => {
    try {
      const res = await api.get('/api/orders/', {
        withCredentials: true,
      });
      setOrders(res.data.orders || []);
    } catch (err) {
      console.log(err.response?.data || err);
    }
  };

  useEffect(() => {
    fetchOrders();
  }, []);

  const getStatusIcon = (status) => {
    if (status === 'paid') return <BsBagCheck />;
    if (status === 'shipped') return <BsTruck />;
    if (status === 'cancelled') return <BsXCircle />;
    return <BsBoxSeam />;
  };

  return (
    <>
      <section id="orders" className="section">
        <div className="container">
          <SectionsHead heading="My Orders" />

          {orders.length === 0 ? (
            <div className="orders_empty">
              <EmptyView icon={<BsBoxSeam />} msg="No Orders Yet" />
            </div>
          ) : (
            <div className="orders_list">
              {orders.map((order) => (
                <div className="order_card" key={order.id}>
                  <div className="order_card_top">
                    <div>
                      <h4>{order.order_number}</h4>
                      <p>
                        Placed on {new Date(order.created_at).toLocaleDateString()}
                      </p>
                    </div>

                    <div className={`order_status ${order.status}`}>
                      <span className="order_status_icon">
                        {getStatusIcon(order.status)}
                      </span>
                      <span>{order.status}</span>
                    </div>
                  </div>

                  <div className="separator"></div>

                  <div className="order_items">
                    {order.items.map((item) => (
                      <div className="order_item" key={item.id}>
                        <div>
                          <h5>{item.title_snapshot}</h5>
                          <p>Qty: {item.quantity}</p>
                          <p>Unit Price: NZ${item.unit_price_snapshot}</p>
                        </div>

                        <strong>NZ${item.line_total}</strong>
                      </div>
                    ))}
                  </div>

                  <div className="separator"></div>

                  <div className="order_card_bottom">
                    <p>
                      Total <strong>NZ${order.total}</strong>
                    </p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </section>

      <Services />
    </>
  );
};

export default Orders;