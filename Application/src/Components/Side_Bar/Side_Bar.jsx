import React from "react";
import "./Side_Bar.css";

const Side_Bar = ({ icon, title, children }) => {
  return (
    <div className="w-[14%] p-5 bg-[#d9d9d9] hidden md:flex flex-col">
      <div className="sidebar-header">
        <img src={icon} alt="icon" className="sidebar-icon" />
        <div className="sidebar-title">{title}</div>
      </div>
      <div className="sidebar-content">{children}</div>
    </div>
  );
};

export default Side_Bar;
