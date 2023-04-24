import React, {useEffect, useState} from 'react';
import apis from '../../../util/apis';
import {update_interval} from '../../../util/config';

import {using_fake_data} from '../../../util/config';
import fake_data from '../../../util/fake_data';
import TaskParam from './TaskParam';

const TaskConfig = () => {
    const [task_config, set_task_config] = useState(undefined);

    useEffect(() => {
        if (using_fake_data) {
            set_task_config(fake_data.task_config)
        }

        const update_task_config = async () => {
            try {
                let response = await fetch(apis.get_task_config);
                response = await response.json();
                response = response.result;
                delete response._id
                set_task_config(response);

                console.log('Updated task config');
            } catch (err) {
                console.error(err);
            }
        };

        update_task_config().then();

        const intervalId = setInterval(
            () => {
                update_task_config().then(() => console.log('Initialized flightpath.'));
            }, update_interval
        );
        return () => clearInterval(intervalId);
    }, [])

    return (
        task_config && <div>
            <h2 className='home-subtitle'>Task Config</h2>
            <TaskParam init_config={task_config}/>
        </div>
    );
}

export default React.memo(TaskConfig);