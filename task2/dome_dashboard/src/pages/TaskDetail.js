import FirePreview from './components/fire_status/FirePreview';
import TaskConfig from './components/task_config/TaskConfig';

import '../style/TaskDetail.scss';

const TaskDetail = () => {
    return (
        <div className='Task-detail'>
            <FirePreview/>
            <TaskConfig/>
        </div>
    );
}

export default TaskDetail;