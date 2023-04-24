import React, {useRef, useEffect} from 'react';

function FireTasks({tasks}) {
    const canvasRef = useRef(null);

    useEffect(() => {
        const canvas = canvasRef.current;
        const ctx = canvas.getContext('2d');
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Draw x and y axes
        ctx.beginPath();
        ctx.moveTo(5, 5);
        ctx.lineTo(155, 5);
        ctx.moveTo(5, 55);
        ctx.lineTo(155, 55);
        ctx.moveTo(5, 105);
        ctx.lineTo(155, 105);
        ctx.moveTo(5, 155);
        ctx.lineTo(155, 155);
        ctx.moveTo(5, 205);
        ctx.lineTo(155, 205);

        ctx.moveTo(5, 5);
        ctx.lineTo(5, 205);
        ctx.moveTo(55, 5);
        ctx.lineTo(55, 205);
        ctx.moveTo(105, 5);
        ctx.lineTo(105, 205);
        ctx.moveTo(155, 5);
        ctx.lineTo(155, 205);
        ctx.strokeStyle = 'black';
        ctx.stroke();

        // Draw axis labels
        ctx.font = '12px sans-serif';
        ctx.fillStyle = 'black';
        ctx.fillText('-75', 0, 220);
        ctx.fillText('-25', 50, 220);
        ctx.fillText('25', 100, 220);
        ctx.fillText('75', 150, 220);

        ctx.fillText('100', 160, 15);
        ctx.fillText('50', 160, 65);
        ctx.fillText('0', 160, 105);
        ctx.fillText('-50', 160, 155);
        ctx.fillText('-100', 160, 205);

        // Draw fires
        const cellWidth = 50;
        const cellHeight = 50;

        // Draw cell tasks
        for (const {x, y, task} of tasks) {
            const rectX = (y * cellWidth) + 5;
            const rectY = (x * cellHeight) + 5;

            ctx.fillStyle = task.hasOwnProperty('BM')
                ? 'blue'
                : (task.hasOwnProperty('FI') ? 'red' : 'green');
            ctx.fillRect(rectX + 2, rectY + 2, cellWidth - 4, cellHeight - 4);
        }

        // Draw legend
        const legendWidth = 30;
        const legendHeight = 15;
        const legendX = 200;
        const legendY = 5;

        // Blue task
        ctx.fillStyle = 'blue';
        ctx.fillRect(legendX, legendY, legendWidth, legendHeight);
        ctx.font = '12px sans-serif';
        ctx.fillStyle = 'black';
        ctx.fillText('BM', legendX + legendWidth + 5, legendY + legendHeight);

        // Red task
        ctx.fillStyle = 'red';
        ctx.fillRect(legendX, legendY + legendHeight + 5, legendWidth, legendHeight);
        ctx.fillText('FI', legendX + legendWidth + 5, legendY + legendHeight * 2 + 5);

        // Green task
        ctx.fillStyle = 'green';
        ctx.fillRect(legendX, legendY + (legendHeight + 5) * 2, legendWidth, legendHeight);
        ctx.fillText('FT', legendX + legendWidth + 5, legendY + legendHeight * 3 + 10);
    }, [tasks]);

    return (
        <div className="grid-area__graph">
            <div className="home__module__title">Tasks</div>
            <canvas ref={canvasRef} width={260} height={240}/>
        </div>
    );
}

export default React.memo(FireTasks);
