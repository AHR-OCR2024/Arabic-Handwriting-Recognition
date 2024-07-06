// Home.jsx
import React from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { AnimatePresence } from "framer-motion";
import "./Home.css";
import DAHDICON from "../../assets/Digital_Dahd_Icon.png";
import OCRICON from "../../assets/ocr.png";
import EXAMICON from "../../assets/exam.png";
import SCANICON from "../../assets/scanning.png";

const Home = () => {
  return (
    <div>
      <main className="w-full flex flex-col items-center justify-center mt-10">
        <img src={DAHDICON} alt="Logo" className="home-logo" />
        <h1 className="text-[24px] mb-2 mt-5">Welcome to ضاد الرقمية</h1>
        <p className="mb-5 text-center">
          Explore our featured services for efficient documentation below
        </p>
        <div className="w-auto lg:w-full flex flex-col lg:flex-row items-center justify-center">
          <motion.div
            className="mb-10 rounded-[10px] mr-4 ml-4"
            whileHover={{
              scale: 1.05,
              boxShadow: "0 4px 8px rgba(0, 0, 0, 0.2)", // Added shadow on hover
            }}
          >
            <Link
              className="w-[300px] h-[300px] text-center p-2 bg-white border border-teal-800 rounded-[10px] flex flex-col items-center justify-center"
              to="/our_model"
            >
              <img
                className="w-2/5 opacity-70"
                src={OCRICON}
                alt="Handwriting OCR"
              />
              <p className="text-[18px] font-semibold text-[#387771] mb-2 mt-6">
                Handwriting OCR (our model)
              </p>
              <p className="text-[14px]">
                Convert handwritten text into digital format accurately and
                efficiently.
              </p>
            </Link>
          </motion.div>
          <motion.div
            className="mb-10 rounded-[10px] mr-4 ml-4"
            whileHover={{
              scale: 1.05,
              boxShadow: "0 4px 8px rgba(0, 0, 0, 0.2)", // Added shadow on hover
            }}
          >
            <Link
              className="w-[300px] h-[300px] text-center p-2 bg-white border border-teal-800 rounded-[10px] flex flex-col items-center justify-center"
              to="/exam-grader"
            >
              <img
                className="w-2/5 opacity-70"
                src={EXAMICON}
                alt="Exam Grading"
              />
              <p className="text-[18px] font-semibold text-[#387771] mb-2 mt-6">
                Exam Grading
              </p>
              <p className="text-[14px]">
                Automate the grading process with high accuracy and speed.
              </p>
            </Link>
          </motion.div>
          <motion.div
            className="mb-10 rounded-[10px] mr-4 ml-4"
            whileHover={{
              scale: 1.05,
              boxShadow: "0 4px 8px rgba(0, 0, 0, 0.2)", // Added shadow on hover
            }}
          >
            <Link
              className="w-[300px] h-[300px] text-center p-2 bg-white border border-teal-800 rounded-[10px] flex flex-col items-center justify-center"
              to="/image-rectifying"
            >
              <img
                className="w-2/5 opacity-70"
                src={SCANICON}
                alt="Document Scanner"
              />
              <p className="text-[18px] font-semibold text-[#387771] mb-2 mt-6">
                Document Scanner
              </p>
              <p className="text-[14px]">
                Scan documents quickly and maintain high-quality digital copies.
              </p>
            </Link>
          </motion.div>
        </div>
      </main>
    </div>
  );
};

export default Home;
