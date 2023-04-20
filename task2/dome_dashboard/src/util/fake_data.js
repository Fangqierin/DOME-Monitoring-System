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
                z: 100,
                read: 0
            },
            {
                time_stamp: '10:23:22',
                x: 0,
                y: -25,
                z: 100,
                read: 0
            },
            {
                time_stamp: '10:23:22',
                x: 0,
                y: -25,
                z: 40,
                read: 0
            }
        ],
        grids: [
            {
                "location": {"x": -50, "y": 25, "z": 110},
                "fires": [{"fx": -68, "fy": 16, "fw": 4, "fh": 2}, {"fx": -68, "fy": 33, "fw": 3, "fh": 2}, {
                    "fx": -55,
                    "fy": 48,
                    "fw": 5,
                    "fh": 10
                }, {"fx": -27, "fy": 31, "fw": 3, "fh": 3}],
                "time": "21:53:28"
            }
        ],
        processed_data:
            {
                "grids": [[0, 0, 1], [0, 1, 0], [0, 1, 0], [0, 0, 0]],
                "estimated_fire_arrival_time":
                    [
                        [0, 6, 9],
                        [0, 6, 6],
                        [0, 6, 6],
                        [3, 3, 6]
                    ],
                "tasks": [
                    {
                        "x": 3,
                        "y": 2,
                        "task": {
                            "FI": [
                                0,
                                -1
                            ]
                        }
                    },
                    {
                        "x": 3,
                        "y": 1,
                        "task": {
                            "FI": [
                                0,
                                -1
                            ]
                        }
                    },
                    {
                        "x": 3,
                        "y": 0,
                        "task": {
                            "FI": [
                                0,
                                -1
                            ]
                        }
                    },
                    {
                        "x": 2,
                        "y": 2,
                        "task": {
                            "FI": [
                                0,
                                -1
                            ]
                        }
                    },
                    {
                        "x": 2,
                        "y": 1,
                        "task": {
                            "FI": [
                                0,
                                -1
                            ]
                        }
                    },
                    {
                        "x": 2,
                        "y": 0,
                        "task": {
                            "FI": [
                                0,
                                -1
                            ]
                        }
                    },
                    {
                        "x": 1,
                        "y": 2,
                        "task": {
                            "BM": [
                                0,
                                -1
                            ]
                        }
                    },
                    {
                        "x": 1,
                        "y": 1,
                        "task": {
                            "FI": [
                                0,
                                -1
                            ]
                        }
                    },
                    {
                        "x": 1,
                        "y": 0,
                        "task": {
                            "FI": [
                                0,
                                -1
                            ]
                        }
                    },
                    {
                        "x": 0,
                        "y": 2,
                        "task": {
                            "FT": [
                                0,
                                -1
                            ]
                        }
                    },
                    {
                        "x": 0,
                        "y": 1,
                        "task": {
                            "FI": [
                                0,
                                -1
                            ]
                        }
                    },
                    {
                        "x": 0,
                        "y": 0,
                        "task": {
                            "FT": [
                                0,
                                -1
                            ]
                        }
                    }
                ]
            },
        task_config: {
            param: {
                BM: [1, 1],
                FD:[0.5, 1],
                FI:[0.5, 1],
                FT:[1, 1]
            }
        }
    }
;

export default fake_data;