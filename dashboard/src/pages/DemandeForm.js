import React, { useEffect, useState } from "react";
import "./DemandeForm.css";
import axios from "axios";
import Cookies from "js-cookie";
import { useNavigate } from "react-router-dom";

const DemandeForm = () => {
  const [missionTypes, setMissionTypes] = useState([]);
  const [agencies, setAgencies] = useState([]);
  const [formVisible, setFormVisible] = useState(false);
  const [vehicleType, setVehicleType] = useState("0");
  const navigate = useNavigate()

  useEffect(() => {
    const fetchData = async () => {
      try {
        const missionTypesResponse = await axios.get("http://localhost:8000/api/mission-types/");
        const agenciesResponse = await axios.get("http://localhost:8000/api/agencies/");
        setMissionTypes(missionTypesResponse.data);
        setAgencies(agenciesResponse.data);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, []);

  const handleVehicleTypeChange = (event) => {
    setVehicleType(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    
    const usePersonalVehicle = vehicleType === "1";

    let formdata = {
      "type_mission": event.target.missionType.value,
      "use_personel_v": usePersonalVehicle,
      "mission_reason": event.target.motif.value,
      "destination": event.target.agency.value,
      "departure": event.target.departTime.value,
      "return": event.target.returnTime.value,
      "type_demand": 1
    }

    try {
      const authToken = Cookies.get("auth_token");
      const response = await axios.post("http://localhost:8000/api/create-demand/", formdata, {
        headers: {
          "Authorization": `Token ${authToken}`,
          "Content-Type": "application/json"
        }
      });

      if (response.status === 201) {
        alert("Demande créée avec succès !");
        navigate(`/demand/${response.data.id}`)
      } else {
        alert("Erreur lors de la création de la demande. Veuillez réessayer.");
      }
    } catch (error) {
      console.error("Error creating demand:", error);
      alert("Erreur lors de la création de la demande. Veuillez réessayer.");
    }
  };

  return (
    <div>
      <div className={"form-container active"}>
        <form className="demande-form" onSubmit={handleSubmit}>
          <label>Type de mission:</label>
          <select className="input" name="missionType">
            {missionTypes.map((missionType) => (
              <option key={missionType.id} value={missionType.id}>
                {missionType.name}
              </option>
            ))}
          </select>

          <label>Motif de déplacement:</label>
          <textarea className="input-motif" rows="2" name="motif" required></textarea>

          <label>Moyen de transport:</label>
          <select className="input" name="vehicleType" value={vehicleType} onChange={handleVehicleTypeChange}>
            <option value="0">Véhicule Service</option>
            <option value="1">Véhicule personnel</option>
          </select>

          <label>Agence:</label>
          <select className="input" name="agency">
            <option value="" hidden>--Choisir une agence--</option>
            {agencies.map((agency) => (
            <option key={agency.id} value={agency.id}>
              {agency.name}
            </option>
            ))}
          </select>

          <label>Date et heure départ:</label>
          <input type="datetime-local" className="input" name="departTime"/>

          <label>Date et heure retour:</label>
          <input type="datetime-local" className="input" name="returnTime"/>

          <div className="button-container">
            <button className="button-a" type="button">Annuler</button>
            <button className="button-e" type="submit">Enregistrer</button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default DemandeForm;
