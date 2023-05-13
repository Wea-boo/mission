import "./Dashboard.css";
import { Link } from "react-router-dom";

const Dashboard = ({ setSelectedFilter }) => {
  return (
    <div>
      <div className="grid-container">
        <Link to="/Demandes" className="card" onClick={() => setSelectedFilter(0)}>Demandes attente validation</Link>
        <Link to="/Demandes" className="card" onClick={() => setSelectedFilter(1)}>Demandes validées</Link>
      </div>
    </div>
  );
};

export default Dashboard;