import React, { useEffect, useState } from 'react';
import { Pie } from 'react-chartjs-2';
import axios from 'axios';
import { Chart } from 'chart.js';
import { ArcElement, CategoryScale, Legend, Title, Tooltip } from 'chart.js';

// Register the elements
Chart.register(ArcElement, CategoryScale, Legend, Title, Tooltip);

const COLORS = ['rgba(75, 192, 192, 0.6)', 'rgba(54, 162, 235, 0.6)', 'rgba(255, 206, 86, 0.6)', 'rgba(231, 233, 237, 0.6)', 'rgba(75, 192, 192, 0.4)', 'rgba(153, 102, 255, 0.2)'];

const MissionTypePieChart = () => {
  const [chartData, setChartData] = useState(null);

  useEffect(() => {
    const fetchChartData = async () => {
      try {
        const response = await axios.get("http://localhost:8000/api/number-by-mission-type/");
        const labels = response.data.map(item => item.mission_type__name);
        const data = response.data.map(item => item.mission_count);
        setChartData({
          labels: labels,
          datasets: [
            {
              data: data,
              backgroundColor: COLORS,
              hoverBackgroundColor: COLORS,
            },
          ],
        });
      } catch (error) {
        console.error('Error fetching chart data:', error);
      }
    };

    fetchChartData();
  }, []);

  return (
    <div style={{height: '100%', width: '100%'}}>
      {chartData && <Pie data={chartData} options={{ responsive: true, maintainAspectRatio: false }} />}
    </div>
  );
};

export default MissionTypePieChart;
