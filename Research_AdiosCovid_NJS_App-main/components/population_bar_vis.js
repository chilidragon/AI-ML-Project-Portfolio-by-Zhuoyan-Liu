import React, { useState, useEffect } from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Bar } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

const options = {
  plugins: {
    title: {
      display: true,
      text: 'Latino vs. Total Population in Eastern Washington',
      padding: {
        top: 10,
        bottom: 10
      },
      font: {
        size: 24,
        family: 'Roboto',
        weight: 'bold'
      },
      color: "black"
    },
  },
  labels: {
    color: "black"
  },
  responsive: true,
  maintainAspectRatio: false,
  interaction: {
    mode: 'index',
    intersect: true,
  },
  scales: {
    x: {
      stacked: true,
    },
    y: {
      stacked: true,
      ticks: {
        font: {
            size: 10,
        }
      }
    },
  },
  indexAxis: 'y',
}

function  PopulationBarChart() {
  const [data, setData] = useState([]);
  const [errorMessage, setErrorMessage] = useState('');
  useEffect(() => {
    async function fetchData() {
      try {
        const res = await fetch('https://rprwae53w2.execute-api.us-west-2.amazonaws.com/v-1/latino-populations')
        const json = await res.json()
        setData(json.data);
      } catch (error) {
        setErrorMessage('Error fetching data');
      }
    }
    fetchData();
  }, []);
    var county = [];
    var totalPopulation = [];
    var latinoPopulation = [];
    for (let i = 0; i < data.length; i++) {
        county.push(data[i].County);
        totalPopulation.push(data[i].Pop_Estimate);
        latinoPopulation.push(data[i].Estimated_Latino_Pop);
    }
    if (errorMessage) {
      return <div>{errorMessage}</div>;
    }

  const pop = {
      labels: county,
      datasets: [
        {
          axis: 'y',
          label: 'Total Population',
          data: totalPopulation,
          backgroundColor: 'rgb(237, 231, 45)',
          stack: 'Stack 0',
        },
        {
          axis: 'y',
          label: 'Latino Population',
          data: latinoPopulation,
          backgroundColor: 'rgb(245, 122, 122)',
          stack: 'Stack 0',
        }
      ],
    };

    return(<div class='pop_viz'>
            <Bar options={options} data={pop} />
          </div>
    );
}

export default PopulationBarChart;