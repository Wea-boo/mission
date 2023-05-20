import Modal from 'react-modal';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faDownload } from '@fortawesome/free-solid-svg-icons';
import './EventModal.css'

const EventModal = ({isOpen, onRequestClose, validationInfo}) => {

    return (
        <Modal
            isOpen={isOpen}
            onRequestClose={onRequestClose}
            contentLabel="Event Modal"
            className="event-modal"
            overlayClassName="event-modal-overlay"
            closeTimeoutMS={500} // This will apply a default transition effect on closing
        >
            <h2>Validation Info</h2>
            <div className="modal-content">
              <div className="modal-text">
                <p>{validationInfo?.observation_text}</p>
              </div>
              <div className="modal-download">
                <a href={validationInfo?.attachment} download>
                  <FontAwesomeIcon icon={faDownload} /> Download Attachment
                </a>
              </div>
            </div>
            <button className="modal-close-button" onClick={onRequestClose}>Close</button>
        </Modal>
    );
};
export default EventModal;