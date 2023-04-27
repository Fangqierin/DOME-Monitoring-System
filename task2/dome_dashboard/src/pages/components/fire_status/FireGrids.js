import React, {useEffect, useRef} from 'react';

function FireGrids({ grids }) {
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
        ctx.fillText('0', 0, 220);
        ctx.fillText('50', 50, 220);
        ctx.fillText('100', 100, 220);
        ctx.fillText('150', 150, 220);

        ctx.fillText('200', 160, 15);
        ctx.fillText('150', 160, 65);
        ctx.fillText('100', 160, 105);
        ctx.fillText('50', 160, 155);
        ctx.fillText('0', 160, 205);

        // Draw fires
        const cellWidth = 50;
        const cellHeight = 50;

        for (let i = 0; i < grids.length; i++) {
            const row = grids[i];
            for (let j = 0; j < row.length; j++) {
                const cell = row[j];
                if (cell === 1) {
                    const rectX = (j * cellWidth) + 5;
                    const rectY = (i * cellHeight) + 5;
                    ctx.fillStyle = 'red';
                    ctx.fillRect(rectX + 2, rectY + 2, cellWidth - 4, cellHeight - 4);
                }
            }
        }
    }, [grids]);

    return (
        <div className="grid-area__graph">
            <div className="home__module__title">Grids</div>
            <canvas ref={canvasRef} width={200} height={240} />
        </div>
    );
}

export default React.memo(FireGrids);




