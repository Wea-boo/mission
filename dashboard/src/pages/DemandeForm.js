import React, { useEffect, useState } from "react";
import "./DemandeForm.css";
import axios from "axios";
import Cookies from "js-cookie";
import { useNavigate } from "react-router-dom";
import DemandServices from "../Services/DemandServices";
import AuthServices from "../Services/AuthServices";

const DemandeForm = () => {
  const [missionTypes, setMissionTypes] = useState([]);
  const [agencies, setAgencies] = useState([]);
  const [creatingForSelf, setCreatingForSelf] = useState(true);
  const [vehicleType, setVehicleType] = useState("0");
  const [usersInSameDirection, setUsersInSameDirection] = useState([]);
  const [selectedUser, setSelectedUser] = useState();
  const [userRoles, setUserRoles] = useState(null);
  const navigate = useNavigate()

  useEffect(() => {
    const fetchData = async () => {
      try {
        const missionTypesResponse = await axios.get("http://localhost:8000/api/mission-types/");
        const agenciesResponse = await axios.get("http://localhost:8000/api/agencies/");
        setMissionTypes(missionTypesResponse.data);
        setAgencies(agenciesResponse.data);

        const userRolesResponse = await AuthServices.checkUserRoles();
        console.log(userRolesResponse.data)
        setUserRoles(userRolesResponse.data);

        if (userRolesResponse.data.is_secretary) {
          const usersInSameDirectionResponse = await AuthServices.fetchUsersInSameDirection();
          console.log(usersInSameDirectionResponse.data)
          setUsersInSameDirection(usersInSameDirectionResponse.data);
        }
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, []);

  const handleVehicleTypeChange = (event) => {
    setVehicleType(event.target.value);
  };

  const handleToggleChange = () => {
    setCreatingForSelf(!creatingForSelf);
  };

  const handleUserChange = (event) => {
    console.log(event.target.value);
    setSelectedUser(event.target.value);
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
    const creatingForOthers = userRoles?.is_secretary && !creatingForSelf && selectedUser;

    if (creatingForOthers) {
      formdata["creator"] = selectedUser;
    }
  
    try {
      const response = await DemandServices.postDemand(formdata, creatingForOthers);
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
    <>
      <div className={"form-container active"}>
        <form className="demande-form" onSubmit={handleSubmit}>
        {userRoles?.is_secretary && (
            <div>
              <label>Creating for myself</label>
              <input type="checkbox" checked={creatingForSelf} onChange={handleToggleChange} />
            </div>)}
          {userRoles?.is_secretary && !creatingForSelf && (
            <div>
              <label>Créateur de la demande:</label>
              <select className="input" name="demandCreator" value={selectedUser} onChange={handleUserChange}>
                {usersInSameDirection.map((user) => (
                  <option key={user.id} value={user.id}>
                    {user.username}
                  </option>
                ))}
              </select>
            </div>
          )}
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
          <div className="date-dem-container">
            <div className="date-dem-field">
              <label>Date et heure départ:</label>
              <input type="datetime-local" className="input" name="departTime"/>
            </div>
            <div className="date-dem-field">
              <label>Date et heure retour:</label>
              <input type="datetime-local" className="input" name="returnTime"/>            
            </div>
          </div>
          <div className="button-container">
            <button className="button-a" type="button" onClick={() => navigate("/dashboard")}>Annuler</button>
            <button className="button-e" type="submit">Enregistrer</button>
          </div>
        </form>
      </div>
    </>
  );
};

export default DemandeForm;
