import React, {useEffect, useState} from 'react';
import apis from '../../../util/apis';
import classNames from 'classnames';

const PreviewImage = ({ filename, at_edge }) =>{
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
        imageUrl && <img className={classNames('live-preview__img', at_edge && 'live-preview__img--smaller')} src={ imageUrl } key={ imageUrl } alt='Preview unavailable'/>
    );
}

export default React.memo(PreviewImage);