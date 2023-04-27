import React, {useEffect} from 'react';
import apis from '../../../util/apis';
import PreviewImage from './PreviewImage';

import preview1 from '../../sources/preview1.jpg';
import preview2 from '../../sources/preview2.jpg';
import preview3 from '../../sources/preview3.jpg';
import {update_interval, using_fake_data} from '../../../util/config';

const LivePreview = () => {
    const [file_names, set_file_names] = React.useState([]);

    useEffect(() => {
        const update_previews = async () => {
            try {
                if (using_fake_data) {
                    set_file_names(['preview1.jpg', 'preview2.jpg', 'preview3.jpg']);
                    return;
                }

                const response = await fetch(apis.get_data + "?collection_name=images&limit_num=3");
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

    return (
        <>
            <h2 className="home-subtitle">Live Previews</h2>
            <div className='live-preview'>
                {
                    using_fake_data
                    ?
                    <>
                        <img className='live-preview__img' src={ preview1 } alt='Preview unavailable'/>
                        <img className='live-preview__img' src={ preview2 } alt='Preview unavailable'/>
                        <img className='live-preview__img' src={ preview3 } alt='Preview unavailable'/>
                    </>
                    :
                    file_names.map((filename, i) =>
                        filename && <PreviewImage filename={filename} key={filename}/>
                    )
                }
            </div>
        </>

    )
}


export default React.memo(LivePreview);