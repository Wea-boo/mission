import React, { useState, useEffect } from 'react';
import axios from 'axios';
import CountUp from 'react-countup';
import './StatisticsCard.css'
import '../pages/Stats.css'
const StatisticsCards = () => {
    const [demandStats, setDemandStats] = useState({
        totalDemands: 0,
        avgDemands: 0
    });

    const [totalTimeFrame, setTotalTimeFrame] = useState('all');
    const [avgTimeFrame, setAvgTimeFrame] = useState('day');

    useEffect(() => {
        const fetchTotalDemands = async (timeFrame) => {
            const response = await axios.get(`http://localhost:8000/api/total_demands_${timeFrame}/`);
            return response.data.total;  // Assuming 'totalDemands' is the property you need
        };
        
        const fetchAvgDemands = async (timeFrame) => {
            const response = await axios.get(`http://localhost:8000/api/avg_demands_${timeFrame}/`);
            return response.data.average.avg__avg;  // Assuming 'avgDemands' is the property you need
        };

        const fetchData = async () => {
            const totalDemands = await fetchTotalDemands(totalTimeFrame);
            const avgDemands = await fetchAvgDemands(avgTimeFrame);

            setDemandStats({
                totalDemands: totalDemands,
                avgDemands: avgDemands
            });
            console.log(totalDemands);
        };

        fetchData();
    }, [totalTimeFrame, avgTimeFrame]);

    const handleTotalTimeFrameChange = (event) => {
        setTotalTimeFrame(event.target.value);
    };

    const handleAvgTimeFrameChange = (event) => {
        setAvgTimeFrame(event.target.value);
    };

    return (
        <div className="statistics__cards statistics__item--double">
            <div className="statistics__card">
                <div className="statistics__card-content">
                    <h3>Total demands</h3>
                    <select onChange={handleTotalTimeFrameChange}>
                        <option value="all">All time</option>
                        <option value="year">This year</option>
                        <option value="month">This month</option>
                        <option value="week">This week</option>
                    </select>
                    <p><CountUp end={demandStats.totalDemands} /></p>
                </div>
            </div>
            <div className="statistics__card">
                <div className="statistics__card-content">
                    <h3>Average demands</h3>
                    <select onChange={handleAvgTimeFrameChange}>
                        <option value="day">Per day</option>
                        <option value="week">Per week</option>
                        <option value="month">Per month</option>
                    </select>
                    <p><CountUp end={demandStats.avgDemands} decimals={2} /></p>
                </div>
            </div>
        </div>
    );
};

export default StatisticsCards;