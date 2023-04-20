import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

import Home from "./pages/Home";

import './style/App.scss';
import DetailedTable from './pages/DetailedTable';
import TaskDetail from './pages/TaskDetail';


const App = () =>
    <div className="app">
        <Router>
            <Routes>
                <Route path="/" element={<Home/>} />
                <Route path="/waypoints" element={<Home/>} />
                <Route path="/tasks" element={<TaskDetail/>} />
                <Route path="/chart/:name" element={<DetailedTable/>} />
            </Routes>
        </Router>
    </div>


export default App;
