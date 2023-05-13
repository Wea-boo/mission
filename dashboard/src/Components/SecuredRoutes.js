import React from "react";
import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "../Contexts/AuthContexts";
import Sidebar from "./Sidebar";
import Navbar from "./NavBar";
import LoadingSpinner from './LoadingSpinner';

function SecuredRoutes() {
  const { isLoggedIn, loading } = useAuth();

  if (loading) {
    return <LoadingSpinner />; // or return a loading indicator
  }

  return (
    isLoggedIn ? 
    <>
      <Navbar />
      <Sidebar>
        <Outlet />
      </Sidebar>
    </> 
    : 
    <Navigate to="/login"/>
  );
}

export default SecuredRoutes;