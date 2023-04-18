import React, {useEffect} from 'react';

import {update_interval, using_fake_data} from '../../../util/config';
import fake_data from '../../../util/fake_data';
import apis from '../../../util/apis';

import WayPointGraph from './WayPointGraph';

const FlightPath = () => {
    const [way_points, set_way_points] = React.useState(undefined);

    useEffect(() => {
        const update_way_points = async () => {
            try {
                let response;
                if (using_fake_data) {
                    response = fake_data.waypoints;
                } else {
                    response = await fetch(apis.get_grids);
                    response = await response.json();
                    response = response.result.map(entry => JSON.parse(entry.data).location);
                }
                set_way_points(response);

                console.log('Updated way points');
            } catch (err) {
                console.error(err);
            }
        };

        update_way_points().then(() => console.log('Initialized way points.'));

        const intervalId = setInterval(update_way_points, update_interval);
        return () => clearInterval(intervalId);
    }, []);

    if (!way_points) return (<></>);

    return <>
        <h2 className="home-subtitle">Flight Path</h2>
        <div className='chart-area' onDoubleClick={() => window.open('/chart/waypoints', '_blank')}>
            <WayPointGraph way_points={way_points}/>
        </div>

    </>
}

export default FlightPath;