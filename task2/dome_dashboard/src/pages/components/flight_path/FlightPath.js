import React, {useEffect} from 'react';

import {update_interval, using_fake_data} from '../../../util/config';
import fake_data from '../../../util/fake_data';
import apis from '../../../util/apis';

import WayPointGraph from './WayPointGraph';

const FlightPath = () => {
    const [flightpath, set_flightpath] = React.useState(undefined);
    const [waypoints, set_waypoints] = React.useState(undefined);

    useEffect(() => {
        const update_flightpath = async () => {
            try {
                let response;
                if (using_fake_data) {
                    response = fake_data.waypoints;
                } else {
                    response = await fetch(apis.get_grids);
                    response = await response.json();
                    response = response.result.map(entry => JSON.parse(entry.data).location);
                }
                set_flightpath(response);

                console.log('Updated way points');
            } catch (err) {
                console.error(err);
            }
        };

        const update_waypoints = async () => {
            try {
                if (using_fake_data) {
                    set_waypoints(fake_data.waypoints);
                    return;
                }
                let response = await fetch(apis.get_waypoints);
                response = await response.json();
                response = response.map(r => {
                    return {
                        x: r.x * 100 - 100,
                        y: r.y * 100 - 100,
                        z: r.z * 100 - 100,
                    }
                });
                set_waypoints(response);

                console.log('Updated way points');
            } catch (err) {
                console.error(err);
            }
        };

        update_flightpath().then(() => console.log('Initialized flightpath.'));
        update_waypoints().then(() => console.log('Initialized waypoints.'));

        const intervalId = setInterval(
            () => {
                update_flightpath().then(() => console.log('Initialized flightpath.'));
                update_waypoints().then(() => console.log('Initialized waypoints.'));
            }, update_interval
        );
        return () => clearInterval(intervalId);
    }, []);

    return <>
        <h2 className="home-subtitle">Flight Path</h2>
        <div className='chart-area'>
            {flightpath && <WayPointGraph way_points={flightpath} title='Flight Path'/>}
            {waypoints && <WayPointGraph way_points={waypoints} title='Waypoints'/>}
        </div>

    </>
}

export default React.memo(FlightPath);