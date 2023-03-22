import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    Colors,
} from 'chart.js';

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    Colors
);

const line_chart_reformat_data = (json_data, x_param, y_param_list) => {
    const datasets = []

    for (let y_param of y_param_list) {
        datasets.push({
            label: y_param,
            data: json_data.map(entry => entry[y_param]),
            fill: false,
        })
    }

    return {
        labels: json_data.map(entry => entry[x_param]),
        datasets
    };
}

export {  line_chart_reformat_data };