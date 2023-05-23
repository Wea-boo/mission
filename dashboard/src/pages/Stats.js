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
                <div className="statistics__chart-card">
                    <TopEmployeeDemands />
                </div>
                <div className="statistics__chart-card">
                    <MissionTypePieChart />
                </div>
            </div>
        </div>
    );
};

export default Stats;
