import React, { useState, useEffect } from 'react';
import './Dashboard.css';
import { Link, useNavigate } from 'react-router-dom';
import FilterServices from '../Services/FilterServices';
import LoadingSpinner from '../Components/LoadingSpinner';

const Dashboard = () => {
  const [filters, setFilters] = useState([]);
  const [loading, setLoading] = useState(true);
  const filterServices = new FilterServices();
  const navigate = useNavigate();

  useEffect(() => {
    const getFilters = async () => {
      setLoading(true);
      try {
        const response = await filterServices.getDashboardFilters();
        console.log(response.data)
        setFilters(response.data);
      } catch (error) {
        console.error(error);
      }
      setLoading(false);
    };

    getFilters();
  }, []);

  const handleFilterClick = (filter) => {
    navigate('/demandes', { state: { filter } });
  };

  if (loading) {
    return <LoadingSpinner />
  }

  return (
    <div className='dashboard'>
      <div className="filter-container">
        {filters.map((filter, index) => (
          <div
            key={index}
            onClick={() => handleFilterClick(filter)}
            className='filter-card'
          >
            {filter.name} ({filter.count})
          </div>
        ))}
      </div>
    </div>
  );
};
export default Dashboard;
