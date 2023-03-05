import React, {useEffect} from 'react';
import apis from '../../../util/apis';
import PreviewImage from './PreviewImage';
import {using_fake_data} from '../../../util/config';

const LivePreview = () => {
    const [file_names, set_file_names] = React.useState([]);

    useEffect(() => {
        setInterval(() => {
            if(using_fake_data){
                set_file_names(['preview1.jpg', 'preview2.jpg', 'preview3.jpg']);
                return;
            }

            fetch(apis.get_data + "?collection_name=images")
                .then(res => res.json())
                .then(data => {
                    set_file_names(data.result.map(item => item.filename));
                })

            return () => clearInterval();
        }, 10000)
    }, []);

    return (
        <>
            <h2 className="home-subtitle">Live Previews</h2>
            <div className='live-preview'>
                {
                    file_names.map(filename =>
                        filename && <PreviewImage key={filename} filename={filename}/>
                    )
                }

            </div>
        </>

    )
}


export default LivePreview;