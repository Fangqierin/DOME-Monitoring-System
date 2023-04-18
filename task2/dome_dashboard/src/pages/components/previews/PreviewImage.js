import React, {useEffect, useState} from 'react';
import apis from '../../../util/apis';

const PreviewImage = ({ filename }) =>{
    const [imageUrl, setImageUrl] = useState('');

    useEffect(() => {
        const getImage = async () => {
            const response = await fetch(`${apis.get_image}${filename}`);
            const blob = await response.blob();
            const url = URL.createObjectURL(blob);
            setImageUrl(url);
        };

        getImage().then(_ => console.log(filename + ' loaded.'));
    }, [filename]);

    return (
        imageUrl && <img className='live-preview__img' src={ imageUrl } alt='Preview unavailable'/>
    );
}

export default PreviewImage;