import React from "react";
import { Link } from "react-router-dom";

const Filter = ({ filterName, subFilters, onSubFilterClick }) => {
  
  const renderSubFilters = () => {
    return subFilters.map((subFilter, index) => (
      <Link 
        key={index} 
        to="/Demandes" 
        className="filter-card" 
        onClick={() => onSubFilterClick()}
      >
        {subFilter}
      </Link>
    ));
  }

  return (
    <div className="filter-container">
      {renderSubFilters()}
    </div>
  );
};

export default Filter;
