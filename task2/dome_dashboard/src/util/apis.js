import { server_url } from './config';

const apis = {
    get_data: server_url + 'get_data',
    get_image: server_url + 'get_image/',
    get_grids: server_url + 'get_grids',
    get_processed_data: server_url + 'processed_data',
    get_waypoints: server_url + 'waypoint?not_drone=true',
    get_task_config: server_url + 'task_config',
    post_task_config: server_url + 'task_config',
};

export default apis;