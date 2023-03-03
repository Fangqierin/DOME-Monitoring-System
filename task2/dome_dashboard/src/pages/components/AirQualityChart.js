import fake_data from "../../util/fake_data";
import { Line } from 'react-chartjs-2';
import React, { useState } from "react";
import { line_chart_reformat_data } from "../../util/data_reformat";

const AirQualityChart = () => {
    const [data, setData] = useState(
        line_chart_reformat_data(fake_data.air_qualities,"time_stamp", {"pm_2_5": "PM 2.5", "pm_10": "PM 10"})
    )

    return <Line data={data} />
}

export default AirQualityChart;