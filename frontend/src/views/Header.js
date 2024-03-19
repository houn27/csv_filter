import React from 'react'
import { Button} from 'antd'
import './Header.css'
import { useNavigate } from 'react-router-dom';


function Header() {
  const navigate=useNavigate();

  function jumpToArticles(){
    navigate("/list");
  };
  
  function jumpToHome(){
    navigate("/");
  };

  return (
    <div className="header">
        <div className="header-content">
            <section className="header-left">
                <h1>CSV Filter</h1>
            </section>
        
            <section className="header-center">
                <Button type="text" size='large' onClick={jumpToHome}>homepage</Button>
                <Button type="text" size='large' onClick={jumpToArticles}>history</Button>
            </section>
        </div>
    </div>
  )
}

export default Header