import React, { useState } from "react";
import "./Demandes.css";

const Demandes = () => {
  return (
      <div className="table-container">
        <table className="custom-table">
            <thead>
                <tr>
                    <th className="table-header">N° demande</th>
                    <th className="table-header">Titre</th>
                    <th className="table-header">Assigné</th>
                    <th className="table-header">état</th>
                    <th className="table-header">Date</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td className="table-cell">1</td>
                    <td className="table-cell">Titre 1</td>
                    <td className="table-cell">Assigné 1</td>
                    <td className="table-cell">état 1</td>
                    <td className="table-cell">2023-04-24</td>
                </tr>
                <tr>
                    <td className="table-cell">2</td>
                    <td className="table-cell">Titre 2</td>
                    <td className="table-cell">Assigné 2</td>
                    <td className="table-cell">état 2</td>
                    <td className="table-cell">2023-04-25</td>
                 </tr>
                 <tr>
                    <td className="table-cell">3</td>
                    <td className="table-cell">Titre 3</td>
                    <td className="table-cell">Assigné 3</td>
                    <td className="table-cell">état 3</td>
                    <td className="table-cell">2023-04-25</td>
                </tr>
                 <tr>
                    <td className="table-cell">4</td>
                    <td className="table-cell">Titre 4</td>
                    <td className="table-cell">Assigné 4</td>
                    <td className="table-cell">état 4</td>
                    <td className="table-cell">2023-04-25</td>
                </tr>
                <tr>
                    <td className="table-cell">5</td>
                    <td className="table-cell">Titre 5</td>
                    <td className="table-cell">Assigné 5</td>
                    <td className="table-cell">état 5</td>
                    <td className="table-cell">2023-04-25</td>
                </tr>
                <tr>
                    <td className="table-cell">6</td>
                    <td className="table-cell">Titre 6</td>
                    <td className="table-cell">Assigné 6</td>
                    <td className="table-cell">état 6</td>
                    <td className="table-cell">2023-04-25</td>
                </tr>
            </tbody>
        </table>
     </div>   
  );
};

export default Demandes;