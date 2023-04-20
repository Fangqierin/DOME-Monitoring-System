import React, {useEffect} from 'react';

import fake_data from '../../../util/fake_data'
import {update_interval, using_fake_data} from '../../../util/config';
import apis from '../../../util/apis';
import FireCanvas from './FireCanvas';
import FireGrids from './FireGrids';
import FireTasks from './FireTasks';
import FireEAT from './FireEAT';

const FirePreview = () => {
    const [grids, set_grids] = React.useState(undefined);
    const [processed_data, set_processed_data] = React.useState(undefined);

    useEffect(() => {
        const update_grids = async () => {
            try {
                let response;
                if (using_fake_data) {
                    response = fake_data.grids;

                    set_grids(response);
                } else {
                    response = await fetch(apis.get_grids);
                    response = await response.json();
                    response = response.result.map(entry => JSON.parse(entry.data));

                    set_grids(response);
                }
            } catch (err) {
                console.error(err);
            }
        };

        const update_processed_data = async () => {
            try {
                let response;
                if (using_fake_data) {
                    response = fake_data.processed_data;

                    set_processed_data(response);
                } else {
                    response = await fetch(apis.get_processed_data);
                    response = await response.json();
                    response = response.result;

                    set_processed_data(response);
                }
            } catch (err) {
                console.error(err);
            }
        };

        update_grids().then(() => console.log('Initialized fire_status.'));
        update_processed_data().then(() => console.log('Initialized processed_data.'));

        const intervalId = setInterval(update_grids, update_interval);
        return () => clearInterval(intervalId);
    }, []);

    if (!grids) return (<></>);

    return (
        <>
            <h2 className="home-subtitle">Fire Status</h2>
            <div className='grid-area'>
                {
                    grids && <FireCanvas grids={grids}/>
                }
                {
                    processed_data && (
                        <>
                            <FireGrids grids={processed_data.grids}/>
                            <FireTasks tasks={processed_data.tasks}/>
                            <FireEAT grids={processed_data.estimated_fire_arrival_time}/>
                        </>
                    )
                }

            </div>
        </>
    );
}

export default FirePreview;