import React from "react";
import "./Dashboard.css";
import { Link } from "react-router-dom";

const Dashboard = ({ setSelectedFilter }) => {
  return (
    <div>
      <h1>Mes demandes</h1>
      <hr />
      
      <div className="grid-container-1">
        <Link to="/Demandes" className="card" onClick={() => setSelectedFilter(0)}>Demandes attente validation</Link>
        <Link to="/Demandes" className="card" onClick={() => setSelectedFilter(1)}>Liste des demandes validées</Link>
      </div>
      <h1>demandes employe</h1>
      <hr />
      <div className="grid-container-2">
        <Link to="/Demandes" className="card" onClick={() => setSelectedFilter(0)}>Demandes attente validation</Link>
      </div>
    </div>
  );
};
export default Dashboard;