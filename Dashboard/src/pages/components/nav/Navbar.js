import React from 'react';
import classNames from 'classnames';
import {useLocation} from 'react-router-dom';

const Navbar = ({selected, setSelected}) => {
    const location = useLocation();

    if (location.pathname !== '/') {
        return null;
    }


    return (
        <ul className='navbar'>
            <div className='navbar__title'>DOME DASHBOARD</div>
            <li className={classNames('navbar__item', selected === 0 && 'navbar__item--focus')}
                onClick={() => setSelected(0)}>Overview
            </li>
            <li className={classNames('navbar__item', selected === 1 && 'navbar__item--focus')}
                onClick={() => setSelected(1)}>Image Detail
            </li>
            <li className={classNames('navbar__item', selected === 2 && 'navbar__item--focus')}
                onClick={() => setSelected(2)}>Task Detail
            </li>
        </ul>
    );
}


export default React.memo(Navbar);