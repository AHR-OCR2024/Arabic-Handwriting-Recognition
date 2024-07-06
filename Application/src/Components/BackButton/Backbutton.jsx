import React from "react";
import { IoArrowBack } from "react-icons/io5";
import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";

const Backbutton = () => {
  const navigate = useNavigate();

  return (
    <>
      <motion.div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          flexDirection: "column",
          cursor: "pointer",
        }}
        onClick={() => navigate("/")}
        whileHover={{ scale: 1.4 }}
      >
        <IoArrowBack style={{ fontSize: "2em", color: "#07522f" }} />
        <p style={{ color: "#07522f", fontSize: "1em", margin: "0" }}>Back</p>
      </motion.div>
    </>
  );
};

export default Backbutton;
