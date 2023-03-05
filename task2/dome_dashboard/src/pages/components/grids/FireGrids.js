import fake_data from '../../../util/fake_data'
import classNames from 'classnames';
import React, {useEffect} from 'react';
import {using_fake_data} from '../../../util/config';
import apis from '../../../util/apis';

const FireGrids = () => {
    const [grids, set_grids] = React.useState(undefined);

    useEffect(() => {
        setInterval(() => {
            if(using_fake_data){
                set_grids(fake_data.grids);
                return;
            }

            fetch(apis.get_grids)
                .then(res => res.json())
                .then(data => {
                    set_grids(JSON.parse(data.result.grids));
                })

            return () => clearInterval();
        }, 10000)
    }, []);

    if(!grids) return (<></>);

    return(
        <>
            <h2 className="home-subtitle">Fire Grids</h2>
            <div className='grid-area'>
                <div className="grid-area__chart">
                    {
                        grids.map((row, i) =>
                            <div className="grid-area__chart__row" key={`grid_row_${i}`}>
                                {
                                    row.map((g, j) =>
                                        <div className={
                                            classNames("grid-area__chart__cell", g > 0 ? "grid-area__chart__cell--on" : "grid-area__chart__cell--off")
                                        } key={`grid_cell_${i}_${j}`}>
                                        </div>
                                    )
                                }
                            </div>
                        )
                    }
                </div>

                <table className='table grid-area__table'>
                    <thead>
                    <tr>
                        <th>Grid</th>
                        <th>Fire</th>
                    </tr>
                    </thead>

                    <tbody>
                    {
                        grids.map((row, i) =>
                            row.map((g, j) =>
                                <tr key={`grid_row_${i}_${j}`}>
                                    <td>{`(${i}, ${j})`}</td>
                                    <td>{g > 0 ? "Yes" : "No"}</td>
                                </tr>
                            )
                        )
                    }
                    </tbody>
                </table>
            </div>
        </>
    );
}

export default FireGrids;