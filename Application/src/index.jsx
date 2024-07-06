//index.jsx
import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route, useLocation } from "react-router-dom";
import { AnimatePresence, motion } from "framer-motion";
import Home from "./Pages/Home/Home.jsx";
import OurModel from "./Pages/our_model/our_model.jsx";
import ExamGrader from "./Pages/exam_grader/exam_grader.jsx";
import ImageRectifying from "./Pages/image_rectifying/image_rectifying.jsx";
import Header from "./Components/Header/Header.jsx";
import Footer from "./Components/Footer/Footer.jsx";
import "./index.css";

const App = () => {
  const location = useLocation();

  return (
    <>
      <Header />
      <div className="main-content">
        <AnimatePresence mode="wait">
          <Routes location={location} key={location.pathname}>
            <Route
              path="/"
              element={
                <motion.div
                  initial={{ x: "15%", opacity: 0 }}
                  animate={{ x: 0, opacity: 1 }}
                  exit={{ x: "-15%", opacity: 0 }}
                >
                  <Home />
                </motion.div>
              }
            />
            <Route
              path="/our_model"
              element={
                <motion.div
                  initial={{ x: "15%", opacity: 0 }}
                  animate={{ x: 0, opacity: 1 }}
                  exit={{ x: "-15%", opacity: 0 }}
                >
                  <OurModel />
                </motion.div>
              }
            />
            <Route
              path="/exam-grader"
              element={
                <motion.div
                  initial={{ x: "15%", opacity: 0 }}
                  animate={{ x: 0, opacity: 1 }}
                  exit={{ x: "-15%", opacity: 0 }}
                >
                  <ExamGrader />
                </motion.div>
              }
            />
            <Route
              path="/image-rectifying"
              element={
                <motion.div
                  initial={{ x: "15%", opacity: 0 }}
                  animate={{ x: 0, opacity: 1 }}
                  exit={{ x: "-15%", opacity: 0 }}
                >
                  <ImageRectifying />
                </motion.div>
              }
            />
          </Routes>
        </AnimatePresence>
      </div>
      <Footer />
    </>
  );
};

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </React.StrictMode>
);
