import React, { useContext, useRef, useState } from 'react';
import { Link } from 'react-router-dom';
import commonContext from '../../contexts/common/commonContext';
import useForm from '../../hooks/useForm';
import useOutsideClose from '../../hooks/useOutsideClose';
import useScrollDisable from '../../hooks/useScrollDisable';
import api from '../../api/axios';

const AccountForm = () => {
  const { isFormOpen, toggleForm, setCurrentUser } = useContext(commonContext);
  const { inputValues, handleInputValues } = useForm();

  const formRef = useRef();
  const [isSignupVisible, setIsSignupVisible] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  useOutsideClose(formRef, () => {
    toggleForm(false);
  });

  useScrollDisable(isFormOpen);

  const handleIsSignupVisible = () => {
    setIsSignupVisible((prev) => !prev);
    setErrorMessage('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      setErrorMessage('');

      if (isSignupVisible) {
        await api.post('/api/auth/signup/', {
          username: inputValues.username,
          email: inputValues.email,
          phone: inputValues.phone,
          password: inputValues.password,
          conf_password: inputValues.conf_password,
        });

        setErrorMessage('');
        alert('Signup successful. Please login.');
        setIsSignupVisible(false);
        return;
      }

      await api.post('/api/auth/login/', {
        email: inputValues.email,
        password: inputValues.password,
      });

      const me = await api.get('/api/auth/me/');
      setCurrentUser(me.data);

      console.log('logged in user:', me.data);

      toggleForm(false);
    } catch (err) {
      console.log(err.response?.data);
      setErrorMessage(err.response?.data?.message || 'Request failed');
    }
  };

  return (
    <>
      {isFormOpen && (
        <div className="backdrop">
          <div className="modal_centered">
            <form id="account_form" ref={formRef} onSubmit={handleSubmit}>
              <div className="form_head">
                <h2>{isSignupVisible ? 'Signup' : 'Login'}</h2>
                <p>
                  {isSignupVisible ? 'Already have an account ?' : 'New to PurePro ?'}
                  &nbsp;&nbsp;
                  <button type="button" onClick={handleIsSignupVisible}>
                    {isSignupVisible ? 'Login' : 'Create an account'}
                  </button>
                </p>
              </div>

              <div className="form_body">
                {isSignupVisible && (
                  <div className="input_box">
                    <input
                      type="text"
                      name="username"
                      className="input_field"
                      value={inputValues.username || ''}
                      onChange={handleInputValues}
                      required
                    />
                    <label className="input_label">Username</label>
                  </div>
                )}

                <div className="input_box">
                  <input
                    type="email"
                    name="email"
                    className="input_field"
                    value={inputValues.email || ''}
                    onChange={handleInputValues}
                    required
                  />
                  <label className="input_label">Email</label>
                </div>

                {isSignupVisible && (
                  <div className="input_box">
                    <input
                      type="tel"
                      name="phone"
                      className="input_field"
                      value={inputValues.phone || ''}
                      onChange={handleInputValues}
                      required
                    />
                    <label className="input_label">Phone</label>
                  </div>
                )}

                <div className="input_box">
                  <input
                    type="password"
                    name="password"
                    className="input_field"
                    value={inputValues.password || ''}
                    onChange={handleInputValues}
                    required
                  />
                  <label className="input_label">Password</label>
                </div>

                {isSignupVisible && (
                  <div className="input_box">
                    <input
                      type="password"
                      name="conf_password"
                      className="input_field"
                      value={inputValues.conf_password || ''}
                      onChange={handleInputValues}
                      required
                    />
                    <label className="input_label">Confirm Password</label>
                  </div>
                )}

                {errorMessage && <p className="form_error_text">{errorMessage}</p>}

                <button type="submit" className="btn login_btn">
                  {isSignupVisible ? 'Signup' : 'Login'}
                </button>
              </div>

              <div className="form_foot">
                <p>or login with</p>
                <div className="login_options">
                  <Link to="/">Facebook</Link>
                  <Link to="/">Google</Link>
                  <Link to="/">Twitter</Link>
                </div>
              </div>

              <div className="close_btn" title="Close" onClick={() => toggleForm(false)}>
                &times;
              </div>
            </form>
          </div>
        </div>
      )}
    </>
  );
};

export default AccountForm;