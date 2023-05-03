import React, {useEffect, useState} from 'react';
import apis from '../util/apis';

import preview1 from './sources/preview1.jpg';
import preview2 from './sources/preview2.jpg';
import preview3 from './sources/preview3.jpg';
import {update_interval, using_fake_data} from '../util/config';
import PreviewImage from './components/previews/PreviewImage';

import '../style/ImageDetail.scss';
import classNames from 'classnames';

const ImageDetail = () => {
    const [file_names, set_file_names] = useState(undefined);
    const [selectedImage, setSelectedImage] = useState(0);

    useEffect(() => {
        const update_previews = async () => {
            try {
                if (using_fake_data) {
                    set_file_names(['preview1.jpg', 'preview2.jpg', 'preview3.jpg']);
                    return;
                }

                const response = await fetch(apis.get_data + "?collection_name=images");
                const data = await response.json();

                set_file_names(data.result.map(item => item.filename));

                console.log('Updated previews');
            } catch (error) {
                console.error(error);
            }
        };

        update_previews().then(() => console.log('Initialized previews.'));

        const intervalId = setInterval(update_previews, update_interval);
        return () => clearInterval(intervalId);
    }, []);

    if (using_fake_data) {
        let file_names = ['preview1.jpg', 'preview2.jpg', 'preview3.jpg'];
        let images = [preview1, preview2, preview3];
        return (
            <div className='image-detail'>
                <ul className='image-detail__list'>
                    {
                        file_names.map(
                            (f, i) => <li
                                className={classNames('image-detail__list__item', f === file_names[selectedImage] && 'image-detail__list__item--focus')}
                                onClick={() => setSelectedImage(i)} key={f}>
                                {f}
                            </li>
                        )
                    }
                </ul>
                <div className='image-detail__image-wrapper'>
                    {
                        selectedImage > 0 &&
                        <img className='live-preview__img live-preview__img--smaller' src={images[selectedImage - 1]}
                             alt='Preview unavailable'/>
                    }
                    {
                        <img className='live-preview__img' src={images[selectedImage]} alt='Preview unavailable'/>
                    }
                    {
                        selectedImage < file_names.length - 1 &&
                        <img className='live-preview__img live-preview__img--smaller' src={images[selectedImage + 1]}
                             alt='Preview unavailable'/>
                    }
                </div>
            </div>
        );
    }

    if (!file_names || file_names.length === 0)
        return (
            <div className='image-detail'>
                <h1 className='home__module__title'>
                    No images found.
                </h1>
            </div>
        );


    return (
        <div className='image-detail'>
            <ul className='image-detail__list'>
                {
                    file_names.map(
                        (f, i) => <li
                            className={classNames('image-detail__list__item', f === file_names[selectedImage] && 'image-detail__list__item--focus')}
                            onClick={() => setSelectedImage(i)} key={f}>
                            {f}
                        </li>
                    )
                }
            </ul>
            <div className='image-detail__image-wrapper'>
                {
                    selectedImage > 0 &&
                    <PreviewImage filename={file_names[selectedImage - 1]} key={file_names[selectedImage - 1]}
                                  at_edge={true}/>
                }
                {
                    <PreviewImage filename={file_names[selectedImage]} key={file_names[selectedImage]}/>
                }
                {
                    selectedImage < file_names.length - 1 &&
                    <PreviewImage filename={file_names[selectedImage + 1]} key={file_names[selectedImage + 1]}
                                  at_edge={true}/>
                }
            </div>
        </div>
    )
}


export default ImageDetail;