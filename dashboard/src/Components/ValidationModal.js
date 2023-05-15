import React, { useState } from 'react';
import Modal from 'react-modal';

export const validationInfoRequirements = {
    'approuver': [{ type: 'textarea', label: 'Manager Observation', name: 'obs_manager', required: true}],
    'refuser': [{ type: 'textarea', label: 'Manager Observation', name: 'obs_manager', required: true}],
    'validate': [{ type: 'textarea', label: 'HR Manager Observation', name: 'obs_hr', required: true}],
    // Add more actions as required
};

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


const ValidationModal = ({ isOpen, onRequestClose, onSubmit, action }) => {
    const requirements = validationInfoRequirements[action?.action] || [];
    const [validationInfos, setValidationInfos] = useState(Array(requirements.length).fill(''));

    const inputs = requirements.map((requirement, i) => {
        if (requirement.type === 'textarea') {
            return (
                <div style={{ marginBottom: '15px' }} key={i}>
                    <label style={{ display: 'block', marginBottom: '5px' }}>{requirement.label}</label>
                    <textarea 
                        rows="4"
                        value={validationInfos[i]} 
                        name={requirement.name}
                        required={requirement.required ? true : undefined} 
                        onChange={e => {
                            const newValidationInfos = [...validationInfos];
                            newValidationInfos[i] = e.target.value;
                            setValidationInfos(newValidationInfos);
                        }}
                        style={{ width: '100%', padding: '10px', border: '1px solid #ccc', borderRadius: '4px' }}
                    />
                </div>
            );
        } else if (requirement.type === 'text') {
            return (
                <div style={{ marginBottom: '15px' }} key={i}>
                    <label style={{ display: 'block', marginBottom: '5px' }}>{requirement.label}</label>
                    <input 
                        type="text" 
                        value={validationInfos[i]}
                        name={requirement.name}
                        required={requirement.required ? true : undefined}                         
                        onChange={e => {
                            const newValidationInfos = [...validationInfos];
                            newValidationInfos[i] = e.target.value;
                            setValidationInfos(newValidationInfos);
                        }}
                        style={{ width: '100%', padding: '10px', border: '1px solid #ccc', borderRadius: '4px' }}
                    />
                </div>
            );
        } else if (requirement.type === 'file') {
            return (
                <div style={{ marginBottom: '15px' }} key={i}>
                    <label style={{ display: 'block', marginBottom: '5px' }}>{requirement.label}</label>
                    <input 
                        type="file"
                        name={requirement.name}
                        required={requirement.required ? true : undefined}  
                        onChange={e => {
                            const newValidationInfos = [...validationInfos];
                            newValidationInfos[i] = e.target.files[0];
                            setValidationInfos(newValidationInfos);
                        }} 
                        style={{ display: 'block' }}
                    />
                </div>
            );
        }
        return null;
    });
  
    const handleSubmit = () => {
        let validationInfoObject = {};
        requirements.forEach((requirement, i) => {
            validationInfoObject[requirement.name] = validationInfos[i];
        });
        onSubmit(validationInfoObject);
    };
  
    return (
        <Modal isOpen={isOpen} onRequestClose={onRequestClose} style={customStyles}>
            <h2 style={{ marginBottom: '20px' }}>Enter Validation Information</h2>
            {inputs}
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