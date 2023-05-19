import React from 'react';
import Navbar from './NavBar';
import Sidebar from './Sidebar';
import './MainLayout.css'
const MainLayout = ({children}) => {
    return (
        <div className="app-layout">
            <Sidebar/>
            <div className="main-section">
                <Navbar/>
                <div className="content">
                    {children}
                </div>
            </div>
        </div>
    );
};

export default MainLayout;
