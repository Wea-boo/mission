import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import "./Demandes.css";
import FilterServices from '../Services/FilterServices';
import LoadingSpinner from '../Components/LoadingSpinner';

const Demandes = () => {
    const [demands, setDemands] = useState([]);
    const [loading, setLoading] = useState(true);
    const filterServices = new FilterServices();
    const location = useLocation();
    const navigate = useNavigate();
    const { filter } = location.state || {};

    useEffect(() => {
      const getFilteredDemands = async () => {
        setLoading(true);
        try {
          if(filter) {
            let states;
            if (Array.isArray(filter.state)) {
              states = filter.state.map(s => s.name).join(",");
            } else {
              states = filter.state.name;
            }
            
            const response = await filterServices.getFilteredDemands(
              filter.creator,
              filter.assignee,
              states,
              null
            );
            console.log(response.data.results)
            setDemands(response.data.results);
          } else {
            console.log("no filter found");
          }
        } catch (error) {
          console.error(error);
        }
        setLoading(false);
      };
      
      getFilteredDemands();
    }, [filter]);

    const handleVoirDemandeClick = (id) => {
      navigate(`/demand/${id}`);
    };

    if (loading) {
      return <LoadingSpinner />
    }

    return (
      <div className="table-container">
        <table className="custom-table">
          <thead>
            <tr>
              <th className="table-header">N° demande</th>
              <th className="table-header">Titre</th>
              <th className="table-header">Assigné</th>
              <th className="table-header">état</th>
              <th className="table-header">Date de création</th>
              <th className="table-header">Dernière mise à jour</th>
              <th className="table-header">Action</th>
            </tr>
          </thead>
          <tbody>
            {demands?.map((demand) => (
              <tr key={demand.id}>
                <td className="table-cell">{demand.id}</td>
                <td className="table-cell">{`Mission -- ${demand.creator}`}</td>
                <td className="table-cell">{demand.assignee}</td>
                <td className="table-cell">{demand.state}</td>
                <td className="table-cell">{new Date(demand.created_at).toLocaleDateString()}</td>
                <td className="table-cell">{new Date(demand.last_modified).toLocaleDateString()}</td>
                <td className="table-cell">
                  <button className="btn" onClick={() => handleVoirDemandeClick(demand.id)}>
                    Voir demande
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
};

export default Demandes;