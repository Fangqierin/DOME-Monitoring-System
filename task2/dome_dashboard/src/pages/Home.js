import React from "react";

import FirePreview from './components/fire_status/FirePreview';
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
            <h1 className='home-title'>DOME Dashboard</h1>

            { 
                <LivePreview/> 
            }
            <FirePreview/>
            <FlightPath/>

            <ChartArea/>
        </div>
    );
}

export default Home;