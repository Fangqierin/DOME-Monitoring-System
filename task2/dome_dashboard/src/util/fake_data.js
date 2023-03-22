const fake_data = {
    air: [
        {
            timestamp: "10:23:26",
            "pm2.5": 11,
            "pm10": 45
        },
        {
            timestamp: "10:23:27",
            "pm2.5": 11,
            "pm10": 45
        },
        {
            timestamp: "10:23:28",
            "pm2.5": 11,
            "pm10": 45
        }
    ],
    weather: [
        {
            timestamp: "10:23:26",
            temperature: 21,
            humidity: 21.38,
            dew_point: 18.18,
            light: 95.14,
            pressure: 956.6,
            wind_speed: 54,
            rain: 0
        },
        {
            timestamp: "10:23:27",
            temperature: 23,
            humidity: 21.38,
            dew_point: 18.18,
            light: 95.14,
            pressure: 956.6,
            wind_speed: 21,
            rain: 23
        },
        {
            timestamp: "10:23:28",
            temperature: 52,
            humidity: 21.38,
            dew_point: 18.18,
            light: 95.14,
            pressure: 956.6,
            wind_speed: 54,
            rain: 12
        }
    ],
    waypoints: [
        {
            time_stamp: '10:23:22',
            x: 0,
            y: 25,
            z: 100
        },
        {
            time_stamp: '10:23:22',
            x: 0,
            y: -25,
            z: 100
        },
        {
            time_stamp: '10:23:22',
            x: 0,
            y: -25,
            z: 40
        }
    ],
    grids: [
        [1, 0, 0, 0],
        [1, 1, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]
};

export default fake_data;