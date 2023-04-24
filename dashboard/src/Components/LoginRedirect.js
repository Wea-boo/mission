import React from "react";
import { useAuth } from "../Contexts/AuthContexts";
import { Navigate } from "react-router-dom";
import LoginForm from "./loginform";

function LoginRedirect() {
  const { isLoggedIn } = useAuth();

  return (
    isLoggedIn ? <Navigate to="/dashboard" /> : <LoginForm />
  );
}

export default LoginRedirect;