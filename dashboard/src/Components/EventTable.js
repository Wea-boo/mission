import React, { useState } from 'react';
import './EventTable.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faInfoCircle } from '@fortawesome/free-solid-svg-icons';
import EventModal from './EventModal';

const EventTable = ({ events }) => {
    const [open, setOpen] = useState(false);
    const [currentEvent, setCurrentEvent] = useState(null);

    const onOpenModal = (event) => {
      setCurrentEvent(event);
      setOpen(true);
    };
  
    const onCloseModal = () => {
      setOpen(false);
      setCurrentEvent(null);
    };

    return (
      <>
        <table className="event-table">
          <thead>
            <tr>
              <th>Trigger User</th>
              <th>Action</th>
              <th>Start State</th>
              <th>End State</th>
              <th>Time Event</th>
              <th>Validation Info</th>
            </tr>
          </thead>
          <tbody>
            {events.map(event => (
              <tr key={event.id}>
                <td>{event.trigger_user}</td>
                <td>{event.transition.action}</td>
                <td>{event.transition.start_state}</td>
                <td>{event.transition.end_state}</td>
                <td>{new Date(event.time_event).toLocaleString()}</td>
                <td>
                {event.validation_info &&
                  <button 
                    onClick={() => onOpenModal(event.validation_info)}
                    className="info-button">
                    <FontAwesomeIcon icon={faInfoCircle} />
                  </button>}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        <EventModal 
        isOpen={open} 
        onRequestClose={onCloseModal} 
        validationInfo={currentEvent} 
      />
      </>
    );
  }; export default EventTable;
  