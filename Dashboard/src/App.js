import React from 'react';
import {BrowserRouter as Router, Routes, Route} from 'react-router-dom';

import Home from "./pages/Home";

import DetailedTable from './pages/DetailedTable';
import TaskDetail from './pages/TaskDetail';
import Navbar from './pages/components/nav/Navbar';

import './style/App.scss';
import './style/Navbar.scss';
import './style/Icon.scss';
import ImageDetail from './pages/ImageDetail';


const App = () => {
    const [selected, setSelected] = React.useState(0);

    return (
        <div id='app' className="app">
            <Router>
                <Navbar selected={selected} setSelected={setSelected}/>
                <div className='nav-space'>
                </div>

                <Routes>
                    <Route path="/" element={
                        selected === 0
                            ? <Home/>
                            : selected === 1
                                ? <ImageDetail/>
                                : <TaskDetail/>
                    }/>
                    <Route path="/chart/:name" element={<DetailedTable/>}/>
                </Routes>
            </Router>
        </div>
    )
}


export default App;
