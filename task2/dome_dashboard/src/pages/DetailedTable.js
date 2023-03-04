import { useParams } from 'react-router-dom';

import fake_data from '../util/fake_data';

import '../style/Table.scss';

const DetailedTable = () =>{
    const { name } = useParams();

    const data = fake_data[name];
    if(!data) return <div>Invalid url</div>
    const titles = Object.keys(data[0])

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