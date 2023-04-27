import FirePreview from './components/fire_status/FirePreview';
import TaskConfig from './components/task_config/TaskConfig';
import FlightPath from './components/flight_path/FlightPath';

import '../style/TaskDetail.scss';

const TaskDetail = () => {
    return (
        <div className='task-detail'>
            <TaskConfig/>
            <FirePreview/>
            <FlightPath/>
        </div>
    );
}

export default TaskDetail;