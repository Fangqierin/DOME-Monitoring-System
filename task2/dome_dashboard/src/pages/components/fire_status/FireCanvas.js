import React, {useRef, useEffect} from 'react';

function FireCanvas({grids}) {
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
        grids.forEach(grid => {
            const fires = grid.fires;

            fires.forEach(fire => {
                const fx = fire.fx;
                const fy = fire.fy;
                const fw = fire.fw;
                const fh = fire.fh;

                const rectX = (fx) + 5;
                const rectY = ((200 - fy) + 5) - fh; // Subtract fh*yRatio to shift the rectangle up

                ctx.fillStyle = 'red';
                ctx.fillRect(rectX, rectY, fw, fh);
            });
        });
    }, [grids]);

    return (
        <div className={'grid-area__graph'}>
            <div className="home__module__title">Preview</div>
            <canvas ref={canvasRef} width={200} height={240}/>
        </div>
    );
}

export default React.memo(FireCanvas);