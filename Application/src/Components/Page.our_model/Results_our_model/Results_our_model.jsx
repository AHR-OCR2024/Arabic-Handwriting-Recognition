import React from "react";
import "./Results_our_model.css";
import { motion, AnimatePresence } from "framer-motion";

const Results = ({ results }) => {
  return (
    <AnimatePresence>
      {results && results.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: -100 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -100, duration: 0.1 }}
          transition={{ duration: 0.3 }}
          // style={{ width: "100%", marginTop: "5vh", marginBottom: "100vh" }}
        >
          <table className="rounded-table-borders">
            <thead>
              <tr>
                <th>Image</th>
                <th>Label</th>
              </tr>
            </thead>
            <motion.tbody
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ staggerChildren: 0.1 }}
            >
              {results.map((result, index) => (
                <motion.tr
                  key={index}
                  initial={{ opacity: 0, x: -100 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -100, zIndex: -1 }}
                  transition={{
                    duration: 0.3,
                    delay: index < 7 ? index * 0.1 : 0,
                  }}
                >
                  <td>
                    <img src={result.src} alt={result.alt} />
                  </td>
                  <td>{result.alt}</td>
                </motion.tr>
              ))}
            </motion.tbody>
          </table>
        </motion.div>
      )}
    </AnimatePresence>
  );
};

export default Results;
