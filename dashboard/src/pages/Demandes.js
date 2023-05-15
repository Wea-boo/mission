import React from "react";
import { Link, useNavigate } from "react-router-dom";
import "./Demandes.css";

const Demandes = ({ filter }) => {
    const navigate = useNavigate();
  
    const handleVoirDemandeClick = () => {
      navigate("/Visualization");
    };
  
    return (
      <div className="table-container">
        {filter === 0 && (
          <table className="custom-table">
            <thead>
              <tr>
                <th className="table-header">N° demande</th>
                <th className="table-header">Titre</th>
                <th className="table-header">Assigné</th>
                <th className="table-header">état</th>
                <th className="table-header">Date</th>
                <th className="table-header">Action</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td className="table-cell">1</td>
                <td className="table-cell">Titre 1</td>
                <td className="table-cell">Assigné 1</td>
                <td className="table-cell">état 1</td>
                <td className="table-cell">2023-04-24</td>
                <td className="table-cell">
                  <button className="btn" onClick={handleVoirDemandeClick}>
                    Voir demande
                  </button>
                </td>
              </tr>
              <tr>
                <td className="table-cell">2</td>
                <td className="table-cell">Titre 2</td>
                <td className="table-cell">Assigné 2</td>
                <td className="table-cell">état 2</td>
                <td className="table-cell">2023-04-25</td>
                <td className="table-cell">
                  <button className="btn" onClick={handleVoirDemandeClick}>
                    Voir demande
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        )}
        {filter === 1 &&
            <table className="custom-table">
                <thead>
                    <tr>
                        <th className="table-header">N° demande</th>
                        <th className="table-header">Titre</th>
                        <th className="table-header">Assigné</th>
                        <th className="table-header">état</th>
                        <th className="table-header">Date</th>
                        <th className="table-header"></th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td className="table-cell">3</td>
                        <td className="table-cell">Titre 3</td>
                        <td className="table-cell">Assigné 3</td>
                        <td className="table-cell">état 3</td>
                        <td className="table-cell">
                  <button className="btn" onClick={handleVoirDemandeClick}>
                    Voir demande
                  </button>
                </td>
                    </tr>
                    <tr>
                        <td className="table-cell">4</td>
                        <td className="table-cell">Titre 4</td>
                        <td className="table-cell">Assigné 4</td>
                        <td className="table-cell">état 4</td>
                        <td className="table-cell">
                  <button className="btn" onClick={handleVoirDemandeClick}>
                    Voir demande
                  </button>
                </td>
                    </tr>
                </tbody>
            </table>
        }    
     </div>   
  );
};

export default Demandes;