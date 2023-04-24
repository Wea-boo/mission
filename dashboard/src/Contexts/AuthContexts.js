import React, { createContext, useState, useContext, useEffect } from "react";
import AuthServices from "../Services/AuthServices";

const AuthContext = createContext();

export function useAuth() {
  return useContext(AuthContext);
}

export function AuthProvider({ children }) {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [loading, setLoading] = useState(true);

  const handleLogin = async (username, password) => {
    try {
      const response = await AuthServices.login({ username, password });
      if (response.status === 200) {
        setIsLoggedIn(true);
      } else {
        console.log(response.status)
      }
    } catch (error) {
      console.log(error)
    }
    
  };

  const handleLogout = async () => {
    try {
      await AuthServices.logout();
      setIsLoggedIn(false);
    } catch (error) {
      console.log(error)
    }
  };

  useEffect(() => {
    const checkLoggedInStatus = async () => {
      try {
        const response = await AuthServices.checkAuth();
        console.log(response.data.is_authenticated);
        setIsLoggedIn(response.data.is_authenticated);
        console.log(isLoggedIn)
      } catch (error) {
        console.log(error);
      } finally {
        setLoading(false);
      }
    };
  
    checkLoggedInStatus();
  }, []);
  
  const value = {
    loading,
    isLoggedIn,
    handleLogin,
    handleLogout,
  };

  return (
    <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
  );
}
