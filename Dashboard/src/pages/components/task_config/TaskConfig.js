import React, {useEffect, useState} from 'react';
import axios from 'axios';

import apis from '../../../util/apis';
import {update_interval, using_fake_data} from '../../../util/config';
import fake_data from '../../../util/fake_data';
import TaskParam from './TaskParam';
import TaskEnv from './TaskEnv';
import TaskTrigger from './TaskTrigger';
import TaskReset from './TaskReset';

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

                console.log('Updated task config');
                set_task_config(response);
            } catch (err) {
                console.error(err);
            }
        };

        update_task_config().then();
    }, [])

    const update_config = (config) => {
        config = JSON.parse(JSON.stringify(config))

        if (using_fake_data) {
            set_task_config({...config});
            return;
        }

        axios.post(apis.post_task_config, config)
            .then(response => {
                console.log(response.data);
                set_task_config({...config})
            })
            .catch(error => {
                console.log(error);
            });
    };

    return (
        task_config && <div className='task-config'>
            <h2 className='home-subtitle'>Task Config</h2>
            <div className='task-config__area'>
                <TaskParam init_config={task_config} update_config={update_config}/>
                <TaskEnv init_config={task_config} update_config={update_config}/>
                <TaskTrigger init_config={task_config} update_config={update_config}/>
                <TaskReset update_config={update_config}/>
            </div>
        </div>
    );
}

export default React.memo(TaskConfig);