import React, { createContext, useContext, useState } from 'react'

const SESSION_KEY = 'loggedin';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [isLoggedIn, setIsLoggedIn] = useState(!!sessionStorage.getItem(SESSION_KEY));
  // The !! means convert to boolean

  const login = async(username, password) => {
    const payload = { username, password }
    

    try {
      const response = await fetch('/api/auth/login',{
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      if (response.ok) {
        const data = await response.json();

        sessionStorage.setItem(SESSION_KEY, 'true');
        setIsLoggedIn(true);
        setUser({username: data.username});

        return true;
      }
      else {
        return false;
      }
    }
    catch (error) {
      return false;
    }
  };

  const logout = () => {
    sessionStorage.removeItem(SESSION_KEY);
    setIsLoggedIn(false);
    setUser(null);
  }

  const value = {
    user,
    isLoggedIn,
    login,
    logout
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if( context === undefined ){
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}