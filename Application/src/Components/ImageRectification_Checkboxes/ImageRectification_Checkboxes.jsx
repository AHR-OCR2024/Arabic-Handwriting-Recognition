import React from "react";
import { motion } from "framer-motion";
import PropTypes from "prop-types";

const CheckboxGroup = ({
  geometricUnwrapping,
  setGeometricUnwrapping,
  illuminationRectifying,
  setIlluminationRectifying,
  loading,
}) => {
  return (
    <>
      <div className="mt-2">
        <label className="inline-flex items-center me-5 cursor-pointer">
          <input
            type="checkbox"
            value=""
            className="sr-only peer"
            checked={geometricUnwrapping}
            onChange={(e) => setGeometricUnwrapping(e.target.checked)}
            disabled={loading}
          />
          <div className="relative w-11 h-6 bg-gray-200 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-0.5 after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-green-600 transition-all"></div>
          <span className="ms-3 text-sm font-medium text-gray-900">
            Geometric Unwrapping
          </span>
        </label>
      </div>
      <div className="mb-4">
        <label className="inline-flex items-center me-5 cursor-pointer">
          <input
            type="checkbox"
            value=""
            className="sr-only peer"
            checked={illuminationRectifying}
            onChange={(e) => setIlluminationRectifying(e.target.checked)}
            disabled={loading}
          />
          <div className="relative w-11 h-6 bg-gray-200 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-0.5 after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-green-600 transition-all"></div>
          <span className="ms-3 text-sm font-medium text-gray-900">
            Illumination Rectifying
          </span>
        </label>
      </div>
    </>
  );
};

CheckboxGroup.propTypes = {
  geometricUnwrapping: PropTypes.bool.isRequired,
  setGeometricUnwrapping: PropTypes.func.isRequired,
  illuminationRectifying: PropTypes.bool.isRequired,
  setIlluminationRectifying: PropTypes.func.isRequired,
  loading: PropTypes.bool.isRequired,
};

export default CheckboxGroup;
