import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import "./Header.css";
import Modal from "../Modal/Modal";
import DAHDICON1 from "../../assets/Digital_Dahd.png";
import CustomApiInput from "../customAPI/customAPI";

const Header = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isApiActive, setIsApiActive] = useState(false);

  useEffect(() => {
    const apiUrl = localStorage.getItem("customApiUrl");
    if (apiUrl) {
      setIsApiActive(true);
    }
  }, []);

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  return (
    <>
      <header className="header">
        <button className="menu-button" onClick={toggleMenu}>
          ☰
        </button>
        <div
          className="nav-logo"
          style={{
            display: "flex",
            alignItems: "center",
            flexDirection: "row",
            gap: "20px",
          }}
        >
          <Link to="/">
            <img src={DAHDICON1} alt="Logo" className="nav-logo" />
          </Link>
          <Link
            to="/"
            className="hidden md:block"
            style={{
              color: "#f7f7f7",
              fontSize: "20px",
            }}
          >
            ضاد الرقمية
          </Link>
        </div>
        <nav className="hidden md:flex">
          <ul className="flex m-0 p-0 list-none">
            <li className="mr-5">
              <Link
                className="text-white hover:text-[#afafaf] transition-all"
                to="/"
              >
                HOME
              </Link>
            </li>
            <li className="mr-5">
              <Link
                className="text-white hover:text-[#afafaf] transition-all"
                to="/our_model"
              >
                Handwriting OCR
              </Link>
            </li>
            <li className="mr-5">
              <Link
                className="text-white hover:text-[#afafaf] transition-all"
                to="/exam-grader"
              >
                Exam Grading
              </Link>
            </li>
            <li className="mr-5">
              <Link
                className="text-white hover:text-[#afafaf] transition-all"
                to="/image-rectifying"
              >
                Document Scanner
              </Link>
            </li>
            <li className="mr-5">
              <Link
                className="text-white hover:text-[#afafaf] transition-all"
                to="/about-us"
              >
                About Us
              </Link>
            </li>
            <li className="mr-5 flex justify-center items-center">
              <CustomApiInput
                isActive={isApiActive}
                setIsActive={setIsApiActive}
              />
            </li>
          </ul>
        </nav>
      </header>
      <Modal isOpen={isMenuOpen} title="" onClose={toggleMenu}>
        <ul className="flex flex-col items-center justify-center text-center">
          <li className="mb-2">
            <Link
              className="text-white hover:text-[#afafaf] transition-all"
              to="/"
              onClick={toggleMenu}
            >
              HOME
            </Link>
          </li>
          <li className="mb-2">
            <Link
              className="text-white hover:text-[#afafaf] transition-all"
              to="/our_model"
              onClick={toggleMenu}
            >
              Handwriting OCR (Our Model)
            </Link>
          </li>
          <li className="mb-2">
            <Link
              className="text-white hover:text-[#afafaf] transition-all"
              to="/exam-grader"
              onClick={toggleMenu}
            >
              Exam Grading
            </Link>
          </li>
          <li className="mb-2">
            <Link
              className="text-white hover:text-[#afafaf] transition-all"
              to="/image-rectifying"
              onClick={toggleMenu}
            >
              Document Scanner
            </Link>
          </li>
          <li className="mb-2">
            <Link
              className="text-white hover:text-[#afafaf] transition-all"
              to="/about-us"
              onClick={toggleMenu}
            >
              About Us
            </Link>
          </li>
          <li className="mb-2 flex justify-center items-center">
            <CustomApiInput
              isActive={isApiActive}
              setIsActive={setIsApiActive}
            />
          </li>
        </ul>
      </Modal>
    </>
  );
};

export default Header;
