import React from "react";

import ChartModule from "./components/ChartModule";
import AirQualityChart from "./components/AirQualityChart";
import WeatherParamChart from "./components/WeatherParamChart";
import GridChart from './components/GridChart';
import LivePreview from './components/LivePreview';

import "../style/Home.scss"

const Home = () => {
    return (
        <div className='home'>
            <h1 className='home-title'>Dome Dashboard</h1>

            <div className='chart-area'>
                <ChartModule chart={<AirQualityChart/>} title='Air Quality' detail_link='/chart/air_qualities'/>
                <ChartModule chart={<WeatherParamChart/>} title='Weather Parameters' detail_link='/chart/weather_params'/>
                <ChartModule chart={<GridChart/>} title='Fire Grid' detail_link='/chart/grids'/>
                <ChartModule chart={<LivePreview/>} title='Live Preview' detail_link='/chart/live_preview'/>
            </div>
        </div>
    );
}

export default Home;