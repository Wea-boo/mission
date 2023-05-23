import React from 'react';
import './Stats.css';
import StatisticsCards from '../Components/StatisticsCards';
import TopEmployeeDemands from '../Components/TopEmployeeDemands';
import MissionTypePieChart from '../Components/MissionTypePieChart';


const Stats = () => {
    return (
        <div className="statistics">
            <div className="statistics__row">
                <StatisticsCards />
            </div>
            <div className="statistics__row statistics__charts">
                <div className="chart__container">
                    <TopEmployeeDemands />
                </div>
                <div className="chart__container">
                    <MissionTypePieChart />
                </div>
            </div>
        </div>
    );
};

export default Stats;
