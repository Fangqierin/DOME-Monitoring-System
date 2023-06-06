import AirQualityChart from './AirQualityChart';
import WeatherParamChart from './WeatherParamChart';
import React, {useEffect} from 'react';
import apis from '../../../util/apis';
import {update_interval, using_fake_data} from '../../../util/config';
import fake_data from '../../../util/fake_data';

const ChartArea = () =>{
    const [data_param, set_data_param] = React.useState({
        air_qualities: undefined,
        weather_params: undefined,
    });

    useEffect(() => {
        const update_data = async () => {
            try {
                let new_data_param = {};
                if (using_fake_data) {
                    new_data_param = {
                        air_qualities: fake_data.air,
                        weather_params: fake_data.weather,
                    };
                } else {
                    let res = await fetch(`${apis.get_data}?collection_name=weather`);
                    let data = await res.json();
                    new_data_param.weather_params = data.result.map(entry => JSON.parse(entry.data))
                    new_data_param.weather_params.sort(
                        (a, b) => {
                            const [aH, aM, as] = a.timestamp.split(":")
                            const [bH, bM, bs] = b.timestamp.split(":")

                            return (aH - bH) || (aM - bM) || (as - bs)
                        }
                    );

                    res = await fetch(`${apis.get_data}?collection_name=air`);
                    data = await res.json();
                    new_data_param.air_qualities = data.result.map(entry => JSON.parse(entry.data));
                    new_data_param.air_qualities = new_data_param.air_qualities.sort(
                        (a, b) => {
                            const [aH, aM, as] = a.timestamp.split(":")
                            const [bH, bM, bs] = b.timestamp.split(":")

                            return (aH - bH) || (aM - bM) || (as - bs)
                        }
                    );
                }
                set_data_param(new_data_param);

                console.log('Updated charts');
            } catch (err) {
                console.error(err);
            }
        };

        update_data().then(() => console.log('Initialized charts.'));

        const intervalId = setInterval(update_data, update_interval);
        return () => clearInterval(intervalId);
    }, []);

    return (
        <>
            <h2 className="home-subtitle">Status</h2>
            <AirQualityChart air_qualities={data_param.air_qualities}/>
            <WeatherParamChart weather_params={data_param.weather_params}/>
        </>
    )
}

export default React.memo(ChartArea);