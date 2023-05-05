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
import {group} from 'plotly.js/src/plots/frame_attributes';

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
        const grouped_data = {}

        for (let entry of json_data) {
            if (!entry.id) entry.id = "default";
            const id = entry.id;
            if (!grouped_data[id]) grouped_data[id] = [];
            grouped_data[id].push(entry);
        }

        for (let id in grouped_data) {
            const dataset = {
                label: y_param + (id.includes('2') ? ' (2)' : ' (1)'),
                data: (grouped_data[id]).map(entry => entry[y_param]),
                fill: false
            }

            const color = id.includes('2') ? 'rgb(255, 99, 132)' : 'rgb(54, 162, 235)';
            dataset.borderColor = color;
            dataset.backgroundColor = color;

            datasets.push(dataset);
        }
    }

    return {
        labels: json_data.map(entry => entry[x_param]),
        datasets
    };
}

export {  line_chart_reformat_data };