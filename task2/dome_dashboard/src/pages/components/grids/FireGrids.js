import fake_data from '../../../util/fake_data'
import classNames from 'classnames';
import React, {useEffect} from 'react';
import {using_fake_data} from '../../../util/config';
import apis from '../../../util/apis';

const FireGrids = () => {
    const [grids, set_grids] = React.useState(undefined);

    useEffect(() => {
        const update_grids = async () => {
            try {
                let response;
                if (using_fake_data) {
                    response = set_grids(fake_data.grids);
                } else {
                    response = await fetch(apis.get_grids);
                    response = await response.json();
                    console.log(response.result.map(entry => JSON.parse(entry.data)))
                    response = response.result.map(entry => JSON.parse(entry.data));
                
                    let matrix = []
                    for(let i=0; i<4; i++){
                        let row = []
                        for(let j=0; j<4; j++){
                            row.push(0)
                        }
                        matrix.push(row)
                    }

                    for(let entry of response){
                        if(!entry.fires) continue
                        for(let d of entry.fires){
                            matrix[Math.floor(d.fx / 50) + 4][Math.floor(-d.fy / 50) + 4] = 1
                        }
                    }
                    
                    set_grids(matrix);
                }
                

                console.log('Updated grids');
            } catch (err) {
                console.error(err);
            }
        };

        update_grids().then(() => console.log('Initialized grids.'));

        const intervalId = setInterval(update_grids, 10000);
        return () => clearInterval(intervalId);
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