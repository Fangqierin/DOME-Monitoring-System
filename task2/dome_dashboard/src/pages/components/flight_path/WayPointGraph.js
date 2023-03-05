import { useEffect, useState } from 'react';
import Plotly from 'react-plotly.js';

const WayPointGraph = ({way_points}) => {
    const[params, setParams] = useState({
        data: [],
        layout: {}
    });

    useEffect(() => {
        const x = way_points.map(p => p.x_axis);
        const y = way_points.map(p => p.y_axis);
        const z = way_points.map(p => p.z_axis);
        const lastPointIndex = way_points.length - 1;

        const trace = {
            type: 'scatter3d',
            mode: 'lines+markers',
            x: x,
            y: y,
            z: z,
            marker: {
                color: [...Array(lastPointIndex).fill('#74b9ff'), '#55efc4'],
                size: 10,
                symbol: 'circle'
            }
        };
        const layout = {
            width: 640,
            height: 640,
            // title: 'Flight Path',
            scene: {
                xaxis: { range: [-100, 100] },
                yaxis: { range: [-100, 100] },
                zaxis: { range: [-100, 100] }
            }
        };
        const data = [trace];
        setParams({ data, layout });

        console.log('Generated way point graph');
    }, [way_points]);

    return (
        <div>
            <Plotly
                data={params.data}
                layout={params.layout}
                style={{ width: '100%', height: '100%' }}
            />
        </div>
    );
}

export default WayPointGraph;