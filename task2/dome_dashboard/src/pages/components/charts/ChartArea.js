import AirQualityChart from './AirQualityChart';
import WeatherParamChart from './WeatherParamChart';
import React from 'react';
import fake_data from '../../../util/fake_data';

const ChartArea = () =>
    <>
        <h2 className="home-subtitle">Status</h2>
        <AirQualityChart air_qualities={fake_data.air_qualities}/>
        <WeatherParamChart weather_params={fake_data.weather_params}/>
    </>

export default ChartArea;