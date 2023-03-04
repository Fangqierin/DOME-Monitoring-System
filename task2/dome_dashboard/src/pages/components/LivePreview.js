import preview1 from '../sources/preview1.jpg'
import preview2 from '../sources/preview2.jpg'
import preview3 from '../sources/preview3.jpg'
import React from 'react';

const LivePreview = () => {
    // TODO: fetch live preview images from server

    return (
        <>
            <h2 className="home-subtitle">Live Previews</h2>
            <div className='live-preview'>
                <img className='live-preview__img' src={preview1} alt='Live preview unavailable'/>
                <img className='live-preview__img' src={preview2} alt='Live preview unavailable'/>
                <img className='live-preview__img' src={preview3} alt='Live preview unavailable'/>
            </div>
        </>

    )
}


export default LivePreview;