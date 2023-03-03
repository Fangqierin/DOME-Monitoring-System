const ChartModule = ({ chart, title, detail_link }) =>
    <div className='chart-area__module'>
        <div className='chart-area__module__title'>{ title }</div>
        <div className='chart-area__module__chart'>{ chart }</div>
        <a className='chart-area__module__link' href={ detail_link } target='_blank' rel='noreferrer'>Detail</a>
    </div>

export default ChartModule;