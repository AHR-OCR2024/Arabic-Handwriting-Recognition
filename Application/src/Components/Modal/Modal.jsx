import React from "react";
import { motion, AnimatePresence } from "framer-motion";
import "./Modal.css";

const Modal = ({
  isOpen,
  title = "Error",
  children,
  errorMessage,
  onClose,
  rtl = false, // add rtl prop with false as default value
}) => {
  return (
    <AnimatePresence>
      {isOpen && (
        <>
          <motion.div className="modal-overlay" onClick={onClose}>
            <motion.div
              className="modal-overlay-before"
              initial={{ opacity: 0, backdropFilter: "blur(0px)" }}
              animate={{ opacity: 1, backdropFilter: "blur(5px)" }}
              exit={{ opacity: 0, backdropFilter: "blur(0px)" }}
            ></motion.div>
            <motion.div
              initial={{
                opacity: 0,
                scale: 0,
                y: 100,
              }}
              animate={{
                opacity: 1,
                scale: 1,
                y: 0,
              }}
              exit={{
                opacity: 0,
                scale: 0,
                y: 70,
              }}
              transition={{ duration: 0.3, type: "spring" }}
              className="modal-content"
              onClick={(e) => e.stopPropagation()}
            >
              <button className="close-icon" onClick={onClose}>
                ×
              </button>
              <h3
                style={{
                  marginBottom: "0px",
                  marginTop: "0px",
                  position: "absolute",
                  top: "23px",
                  fontWeight: "bold",
                }}
              >
                {title}
              </h3>
              <hr
                style={{
                  marginTop: "0px",
                  marginBottom: "10px",
                  width: "25%",
                  marginLeft: "auto",
                  marginRight: "auto",
                }}
              ></hr>
              {errorMessage ? (
                <p
                  style={{
                    textAlign: rtl ? "right" : "left",
                    direction: rtl ? "rtl" : "ltr",
                  }}
                >
                  {errorMessage}
                </p>
              ) : (
                children
              )}
            </motion.div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
};

export default Modal;
