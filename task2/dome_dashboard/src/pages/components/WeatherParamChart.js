import fake_data from "../../util/fake_data";
import React, { useState } from "react";
import { line_chart_reformat_data } from "../../util/data_reformat";
import { Line } from 'react-chartjs-2';


const WeatherParamChart = () => {
    const [data, setData] = useState(
        line_chart_reformat_data(fake_data.weather_params,"time_stamp", {"wind": "Wind", "rain": "Rain", "temperature": "Temperature"})
    )

    return <Line data={data} />
}

export default WeatherParamChart;