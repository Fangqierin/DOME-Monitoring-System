import React, {useState} from 'react';
import axios from 'axios';
import apis from '../../../util/apis';

function TaskParam({init_config}) {
    const [config, setConfig] = useState({...init_config});

    const handleInputChange = (event, name, index) => {
        let value = parseFloat(event.target.value);
        if (isNaN(value)) {
            value = 0;
        }
        const newConfig = {...config}
        newConfig.param[name][index] = value;
        setConfig(newConfig);
    };

    const handleUpdateConfig = () => {
        axios.post(apis.post_task_config, config)
            .then(response => {
                console.log(response.data);
            })
            .catch(error => {
                console.log(error);
            });
    };

    return (
        <div className='Task-param'>
            <div>
                <label className='Task-param__label'>BM</label>
                <input className='Task-param__input' type="text" step="0.1" value={config.param.BM[0]}
                       onChange={(e) => handleInputChange(e, "BM", 0)}/>
                <input className='Task-param__input' type="text" step="0.1" value={config.param.BM[1]}
                       onChange={(e) => handleInputChange(e, "BM", 1)}/>
            </div>
            <div>
                <label className='Task-param__label'>FD</label>
                <input className='Task-param__input' type="text" step="0.1" value={config.param.FD[0]}
                       onChange={(e) => handleInputChange(e, "FD", 0)}/>
                <input className='Task-param__input' type="text" step="0.1" value={config.param.FD[1]}
                       onChange={(e) => handleInputChange(e, "FD", 1)}/>
            </div>
            <div>
                <label className='Task-param__label'>FI</label>
                <input className='Task-param__input' type="text" step="0.1" value={config.param.FI[0]}
                       onChange={(e) => handleInputChange(e, "FI", 0)}/>
                <input className='Task-param__input' type="text" step="0.1" value={config.param.FI[1]}
                       onChange={(e) => handleInputChange(e, "FI", 1)}/>
            </div>
            <div>
                <label className='Task-param__label'>FT</label>
                <input className='Task-param__input' type="text" step="0.1" value={config.param.FT[0]}
                       onChange={(e) => handleInputChange(e, "FT", 0)}/>
                <input className='Task-param__input' type="text" step="0.1" value={config.param.FT[1]}
                       onChange={(e) => handleInputChange(e, "FT", 1)}/>
            </div>
            <button className='Task-param__button' onClick={handleUpdateConfig}>Update Config</button>
        </div>
    );
}

export default TaskParam;