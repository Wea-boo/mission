import React, { useState } from "react";
import "./App.css";
import { BrowserRouter as Router, Route, Routes, Navigate } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import Demandes from "./pages/Demandes";
import Stats from "./pages/Stats";
import Sidebar from "./Components/Sidebar";
import LoginForm from "./Components/loginform";
import { AuthProvider } from "./Contexts/AuthContexts";
import SecuredRoutes from "./Components/SecuredRoutes";
import LoginRedirect from "./Components/LoginRedirect";

const App = () => {

  return (
    <AuthProvider>
      <Router>
        <div className="App">
          <Routes>
            <Route element={<SecuredRoutes />}>
              <Route path="/" element={<Dashboard />} />
              <Route path="/Dashboard" element={<Dashboard />} />
              <Route path="/Demandes" element={<Demandes />} />
              <Route path="/Stats" element={<Stats />} />
            </Route>
            <Route path="/Login" element={<LoginRedirect />} />
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  );
};


export default App;
