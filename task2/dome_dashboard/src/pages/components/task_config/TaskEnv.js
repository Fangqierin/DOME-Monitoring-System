import React, {useEffect, useState} from 'react';

function TaskEnv({ init_config, update_config }) {
    const [config, setConfig] = useState({ ...init_config });

    useEffect(() => {
            setConfig({...init_config});
        },
        // eslint-disable-next-line react-hooks/exhaustive-deps
        [init_config.env]);

    const handleInputChange = (event, name) => {
        let value = parseFloat(event.target.value);
        if (isNaN(value)) {
            value = 0;
        }

        const newValues = { ...config };
        newValues.env[name] = value;
        setConfig(newValues);
    };

    return (
        <div className="task-config__area__module task-env">
            <div>
                <label className="task-env__label">Wind Speed</label>
                <input
                    className="task-env__input"
                    type="text"
                    step="0.1"
                    value={config.env.wind_speed}
                    onChange={(e) => handleInputChange(e, 'wind_speed')}
                />
            </div>
            <div>
                <label className="task-env__label">Plan Time</label>
                <input
                    className="task-env__input"
                    type="text"
                    step="0.1"
                    value={config.env.plan_time}
                    onChange={(e) => handleInputChange(e, 'plan_time')}
                />
            </div>
            <button className="task-env__button" onClick={ () => update_config(config) }>
                Update Values
            </button>
        </div>
    );
}

export default React.memo(TaskEnv);