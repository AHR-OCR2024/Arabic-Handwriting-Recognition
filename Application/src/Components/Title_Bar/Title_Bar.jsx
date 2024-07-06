import React from "react";
import "./Title_Bar.css";

const Title_Bar = ({ title }) => {
  return (
    <div className="title-bar">
      <p>{title}</p>
    </div>
  );
};

export default Title_Bar;
