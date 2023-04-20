const ChartModule = ({ chart, title }) =>
    <div className='chart-area__module'>
        <div className='home__module__title'>{ title }</div>
        <div className='chart-area__module__chart'>{ chart }</div>
    </div>

export default ChartModule;