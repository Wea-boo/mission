import React, { useState, useEffect } from 'react';
import axios from 'axios';
import CountUp from 'react-countup';
import './StatisticsCard.css'
import '../pages/Stats.css'

const StatisticsCards = () => {
    const [stats, setStats] = useState({
        totalDemands: 0,
        avgDemands: 0,
        activeUsers: 0,
        totalUsers: 0
    });

    const [totalTimeFrame, setTotalTimeFrame] = useState('all');
    const [avgTimeFrame, setAvgTimeFrame] = useState('day');

    const fetchTotalDemands = async (timeFrame) => {
        const response = await axios.get(`http://localhost:8000/api/total_demands_${timeFrame}/`);
        return response.data.total;  // Assuming 'totalDemands' is the property you need
    };
    
    const fetchAvgDemands = async (timeFrame) => {
        const response = await axios.get(`http://localhost:8000/api/avg_demands_${timeFrame}/`);
        return response.data.average.avg__avg;  // Assuming 'avgDemands' is the property you need
    };

    const fetchActiveUsers = async () => {
        const response = await axios.get('http://localhost:8000/api/active_users/'); // Placeholder
        return response.data.count; // Placeholder
    };

    const fetchTotalUsers = async () => {
        const response = await axios.get('http://localhost:8000/api/total_users/'); // Placeholder
        return response.data.count; // Placeholder
    };

    useEffect(() => {
        const fetchData = async () => {
            const totalDemands = await fetchTotalDemands(totalTimeFrame);
            const avgDemands = await fetchAvgDemands(avgTimeFrame);
            const activeUsers = await fetchActiveUsers();
            const totalUsers = await fetchTotalUsers();

            setStats({
                totalDemands: totalDemands,
                avgDemands: avgDemands,
                activeUsers: activeUsers,
                totalUsers: totalUsers
            });
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
        <div className="statistics__cards">
            <div className="statistics__card">
                <div className="statistics__card-content">
                    <h3>Total demands</h3>
                    <div className="statistics__card-content__select-wrapper">
                        <select onChange={handleTotalTimeFrameChange}>
                            <option value="all">All time</option>
                            <option value="year">This year</option>
                            <option value="month">This month</option>
                            <option value="week">This week</option>
                        </select>
                    </div>
                    <p className="statistics__card-content__countup"><CountUp end={stats.totalDemands} /></p>
                </div>
            </div>
            <div className="statistics__card">
                <div className="statistics__card-content">
                    <h3>Average demands</h3>
                    <div className="statistics__card-content__select-wrapper">
                        <select onChange={handleAvgTimeFrameChange}>
                            <option value="day">Per day</option>
                            <option value="week">Per week</option>
                            <option value="month">Per month</option>
                        </select>
                    </div>
                    <p className="statistics__card-content__countup"><CountUp end={stats.avgDemands} decimals={2} /></p>
                </div>
            </div>
            <div className="statistics__card">
                <div className="statistics__card-content">
                    <h3>Active users</h3>
                    <p className="statistics__card-content__countup"><CountUp end={stats.activeUsers} /></p>
                </div>
            </div>
            <div className="statistics__card">
                <div className="statistics__card-content">
                    <h3>Total users</h3>
                    <p className="statistics__card-content__countup"><CountUp end={stats.totalUsers} /></p>
                </div>
            </div>
        </div>
    );
};

export default StatisticsCards;