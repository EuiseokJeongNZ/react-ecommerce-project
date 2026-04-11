import React, { useContext, useRef, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useGoogleLogin } from "@react-oauth/google";
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

  const navigate = useNavigate();

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

      toggleForm(false);
      navigate('/');
      setTimeout(() => {
        window.location.reload();
      }, 100);
    } catch (err) {
      setErrorMessage(err.response?.data?.message || 'Request failed');
    }
  };

  const googleLogin = useGoogleLogin({
    flow: 'implicit',
    onSuccess: async (tokenResponse) => {
      try {
        console.log(tokenResponse);
        setErrorMessage('');

        await api.post('/api/auth/google/', {
          access_token: tokenResponse.access_token,
        });

        const me = await api.get('/api/auth/me/');
        setCurrentUser(me.data);

        toggleForm(false);
        navigate('/');
        setTimeout(() => {
          window.location.reload();
        }, 100);
      } catch (err) {
        console.log(err.response?.data);
        setErrorMessage(err.response?.data?.message || 'Google login failed');
      }
    },
    onError: () => {
      setErrorMessage('Google login failed');
    },
  });

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
                    <button
                      type="button"
                      className="social_login_btn google_custom_btn"
                      onClick={() => googleLogin()}
                    >
                      <span>Continue with </span>
                      <span className="google_icon">
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          viewBox="0 0 48 48"
                          width="18"
                          height="18"
                        >
                          <path fill="#FFC107" d="M43.611 20.083H42V20H24v8h11.303C33.65 32.657 29.243 36 24 36c-6.627 0-12-5.373-12-12s5.373-12 12-12c3.059 0 5.842 1.154 7.961 3.039l5.657-5.657C34.046 6.053 29.27 4 24 4 12.955 4 4 12.955 4 24s8.955 20 20 20 20-8.955 20-20c0-1.341-.138-2.65-.389-3.917z"/>
                          <path fill="#FF3D00" d="M6.306 14.691l6.571 4.819C14.655 16.108 18.961 13 24 13c3.059 0 5.842 1.154 7.961 3.039l5.657-5.657C34.046 6.053 29.27 4 24 4c-7.682 0-14.347 4.337-17.694 10.691z"/>
                          <path fill="#4CAF50" d="M24 44c5.166 0 9.86-1.977 13.409-5.192l-6.19-5.238C29.143 35.091 26.715 36 24 36c-5.222 0-9.617-3.317-11.283-7.946l-6.522 5.025C9.505 39.556 16.227 44 24 44z"/>
                          <path fill="#1976D2" d="M43.611 20.083H42V20H24v8h11.303c-.793 2.272-2.25 4.219-4.094 5.57l.003-.002 6.19 5.238C36.971 39.205 44 34 44 24c0-1.341-.138-2.65-.389-3.917z"/>
                        </svg>
                      </span>
                      <span>oogle </span>
                    </button>
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