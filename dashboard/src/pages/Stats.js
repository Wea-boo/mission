import React from 'react';
import './Stats.css';
import StatisticsCards from '../Components/StatisticsCards';
const Stats = () => {
  return (
    <div className='statistics-container'>
    <div className="statistics">
    <StatisticsCards />
      <div className="statistics__item--full">BarChart: Employees with the highest number of created demands</div>
      <div className="statistics__item--double">LineChart: Average number of demands per day/week/month</div>
      <div className="statistics__item--full">BarChart: Number of demands by state</div>
      <div className="statistics__item--full">PieChart: Number of demands by type</div>
      <div className="statistics__item--double">LineChart: Trends in number of demands over time</div>
      <div className="statistics__item--full">BarChart: Number of demands by assignee</div>
      <div className="statistics__item--full">BarChart: Number of demands by creator</div>
      <div className="statistics__item--full">BarChart: Employees with the most number of assigned demands</div>
    </div>
    </div>
  );
};

export default Stats;