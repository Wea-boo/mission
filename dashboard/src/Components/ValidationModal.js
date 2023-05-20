import React, { useState } from 'react';
import Modal from 'react-modal';

const customStyles = {
    content: {
      top: '50%',
      left: 'calc(50% + 79.86px)',
      right: 'auto',
      bottom: 'auto',
      marginRight: '-50%',
      transform: 'translate(-50%, -50%)',
      backgroundColor: 'white',
      borderRadius: '4px',
      width: '40%', // You can change this as per your requirement
      height: 'auto', // You can change this as per your requirement
      padding: '20px',
      boxShadow: '0px 0px 10px rgba(0,0,0,0.1)', // adding a subtle shadow
      border: 'none', // removing default border
    },
    overlay: {
      backgroundColor: 'rgba(0,0,0,0.5)', // semi-transparent backdrop
    },
};


const ValidationModal = ({ isOpen, onRequestClose, onSubmit, missionSummary }) => {
    const [observation, setObservation] = useState('');
    const [attachment, setAttachment] = useState(null);
  
    const handleSubmit = () => {
      onSubmit(observation, attachment);
    };

    const handleFileChange = (e) => {
        const file = e.target.files[0];
        const allowedFileTypes = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']; // Add more if needed
        if (!allowedFileTypes.includes(file.type)) {
            alert('Please select a valid file type (.pdf, .doc, .docx)');
            return;
        }
        setAttachment(file);
    };
    return (
        <Modal isOpen={isOpen} onRequestClose={onRequestClose} style={customStyles}>
                <h2 style={{ marginBottom: '20px' }}>Résumé de la mission:</h2>
                <div style={{ marginBottom: '15px' }}>
                    <p style={{ marginBottom: '15px' }}>{missionSummary}</p>
                <div/>
                <label style={{ display: 'block', marginBottom: '5px' }}>Observation</label>
                <textarea 
                    rows="4"
                    value={observation}
                    required
                    onChange={e => setObservation(e.target.value)}
                    style={{ width: '100%', padding: '10px', border: '1px solid #ccc', borderRadius: '4px' }}
                />
            </div>
            <div style={{ marginBottom: '15px' }}>
                <label style={{ display: 'block', marginBottom: '5px' }}>Attachment</label>
                <input 
                    type="file"
                    required
                    onChange={handleFileChange}
                    style={{ display: 'block' }}
                />
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '20px' }}>
                <button onClick={handleSubmit} style={{ padding: '10px 20px', background:'#007bff', color: '#fff', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
                    Submit
                </button>
                <button onClick={onRequestClose} style={{ padding: '10px 20px', background: '#dc3545', color: '#fff', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
                    Cancel
                </button>
            </div>
        </Modal>
    );
};

export default ValidationModal;