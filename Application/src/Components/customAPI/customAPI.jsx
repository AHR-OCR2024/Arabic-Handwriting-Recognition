import React, { useState, useEffect } from "react";
import { MdOutlineCode } from "react-icons/md";
import { MdOutlineCodeOff } from "react-icons/md";

const CustomApiInput = ({ isActive, setIsActive }) => {
  const handleClick = () => {
    const apiUrl = prompt(
      "Enter custom API URL:",
      "leave empty to use default API"
    );
    console.log("the api url is: ", apiUrl);
    if (apiUrl !== null && apiUrl.trim() !== "") {
      localStorage.setItem("customApiUrl", apiUrl);
      setIsActive(true);
    } else {
      setIsActive(false);
      localStorage.removeItem("customApiUrl");
    }
  };

  return (
    <div
      onClick={handleClick}
      style={{
        cursor: "pointer",
        display: "flex",
        alignItems: "center",
        scale: "1.5",
      }}
    >
      {isActive ? (
        <MdOutlineCode style={{ color: "white" }} />
      ) : (
        <MdOutlineCodeOff style={{ color: "white" }} />
      )}
      {isActive && (
        <span style={{ marginLeft: "2px", fontSize: "10px", color: "white" }}>
          active
        </span>
      )}
    </div>
  );
};

export default CustomApiInput;
