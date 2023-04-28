import React, {useEffect, useState} from 'react';

function TaskParam({init_config, update_config}) {
    const [config, setConfig] = useState({...init_config});

    useEffect(() => {
            setConfig({...init_config});
        },
        // eslint-disable-next-line react-hooks/exhaustive-deps
        [init_config]);
    const handleInputChange = (event, name, index) => {
        let value = event.target.value;
        if (isNaN(value)) {
            value = 0;
        }
        const newConfig = {...config}
        newConfig.param[name][index] = value;
        setConfig(newConfig);
    };

    return (
        <div className='task-config__area__module task-param'>
            <div>
                <label className='task-param__label'>BM</label>
                <input className='task-param__input' type="text" step="0.1" value={config.param.BM[0]}
                       onChange={(e) => handleInputChange(e, "BM", 0)}/>
                <input className='task-param__input' type="text" step="0.1" value={config.param.BM[1]}
                       onChange={(e) => handleInputChange(e, "BM", 1)}/>
            </div>
            <div>
                <label className='task-param__label'>FD</label>
                <input className='task-param__input' type="text" step="0.1" value={config.param.FD[0]}
                       onChange={(e) => handleInputChange(e, "FD", 0)}/>
                <input className='task-param__input' type="text" step="0.1" value={config.param.FD[1]}
                       onChange={(e) => handleInputChange(e, "FD", 1)}/>
            </div>
            <div>
                <label className='task-param__label'>FI</label>
                <input className='task-param__input' type="text" step="0.1" value={config.param.FI[0]}
                       onChange={(e) => handleInputChange(e, "FI", 0)}/>
                <input className='task-param__input' type="text" step="0.1" value={config.param.FI[1]}
                       onChange={(e) => handleInputChange(e, "FI", 1)}/>
            </div>
            <div>
                <label className='task-param__label'>FT</label>
                <input className='task-param__input' type="text" step="0.1" value={config.param.FT[0]}
                       onChange={(e) => handleInputChange(e, "FT", 0)}/>
                <input className='task-param__input' type="text" step="0.1" value={config.param.FT[1]}
                       onChange={(e) => handleInputChange(e, "FT", 1)}/>
            </div>
            <button className='task-param__button' onClick={() => update_config(config)}>Update Config</button>
        </div>
    );
}

export default React.memo(TaskParam);