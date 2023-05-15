import React from "react";
import { NavLink } from 'react-router-dom';
import { BsFillArrowDownCircleFill } from 'react-icons/bs';
import "./NavBar.css";

const Navbar = () => {
  return (
    <nav className="navbar">
      <ul className="navbar-nav">
        <li className="nav-item dropdown créer-demande">
          <a href="#" className="nav-link dropdown-toggle">Créer Demande <BsFillArrowDownCircleFill /></a>
          <ul className="dropdown-menu">
            <li>
              <NavLink to="/DemandeForm" className="dropdown-item">Mission</NavLink>
            </li>
            <li>
              <NavLink to="/Dashboard" className="dropdown-item">Frais</NavLink>
            </li>
          </ul>
        </li>
      </ul>
    </nav>
  );
};

export default Navbar;