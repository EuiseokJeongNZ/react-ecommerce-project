import React, { useEffect, useState } from 'react';
import { BsGeoAlt, BsPlusCircle } from 'react-icons/bs';
import api from '../api/axios';
import useDocTitle from '../hooks/useDocTitle';
import SectionsHead from '../components/common/SectionsHead';
import EmptyView from '../components/common/EmptyView';
import Services from '../components/common/Services';

const Addresses = () => {
  useDocTitle('Saved Addresses');

  const [addresses, setAddresses] = useState([]);
  const [editingId, setEditingId] = useState(null);

  const [formData, setFormData] = useState({
    recipient: '',
    phone: '',
    zip: '',
    addr1: '',
    addr2: '',
    is_default: false,
  });

  const fetchAddresses = async () => {
    try {
      const res = await api.get('/api/address/', {
        withCredentials: true,
      });
      setAddresses(res.data.addresses);
    } catch (err) {
      console.log(err.response?.data || err);
    }
  };

  useEffect(() => {
    fetchAddresses();
  }, []);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;

    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value,
    });
  };

  const resetForm = () => {
    setFormData({
      recipient: '',
      phone: '',
      zip: '',
      addr1: '',
      addr2: '',
      is_default: false,
    });
    setEditingId(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      if (editingId) {
        await api.put(`/api/address/${editingId}/`, formData, {
          withCredentials: true,
        });
      } else {
        await api.post('/api/address/', formData, {
          withCredentials: true,
        });
      }

      resetForm();
      fetchAddresses();
    } catch (err) {
      console.log(err.response?.data || err);
    }
  };

  const handleEdit = (address) => {
    setEditingId(address.id);
    setFormData({
      recipient: address.recipient,
      phone: address.phone,
      zip: address.zip,
      addr1: address.addr1,
      addr2: address.addr2,
      is_default: address.is_default,
    });

    window.scrollTo({
      top: 0,
      behavior: 'smooth',
    });
  };

  const handleDelete = async (id) => {
    try {
      await api.delete(`/api/address/${id}/`, {
        withCredentials: true,
      });
      fetchAddresses();

      if (editingId === id) {
        resetForm();
      }
    } catch (err) {
      console.log(err.response?.data || err);
    }
  };

  return (
    <>
      <section id="addresses" className="section">
        <div className="container">
          <SectionsHead heading="Saved Addresses" />

          <div className="wrapper addresses_wrapper">
            <div className="addresses_left_col">
              <div className="addresses_form_card">
                <div className="addresses_card_head">
                  <h3>{editingId ? 'Edit Address' : 'Add New Address'}</h3>
                  <p>Manage your shipping details for faster checkout.</p>
                </div>

                <form onSubmit={handleSubmit} className="addresses_form">
                  <div className="input_box">
                    <input
                      type="text"
                      name="recipient"
                      className="input_field"
                      value={formData.recipient}
                      onChange={handleChange}
                      required
                    />
                    <label className="input_label">Recipient</label>
                  </div>

                  <div className="input_box">
                    <input
                      type="text"
                      name="phone"
                      className="input_field"
                      value={formData.phone}
                      onChange={handleChange}
                      required
                    />
                    <label className="input_label">Phone</label>
                  </div>

                  <div className="input_box">
                    <input
                      type="text"
                      name="zip"
                      className="input_field"
                      value={formData.zip}
                      onChange={handleChange}
                      required
                    />
                    <label className="input_label">Zip Code</label>
                  </div>

                  <div className="input_box">
                    <input
                      type="text"
                      name="addr1"
                      className="input_field"
                      value={formData.addr1}
                      onChange={handleChange}
                      required
                    />
                    <label className="input_label">Address Line 1</label>
                  </div>

                  <div className="input_box">
                    <input
                      type="text"
                      name="addr2"
                      className="input_field"
                      value={formData.addr2}
                      onChange={handleChange}
                    />
                    <label className="input_label">Address Line 2</label>
                  </div>

                  <label className="default_check">
                    <input
                      type="checkbox"
                      name="is_default"
                      checked={formData.is_default}
                      onChange={handleChange}
                    />
                    <span>Set as default address</span>
                  </label>

                  <div className="addresses_form_actions">
                    <button type="submit" className="btn">
                      {editingId ? 'Update Address' : 'Add Address'}
                    </button>

                    {editingId && (
                      <button
                        type="button"
                        className="addresses_cancel_btn"
                        onClick={resetForm}
                      >
                        Cancel
                      </button>
                    )}
                  </div>
                </form>
              </div>
            </div>

            <div className="addresses_right_col">
              {addresses.length === 0 ? (
                <div className="addresses_empty">
                  <EmptyView
                    icon={<BsGeoAlt />}
                    msg="No Saved Addresses"
                  />
                </div>
              ) : (
                <div className="addresses_list">
                  {addresses.map((address) => (
                    <div className="address_card" key={address.id}>
                      <div className="address_card_top">
                        <div>
                          <h4>{address.recipient}</h4>
                          <p>{address.phone}</p>
                        </div>

                        {address.is_default && (
                          <span className="address_badge">Default</span>
                        )}
                      </div>

                      <div className="separator"></div>

                      <div className="address_card_body">
                        <p>{address.addr1}</p>
                        {address.addr2 && <p>{address.addr2}</p>}
                        <p>{address.zip}</p>
                      </div>

                      <div className="address_card_actions">
                        <button
                          type="button"
                          className="btn"
                          onClick={() => handleEdit(address)}
                        >
                          Edit
                        </button>

                        <button
                          type="button"
                          className="address_delete_btn"
                          onClick={() => handleDelete(address.id)}
                        >
                          Delete
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              )}

              {!editingId && addresses.length > 0 && (
                <div className="addresses_hint">
                  <BsPlusCircle />
                  <span>You can add multiple delivery addresses and choose one as default.</span>
                </div>
              )}
            </div>
          </div>
        </div>
      </section>

      <Services />
    </>
  );
};

export default Addresses;