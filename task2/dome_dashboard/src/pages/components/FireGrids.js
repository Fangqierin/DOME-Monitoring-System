import fake_data from '../../util/fake_data'
import classNames from 'classnames';
import React from 'react';

const FireGrids = () =>{
    return(
        <>
            <h2 className="home-subtitle">Fire Grids</h2>
            <div className='grid-area'>
                <div className="grid-area__chart">
                    {
                        fake_data.grids.map((row, i) =>
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
                        fake_data.grids.map((row, i) =>
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