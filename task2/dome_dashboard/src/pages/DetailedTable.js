import { useParams } from 'react-router-dom';

import fake_data from '../util/fake_data';

import '../style/Table.scss';
import {using_fake_data} from '../util/config';
import apis from '../util/apis';
import {useEffect, useState} from 'react';

const DetailedTable = () =>{
    const { name } = useParams();
    const [data, set_data] = useState(undefined);


    useEffect(() => {
        const update_data = async () => {
            try {
                let response;
                if (using_fake_data) {
                    response = fake_data[name];
                } else {
                    if(name === 'waypoints') {
                        response = await fetch(apis.get_grids);
                        response = await response.json();
                        response = response.result.map(entry => JSON.parse(entry.data).location);
                    }else {
                        response = await fetch(`${apis.get_data}?collection_name=${name}`);
                        response = await response.json();
                        response = response.result.map(entry => JSON.parse(entry.data));
                    }
                }
                set_data(response);

                console.log('Updated data');
            } catch (err) {
                console.error(err);
            }
        }

        update_data().then(() => console.log('Initialized table.'));
    }, [name]);

    if(!data) return <div>Invalid url</div>
    const titles = Object.keys(data[0]).filter(title => title !== '_id')

    return <table className="table">
        <thead>
            <tr>
                {
                    titles.map(title =>
                        <th key={`table_head_${title}`}>{ title }</th>
                    )
                }
            </tr>
        </thead>

        <tbody>
            {
                data.map((entry, i) =>
                    <tr key={`table_row_${i}`}>
                        {
                            titles.map((title, j) =>
                                <td key={`table_content_${i}_${j}`}>{ entry[title] }</td>
                            )
                        }
                    </tr>
                )
            }
        </tbody>
    </table>
}


export default DetailedTable;