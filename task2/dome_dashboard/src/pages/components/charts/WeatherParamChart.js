import React from "react";
import { line_chart_reformat_data } from "../../../util/data_reformat";
import { Line } from 'react-chartjs-2';
import ChartModule from './ChartModule';


const WeatherParamChart = ({weather_params}) =>
    weather_params &&
        <div className='chart-area' onClick={() => window.open('/chart/weather', '_blank')}>
            <ChartModule chart={
                <Line data={line_chart_reformat_data(weather_params, "timestamp", ["temperature"])} />
            } title='Temperature'/>
            <ChartModule chart={
                <Line data={line_chart_reformat_data(weather_params, "timestamp", ["wind_speed"])} />
            } title='Wind'/>
            <ChartModule chart={
                <Line data={line_chart_reformat_data(weather_params, "timestamp", ["rain"])} />
            } title='Rain'/>
        </div>


export default React.memo(WeatherParamChart);