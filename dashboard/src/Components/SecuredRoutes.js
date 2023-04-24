import React from "react";
import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "../Contexts/AuthContexts";
import Sidebar from "./Sidebar";

function SecuredRoutes() {
  const { isLoggedIn, loading } = useAuth();

  if (loading) {
    return <p>LOADING...</p>; // or return a loading indicator
  }

  return (
    isLoggedIn ? <Sidebar><Outlet/></Sidebar> : <Navigate to="/login"/>
  );
}

export default SecuredRoutes;