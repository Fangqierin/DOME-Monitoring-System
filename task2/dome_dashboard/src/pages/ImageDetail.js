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
    const [file_names, set_file_names] = useState([]);
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
        const selected_filename = file_names;
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
                    <img className='live-preview__img' src={ preview1 } alt='Preview unavailable'/>
                    <img className='live-preview__img' src={ preview2 } alt='Preview unavailable'/>
                    <img className='live-preview__img' src={ preview3 } alt='Preview unavailable'/>
                </div>
            </div>
        );
    }

    const selected_filename = [file_names[selectedImage - 1], file_names[selectedImage], file_names[selectedImage + 166]]

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
                    selected_filename?.map(
                        filename => filename && <PreviewImage filename={filename}/>
                    )
                }
            </div>
        </div>
    )
}


export default ImageDetail;