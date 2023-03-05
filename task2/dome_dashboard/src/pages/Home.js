import React from "react";

import FireGrids from './components/grids/FireGrids';
import LivePreview from './components/previews/LivePreview';
import ChartArea from './components/charts/ChartArea';

import "../style/Home.scss";
import "../style/LivePreview.scss";
import "../style/Grid.scss";
import "../style/Chart.scss";
import FlightPath from './components/flight_path/FlightPath';

const Home = () => {
    return (
        <div className='home'>
            <h1 className='home-title'>Dome Dashboard</h1>

            <LivePreview/>
            <FireGrids/>
            <FlightPath/>

            <ChartArea/>
        </div>
    );
}

export default Home;