import React from "react";
import "./Results_Doc_Rect.css";
import { motion, AnimatePresence } from "framer-motion";

const Results = ({ results }) => {
  const downloadImage = () => {
    const link = document.createElement("a");
    link.href = results.src;
    link.download = results.alt || "download";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <AnimatePresence>
      {results && (
        <motion.div
          initial={{ opacity: 0, y: -100 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -100, duration: 0.1 }}
          transition={{ duration: 0.3 }}
        >
          <div className="flex justify-center flex-col items-center sm:items-start">
            <div className="w-full sm:w-1/2 flex flex-col items-center">
              <img className="rounded-lg" src={results.src} alt={results.alt} />
              <button
                onClick={downloadImage}
                className="mt-2 p-2 text-white rounded-full w-full sm:w-1/2"
              >
                Download Image
              </button>
            </div>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
};

export default Results;
