import React, {useEffect} from 'react';

import { using_fake_data } from '../../../util/config';
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
                    response = fake_data.grids;
                } else {
                    response = await fetch(`${apis.get_data}?collection_name=way_points`);
                    response = await response.json();
                    response = response.result;
                    console.log(response)
                }
                set_way_points(response);

                console.log('Updated way points');
            } catch (err) {
                console.error(err);
            }
        };

        update_way_points().then(() => console.log('Initialized way points.'));

        const intervalId = setInterval(update_way_points, 10000);
        return () => clearInterval(intervalId);
    }, []);

    if(!way_points) return (<></>);

    return <>
        <h2 className="home-subtitle">Flight Path</h2>
        <div className='chart-area' onDoubleClick={() => window.open('/chart/way_points', '_blank')}>
            <WayPointGraph way_points={way_points}/>
        </div>

    </>
}

export default FlightPath;