import React, {useEffect, useState} from 'react';
import apis from '../../../util/apis';

function TaskTrigger({ init_config, update_config }) {
    const [config, setConfig] = useState({...init_config});

    useEffect(() => {
            setConfig({...init_config});
        },
        // eslint-disable-next-line react-hooks/exhaustive-deps
        [init_config.trigger]);
    const handleToggle = () => {
        const newConfig = {...config}
        newConfig.trigger = !newConfig.trigger;
        setConfig(newConfig)
        update_config(newConfig);
    };

    const handleTrigger = () => {
        fetch(apis.get_waypoints_drone).then();
    }

    return (
        <div className="task-config__area__module task-trigger">
            <label className="task-trigger__label">Trigger</label>
            <button className={`task-trigger__button ${config.trigger ? 'on' : 'off'}`} onClick={ handleToggle }>
                {config.trigger ? 'ON' : 'OFF'}
            </button>
            <button className='task-trigger__button task-trigger__button--manual' onClick={() => handleTrigger()}>Manual Trigger</button>
        </div>
    );
}

export default TaskTrigger;
