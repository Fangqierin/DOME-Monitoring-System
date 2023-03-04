import { Line } from 'react-chartjs-2';
import React from "react";
import { line_chart_reformat_data } from "../../../util/data_reformat";
import ChartModule from './ChartModule';

const AirQualityChart = ({air_qualities}) =>
    <div className='chart-area' onClick={() => window.open('/chart/air_qualities', '_blank')}>
        <ChartModule chart={
            <Line data={line_chart_reformat_data(air_qualities, "time_stamp", ["pm_2_5"])} />
        } title='PM 2.5'/>
        <ChartModule chart={
            <Line data={line_chart_reformat_data(air_qualities, "time_stamp", ["pm_10"])} />
        } title='PM 10'/>
    </div>

export default AirQualityChart;