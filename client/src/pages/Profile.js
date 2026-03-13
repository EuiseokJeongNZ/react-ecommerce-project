import React, { useEffect, useState } from 'react';
import { BsPersonCircle, BsEnvelope, BsTelephone, BsShieldCheck } from 'react-icons/bs';
import api from '../api/axios';
import useDocTitle from '../hooks/useDocTitle';
import SectionsHead from '../components/common/SectionsHead';
import Services from '../components/common/Services';

const Profile = () => {
  useDocTitle('Profile');

  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    role: '',
    created_at: '',
  });

  const fetchProfile = async () => {
    try {
      const res = await api.get('/api/profile/', {
        withCredentials: true,
      });

      setFormData({
        name: res.data.user.name || '',
        email: res.data.user.email || '',
        phone: res.data.user.phone || '',
        role: res.data.user.role || '',
        created_at: res.data.user.created_at || '',
      });
    } catch (err) {
      console.log(err.response?.data || err);
    }
  };

  useEffect(() => {
    fetchProfile();
  }, []);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      await api.put(
        '/api/profile/',
        {
          name: formData.name,
          phone: formData.phone,
        },
        {
          withCredentials: true,
        }
      );

      alert('Profile updated successfully');
      fetchProfile();
    } catch (err) {
      console.log(err.response?.data || err);
    }
  };

  return (
    <>
      <section id="profile" className="section">
        <div className="container">
          <SectionsHead heading="My Profile" />

          <div className="wrapper profile_wrapper">
            <div className="profile_left_col">
              <div className="profile_form_card">
                <div className="profile_card_head">
                  <h3>Edit Profile</h3>
                  <p>Update your personal information for your account.</p>
                </div>

                <form onSubmit={handleSubmit} className="profile_form">
                  <div className="input_box">
                    <input
                      type="text"
                      name="name"
                      className="input_field"
                      value={formData.name}
                      onChange={handleChange}
                      required
                    />
                    <label className="input_label">Name</label>
                  </div>

                  <div className="input_box">
                    <input
                    type="email"
                    name="email"
                    className="input_field"
                    value={formData.email}
                    readOnly
                    />
                    <label className="input_label">Email</label>
                  </div>

                  <div className="input_box">
                    <input
                      type="text"
                      name="phone"
                      className="input_field"
                      value={formData.phone}
                      onChange={handleChange}
                    />
                    <label className="input_label">Phone</label>
                  </div>

                  <div className="profile_form_actions">
                    <button type="submit" className="btn">
                      Save Profile
                    </button>
                  </div>
                </form>
              </div>
            </div>

            <div className="profile_right_col">
              <div className="profile_info_card">
                <div className="profile_info_top">
                  <div className="profile_avatar">
                    <BsPersonCircle />
                  </div>

                  <div>
                    <h4>{formData.name || 'User'}</h4>
                    <p>{formData.email}</p>
                  </div>
                </div>

                <div className="separator"></div>

                <div className="profile_info_list">
                  <div className="profile_info_item">
                    <span className="profile_info_icon">
                      <BsEnvelope />
                    </span>
                    <div>
                      <h5>Email</h5>
                      <p>{formData.email || '-'}</p>
                    </div>
                  </div>

                  <div className="profile_info_item">
                    <span className="profile_info_icon">
                      <BsTelephone />
                    </span>
                    <div>
                      <h5>Phone</h5>
                      <p>{formData.phone || '-'}</p>
                    </div>
                  </div>

                  <div className="profile_info_item">
                    <span className="profile_info_icon">
                      <BsShieldCheck />
                    </span>
                    <div>
                      <h5>Role</h5>
                      <p>{formData.role || 'customer'}</p>
                    </div>
                  </div>
                </div>
              </div>

              <div className="profile_hint">
                <span>Keep your profile information up to date for a smoother shopping experience.</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <Services />
    </>
  );
};

export default Profile;