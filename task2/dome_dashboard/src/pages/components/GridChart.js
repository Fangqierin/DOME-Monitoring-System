import fake_data from '../../util/fake_data'
import classNames from 'classnames';

const GridChart = () =>
    <div className="grid-chart">
        {
            fake_data.grids.map((row, i) =>
                <div className="grid-chart__row" key={`grid_row_${i}`}>
                    {
                        row.map((g, j) =>
                            <div className={
                                classNames("grid-chart__cell", g > 0 ? "grid-chart__cell--on" : "grid-chart__cell--off")
                            } key={`grid_cell_${i}_${j}`}>
                                ({i}, {j})
                            </div>
                        )
                    }
                </div>
            )
        }
    </div>

export default GridChart;