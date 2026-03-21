import { createContext, useReducer, useEffect } from 'react';
import commonReducer from './commonReducer';
import api from '../../api/axios';

// Common-Context
const commonContext = createContext();

// Initial State
const initialState = {
  isFormOpen: false,
  formUserInfo: '',
  isSearchOpen: false,
  searchResults: [],
  currentUser: null,
  authLoading: true,
};

// Common-Provider Component
const CommonProvider = ({ children }) => {
  const [state, dispatch] = useReducer(commonReducer, initialState);

  useEffect(() => {
    const checkAuth = async () => {
      try {
        // add timeout safety to prevent infinite pending
        const res = await api.get('/api/auth/me/', {
          timeout: 10000, // stop waiting after 10s
        });
        setCurrentUser(res.data);
      } catch (err) {
        // handle network timeout / error safely
        setCurrentUser(null);
      } finally {
        setAuthLoading(false); // always stop loading
      }
    };

    checkAuth();
  }, []);

  useEffect(() => {
    const handleAutoLogout = () => {
      setCurrentUser(null);
      setAuthLoading(false);
    };

    window.addEventListener("auth:logout", handleAutoLogout);

    return () => {
      window.removeEventListener("auth:logout", handleAutoLogout);
    };
  }, []);

  // Form actions
  const toggleForm = (toggle) => {
    return dispatch({
      type: 'TOGGLE_FORM',
      payload: { toggle },
    });
  };

  const setFormUserInfo = (info) => {
    return dispatch({
      type: 'SET_FORM_USER_INFO',
      payload: { info },
    });
  };

  // Search actions
  const toggleSearch = (toggle) => {
    return dispatch({
      type: 'TOGGLE_SEARCH',
      payload: { toggle },
    });
  };

  const setSearchResults = (results) => {
    return dispatch({
      type: 'SET_SEARCH_RESULTS',
      payload: { results },
    });
  };

  const setCurrentUser = (user) => {
    return dispatch({
      type: 'SET_CURRENT_USER',
      payload: { user },
    });
  };

  const setAuthLoading = (loading) => {
    return dispatch({
      type: 'SET_AUTH_LOADING',
      payload: { loading },
    });
  };

  // Context values
  const values = {
    ...state,
    toggleForm,
    setFormUserInfo,
    toggleSearch,
    setSearchResults,
    setCurrentUser,
    setAuthLoading,
  };

  return (
    <commonContext.Provider value={values}>
      {children}
    </commonContext.Provider>
  );
};

export default commonContext;
export { CommonProvider };