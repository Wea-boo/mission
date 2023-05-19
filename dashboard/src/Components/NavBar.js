import React from "react";
import { NavLink } from "react-router-dom";
import { FaUserEdit } from "react-icons/fa";
import "./NavBar.css";

const Navbar = () => {
  return (
    <nav className="navbar">
      <ul className="navbar-nav">
        <li className="nav-item">
          <NavLink to="/DemandeForm" className="nav-link">
            nouvelle demande <FaUserEdit />
          </NavLink>
        </li>
      </ul>
    </nav>
  );
};

export default Navbar;