import React, { Children } from 'react';
import{
    FaRegChartBar,
    FaTh,
    FaSignOutAlt,
} from "react-icons/fa"
import { AiFillFolderOpen, IconName } from "react-icons/ai";
import { NavLink } from 'react-router-dom';
import { useState } from 'react';
import logo from "./cnr.png";
import "./Sidebar.css";
import { useAuth } from '../Contexts/AuthContexts';


const Sidebar = ({children}) => {
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
        <div className="container">
              
           <div className="sidebar">
               <div className="top_section">
                    {/*<Navbar/>*/}
                   <h1 style={{display:  "block" }} className="logo"><img src={logo} width={60} height={50}/></h1>
               </div>
               {
                   menuItem.map((item, index)=>(
                       <NavLink to={item.path} key={index} className="link" activeclassname="active">
                           <div className="icon">{item.icon}</div>
                           <div style={{display:"block" }} className="link_text">{item.name}</div>
                       </NavLink>
                   ))
               }
               <div className="link" onClick={Logout}>
                   <div className="icon"><FaSignOutAlt/></div>
                   <div style={{display:  "block"  }} className="link_text">logout</div>
               </div>
           </div>
           <main>{children}</main>
        </div>
    );
};

export default Sidebar;