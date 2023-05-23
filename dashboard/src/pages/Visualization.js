import { Link, useParams } from "react-router-dom";
import "./Visualization.css";
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import LoadingSpinner from "../Components/LoadingSpinner";
import DemandServices from "../Services/DemandServices";
import ValidationModal, { validationInfoRequirements } from "../Components/ValidationModal";
import EventTable from '../Components/EventTable';


const UserInfo = ({ title, user }) => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleOpen = () => {
    setIsOpen(!isOpen);
  };

  return (
    <section className="user-info info-section">

      <p><span className="info-label-1" id="user-title">{title} </span></p>
      <>
        <p> {user.employee.first_name} {user.employee.last_name}</p>
        <p> {user.employee.phone}</p>
        <p>{user.username.email}</p>
        {/*<p>{user.employee.grade}</p>*/}
        {/*<p>{user.employee.function}</p> */}
        <p>{user.employee.direction.name}</p>
      </>
    </section>
  );
};

const Visualization = () => {
  const { demand_id } = useParams();
  const [demand, setDemand] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [Actions, setActions] = useState([]);
  const [modalOpen, setModalOpen] = useState(false);
  const [currentAction, setCurrentAction] = useState(null);
  const [observation, setObservation] = useState('');
  const [attachment, setAttachment] = useState(null);
  const [events, setEvents] = useState([]);

  const openModal = (action) => {
    setCurrentAction(action);
    setModalOpen(true);
  };

  const closeModal = () => {
    setModalOpen(false);
    setCurrentAction(null);
    setObservation('');
    setAttachment(null);
  };

  const handleSubmit = async (observation, attachment) => {
    try {
      await DemandServices.triggerTransition(demand_id, currentAction?.action, observation, attachment);
      closeModal();
    } catch (error) {
      console.error(`Error triggering transition '${currentAction?.action}':`, error);
      alert(`Failed to trigger transition: ${error.message}`);
    }
  };

  useEffect(() => {
    const fetchDemandDetails = async () => {
      try {
        const response = await DemandServices.getDemand(demand_id);
        setDemand(response.data);
        setIsLoading(false);
      } catch (error) {
        console.error('Error fetching demand details:', error);
      }
    };
    const fetchTransitions = async () => {
      try {
        const response = await DemandServices.getTransitions(demand_id);
        setActions(response.data);
      } catch (error) {
        console.error('Error fetching transitions:', error);
      }
    };

    const fetchDemandEvents = async () => {
      try {
        const response = await DemandServices.getDemandEvents(demand_id);
        setEvents(response.data);
      } catch (error) {
        console.error('Error fetching demand events:', error);
      }
    }

    fetchDemandDetails();
    fetchTransitions();
    fetchDemandEvents();
  }, [demand_id]);


  const handleButtonClick = async (action) => {
    try {
      await DemandServices.triggerTransition(demand_id, action);

    } catch (error) {
      console.error(`Error triggering transition '${action}':`, error);
      // Handle the error here, for example show a notification or an alert
      alert(`Failed to trigger transition: ${error.message}`);
    }
  };


  return (
    <div className="Visualization">
      {isLoading ? (
        <LoadingSpinner />
      ) : (

          <div style={{ height: "100%", width: "100%", maxWidth: "1200px" }}>
            <div className="actions-container">
              {Actions.map(action => (
                <button
                  key={action.id}
                  className="action-button"
                  onClick={() => openModal(action)}>
                  {action.action}
                </button>
              ))}
            </div>
            <ValidationModal
              isOpen={modalOpen}
              onRequestClose={closeModal}
              onSubmit={handleSubmit}
              missionSummary={demand.mission_summary}
            />
            <h2 className="Title">Mission : {demand.demand.creator.employee.first_name} {demand.demand.creator.employee.last_name}</h2>
            {/*<div className="details-container">*/}
            <section className="demande-info info-section">
              {/*<h2>Informations Demande:</h2>*/}

              <UserInfo title="Demandeur" user={demand.demand.creator} />
              <UserInfo title="Assigné" user={demand.demand.assignee} />

            </section>

            <section className="mission-info info-section">
              {/*<h2>Informations sur la mission:</h2>*/}
              <p><span className="info-label-2">état:</span>{demand.demand.state.name}</p>
              <p><span className="info-label-2">Type de mission:</span> {demand.mission_type.name}</p>
              <p><span className="info-label-2">Motif de déplacement:</span> {demand.trip_purpose}</p>
              <p><span className="info-label-2">Moyen de transport:</span> {demand.use_personal_vehicle ? "véhicule personnel" : "véhicule de service"}</p>
              <p><span className="info-label-2">Agence:</span> {demand.agency.name}</p>
              <p>
                <span className="info-label-2">Date et heure départ:</span>{' '}
                {new Date(demand.departing).toLocaleString()}
              </p>
              <p>
                <span className="info-label-2">Date et heure retour:</span>{' '}
                {new Date(demand.returning).toLocaleString()}
              </p>
              <p><span className="info-label-2">Adresse de l'agence:</span> {demand.agency.address}</p>
              <p><span className="info-label-2">Téléphone de l'agence:</span> {demand.agency.phone}</p>
              {demand.observation_manager && <p><span className="info-label">Observation Manager:</span> {demand.observation_manager}</p>}
              {demand.observation_HR && <p><span className="info-label">Observation HR:</span> {demand.observation_HR}</p>}
            </section>
            <div className="demande-dates">
              <div>
                <span className="info-label-1">crée le : </span> {new Date(demand.demand.created_at).toLocaleString()}
              </div>
              <div className="last-modified">
                <span className="info-label-1">dernière modification:</span>{' '}
                {new Date(demand.demand.last_modified).toLocaleString()}
              </div>
            </div>
            <div className="event-table-container">
              <EventTable events={events} />
            </div>
            <Link to="/Dashboard" className="back-button">
              Retour
            </Link>
          </div>
        )}
    </div>
  );
};

export default Visualization;