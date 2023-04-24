import FirePreview from './components/fire_status/FirePreview';
import TaskConfig from './components/task_config/TaskConfig';

import '../style/TaskDetail.scss';
import FlightPath from './components/flight_path/FlightPath';

const TaskDetail = () => {
    return (
        <div className='task-detail'>
            <FirePreview/>
            <TaskConfig/>
            <FlightPath/>
        </div>
    );
}

export default TaskDetail;