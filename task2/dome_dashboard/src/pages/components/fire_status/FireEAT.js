import React, {useEffect, useRef} from 'react';

function FireEAT({grids}) {
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

        for (let i = 0; i < grids.length; i++) {
            const row = grids[i];
            for (let j = 0; j < row.length; j++) {
                const cell = row[j];
                const rectX = (j * cellWidth) + 5;
                const rectY = (i * cellHeight) + 5;
                ctx.fillStyle = `rgba(255, 0, 0, ${cell < 20 ? (20 - cell) / 20 : 0})`;
                ctx.fillRect(rectX + 2, rectY + 2, cellWidth - 4, cellHeight - 4);
            }
        }

        // Draw legend
        for (let i = 0; i < 20; i++) {
            const opacity = (20 - i) / 20;
            ctx.fillStyle = `rgba(255, 0, 0, ${opacity})`;
            ctx.fillRect(200, 10 + i * 10, 7, 10);
        }
        ctx.fillStyle = 'black';
        ctx.fillText('0s', 220, 20);
        ctx.fillText('20s', 220, 210);
    }, [grids]);

    return (
        <div className="grid-area__graph">
            <div className="home__module__title">Estimated time</div>
            <canvas ref={canvasRef} width={240} height={240}/>
        </div>
    );
}

export default React.memo(FireEAT);