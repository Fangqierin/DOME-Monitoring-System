import React, { useEffect, useState } from 'react';
import Plotly from 'react-plotly.js';

const WayPointGraph = ({way_points, title}) => {
    const[params, setParams] = useState({
        data: [],
        layout: {}
    });

    useEffect(() => {
        if(!way_points || way_points.length === 0) return;

        const x = way_points.map(p => Number(p.x));
        const y = way_points.map(p => Number(p.y));
        const z = way_points.map(p => Number(p.z));
        const lastPointIndex = way_points.length - 1;

        const trace = {
            type: 'scatter3d',
            mode: 'lines+markers',
            x: x,
            y: y,
            z: z,
            marker: {
                color: ['#55efc4', ...Array(lastPointIndex - 1).fill('#74b9ff'), '#55efc4'],
                size: 10,
                symbol: 'circle'
            }
        };
        const layout = {
            width: 640,
            height: 640,
            // title: 'Flight Path',
            scene: {
                xaxis: { range: [0, 200] },
                yaxis: { range: [0, 200] },
                zaxis: { range: [0, 200] }
            },
            title: {
                text: title,
                font: {
                    size: 20
                },
                yref: 'paper',
                automargin: true,
            }
        };
        const data = [trace];
        setParams({ data, layout });

        console.log('Generated way point graph');
    }, [title, way_points]);

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

export default React.memo(WayPointGraph);