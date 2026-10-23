import React, { createContext, useContext, useState, useEffect } from 'react';
import { authApi, setAuthToken } from '../services/api';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  // In-memory authentication state (Tokens are strictly NOT stored in localStorage)
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Clean up any stale localStorage items to enforce strict security compliance
    try {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
    } catch (e) {
      // Ignored
    }

    // Check tab-isolated sessionStorage for active tab lifetime persistence
    try {
      const sessionTok = sessionStorage.getItem('auth_token_session');
      const sessionUser = sessionStorage.getItem('auth_user_session');

      if (sessionTok && sessionUser) {
        setToken(sessionTok);
        setAuthToken(sessionTok);
        setUser(JSON.parse(sessionUser));
      }
    } catch (e) {
      sessionStorage.removeItem('auth_token_session');
      sessionStorage.removeItem('auth_user_session');
    }
    setLoading(false);
  }, []);

  const login = async (email, password) => {
    const data = await authApi.login(email, password);
    const userData = {
      id: data.id,
      email: data.email,
      fullName: data.fullName,
      roles: data.roles,
    };

    setToken(data.token);
    setUser(userData);
    setAuthToken(data.token);

    // Persist only within the active browser tab session (cleared upon tab close)
    sessionStorage.setItem('auth_token_session', data.token);
    sessionStorage.setItem('auth_user_session', JSON.stringify(userData));

    return data;
  };

  const register = async (email, password, fullName) => {
    const data = await authApi.register(email, password, fullName);
    const userData = {
      id: data.id,
      email: data.email,
      fullName: data.fullName,
      roles: data.roles,
    };

    setToken(data.token);
    setUser(userData);
    setAuthToken(data.token);

    sessionStorage.setItem('auth_token_session', data.token);
    sessionStorage.setItem('auth_user_session', JSON.stringify(userData));

    return data;
  };

  const logout = () => {
    authApi.logout();
    setToken(null);
    setUser(null);
    setAuthToken(null);
    sessionStorage.removeItem('auth_token_session');
    sessionStorage.removeItem('auth_user_session');
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        loading,
        isAuthenticated: !!token,
        login,
        register,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
