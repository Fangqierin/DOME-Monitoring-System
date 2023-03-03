const fake_data = {
    air_qualities: [
        {
            device_id: 22,
            time_stamp: '10:23:22',
            pm_2_5: 11.2,
            pm_10: 50
        },
        {
            device_id: 22,
            time_stamp: '10:23:23',
            pm_2_5: 18.2,
            pm_10: 80.2
        },
        {
            device_id: 22,
            time_stamp: '10:23:24',
            pm_2_5: 32,
            pm_10: 20
        }
    ],
    weather_params: [
        {
            device_id: 33,
            time_stamp: '10:23:22',
            temperature: 54,
            humidity: 21.38,
            dew_point: 18.18,
            light: 95.14,
            pressure: 956.6,
            wind: 0.9,
            rain: 0
        },
        {
            device_id: 33,
            time_stamp: '10:23:23',
            temperature: 32.11,
            humidity: 21.38,
            dew_point: 18.18,
            light: 95.14,
            pressure: 956.6,
            wind: 22,
            rain: 0
        },
        {
            device_id: 33,
            time_stamp: '10:23:24',
            temperature: 62,
            humidity: 21.38,
            dew_point: 18.18,
            light: 95.14,
            pressure: 956.6,
            wind: 3,
            rain: 0
        }
    ],
    way_points: [
        {
            time_stamp: '10:23:22',
            x_axis: 0,
            y_axis: -25,
            z_axis: 100
        },
        {
            time_stamp: '10:23:22',
            x_axis: 0,
            y_axis: -25,
            z_axis: 100
        },
        {
            time_stamp: '10:23:22',
            x_axis: 0,
            y_axis: -25,
            z_axis: 100
        }
    ],
    grids: []
}

// Generate random grid
const row_l = 6, col_l = 8;
for(let i = 0; i < row_l; i++){
    const row = []
    for(let j = 0; j < col_l; j++){
        row.push(Math.random() < 0.5 ? -1 : 1)
    }
    fake_data.grids.push(row)
}

export default fake_data;