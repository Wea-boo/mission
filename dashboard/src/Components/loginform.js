import React, { useState } from "react";
import "./loginform.css";
import logo from "./cnr.png";
import passwordIcon from "./password.png";
import userIcon from "./user.png";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../Contexts/AuthContexts";
import AuthServices from "../Services/AuthServices";



const LoginForm = () => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const { handleLogin, isLoggedIn } = useAuth();
    const navigate = useNavigate();

    const inputStyle = {
        backgroundImage: `url(${userIcon})`,
        backgroundRepeat: "no-repeat",
        backgroundPosition: "5px center",
        paddingLeft: "30px",
        backgroundSize: "20px 20px",
    };

    const passwordInputStyle = {
        backgroundImage: `url(${passwordIcon})`,
        backgroundRepeat: "no-repeat",
        backgroundPosition: "5px center",
        paddingLeft: "30px",
        backgroundSize: "20px 20px",
        
    };


    const handleSubmit = (e) => {     
        e.preventDefault();
        handleLogin(username, password);
        navigate('/')
    }

    return (
        <div className="form-outer">
            <div className="form-wrapper">
                <div className="form-shadow"></div>
                <div className="form">
                    <form className="form-inner" onSubmit={handleSubmit}> 
                        <img src={logo} alt="logo" id="login-cnr-logo" />
                        <div style={{width: "100%", display: "flex", flexDirection: "column",gap: "23.31px"}}>
                        <div className="form-groop">
                            <input
                                type="text"
                                id="usrname"
                                placeholder="Nom d'utilisateur"
                                style={inputStyle}
                                value={username}
                                onChange={(e) => setUsername(e.target.value)}
                            />
                        </div>
                        <div className="form-groop">
                            <input
                                type="password"
                                id="pwd"
                                placeholder="Mot de passe"
                                style={passwordInputStyle}
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                            />
                        </div>
                        </div>
                        <button type="submit">Connexion</button>
                    </form>
                </div>
            </div>    
        </div>
    )
}
export default LoginForm;
