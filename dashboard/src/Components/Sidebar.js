import React, { Children } from 'react';
import{
    FaBars,
    FaRegChartBar,
    FaTh,
}from "react-icons/fa"
import { AiFillFolderOpen, IconName } from "react-icons/ai";
import { NavLink } from 'react-router-dom';
import { useState } from 'react';
import logo from "./cnr.png";
const Sidebar = ({children}) => {
    const [isOpen, setIsOpen] = useState(false);
    const toggle = () => setIsOpen (!isOpen);
    const menuItem=[
        {
            path:"/",
            name:"dashboard",
            icon:<FaTh/>
        },
        {
            path:"/Demandes",
            name:"demandes",
            icon:<AiFillFolderOpen/>
        },
        {
            path:"/Stats",
            name:"stats",
            icon:<FaRegChartBar/>
        },

    ]


    return (
        <div className="container">
           <div style={{width: isOpen ? "200px" : "50px"}} className="sidebar">
               <div className="top_section">
                   <h1 style={{display: isOpen ? "block" : "none"}} className="logo"><img src={logo} width={60} height={50} /></h1>
                   <div style={{marginLeft: isOpen ? "50px" : "0px"}} className="bars">
                       <FaBars onClick={toggle}/>
                   </div>
               </div>
               {
                   menuItem.map((item, index)=>(
                       <NavLink to={item.path} key={index} className="link" activeClassName="active">
                           <div className="icon">{item.icon}</div>
                           <div style={{display: isOpen ? "block" : "none"}} className="link_text">{item.name}</div>
                       </NavLink>
                   ))
               }
           </div>
           <main>{children}</main>
        </div>
    );
};

export default Sidebar;