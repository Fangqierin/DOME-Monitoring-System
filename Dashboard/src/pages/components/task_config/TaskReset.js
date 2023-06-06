import React from 'react';

import fake_data from '../../../util/fake_data';
import RefreshBtn from '../icons/RefreshBtn';

function TaskReset({ update_config }) {
    const handleReset = () => {
        update_config(fake_data.task_config);
    };

    return (
        <div className="task-reset" onClick={ handleReset }>
            <RefreshBtn/>
        </div>
    );
}

export default React.memo(TaskReset);