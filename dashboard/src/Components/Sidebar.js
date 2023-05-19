import React from 'react';
import{
    FaRegChartBar,
    FaTh,
    FaSignOutAlt,
} from "react-icons/fa"
import { NavLink } from 'react-router-dom';
import { useAuth } from '../Contexts/AuthContexts';
import logo from "./cnr.png";
import "./Sidebar.css";

const Sidebar = () => {
    const { handleLogout } = useAuth()
    const menuItem=[
        {
            path:"/",
            name:"dashboard",
            icon:<FaTh/>
        },
        {
            path:"/stats",
            name:"stats",
            icon:<FaRegChartBar/>
        },
    ]

    const Logout = async () => {
        handleLogout()
    }

    return (
        <aside className="sidebar">
            <div className="logo-container">
                <img src={logo} alt="logo" className="logo" />
            </div>
            {
                menuItem.map((item, index)=>(
                    <NavLink to={item.path} key={index} className="link" activeClassName="active">
                        <div className="icon">{item.icon}</div>
                        <span className="link_text">{item.name}</span>
                    </NavLink>
                ))
            }
            <div className="link" onClick={Logout}>
                <div className="icon"><FaSignOutAlt/></div>
                <span className="link_text">logout</span>
            </div>
        </aside>
    );
};

export default Sidebar;
