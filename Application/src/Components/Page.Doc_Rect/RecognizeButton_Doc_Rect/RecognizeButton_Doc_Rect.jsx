// RecognizeButton.jsx
import React, { useState } from "react";
import axios from "axios";
import "./RecognizeButton_Doc_Rect.css";
import { ScaleLoader } from "react-spinners";
import { motion } from "framer-motion";
import { AnimatePresence } from "framer-motion";
import Modal from "../../Modal/Modal";
import PropTypes from "prop-types";
import CheckboxGroup from "../../ImageRectification_Checkboxes/ImageRectification_Checkboxes";

const handleError = (error) => {
  if (
    error.response.data.message.includes(
      "Unexpected result of `predict_function`"
    ) ||
    error.response.data.message.includes("non-empty")
  ) {
    return "Couldn't find any text in the image, please upload a different image and try again.";
  } else if (error.response.data.message.includes("No such file")) {
    return "No image was uploaded, please upload an image and try again.";
  } else if (error.response.data.message.includes("Invalid image format")) {
    return "No valid image was uploaded, only JPEG and PNG images are supported.";
  } else {
    return "Unknown Error: " + error.response.data.message;
  }
};

const RecognizeButton = ({ image, setResults, onError }) => {
  const [loading, setLoading] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState({
    open: false,
    message: "",
  });
  const [geometricUnwrapping, setGeometricUnwrapping] = useState(false);
  const [illuminationRectifying, setIlluminationRectifying] = useState(false);

  const handleClick = async () => {
    setLoading(true);
    const formData = new FormData();
    formData.append("image", image);
    formData.append("model", "model3");
    formData.append("geometricUnwrapping", geometricUnwrapping);
    formData.append("illuminationRectifying", illuminationRectifying);
    if (!image) {
      const errorMessage =
        "No image was uploaded, please upload an image and try again.";
      setIsModalOpen({
        open: true,
        message: errorMessage,
      });
      if (onError) onError(errorMessage);
      setLoading(false);
      return;
    }

    try {
      const customApiUrl = localStorage.getItem("customApiUrl");
      const defaultApiUrl =
        "https://lynx-upright-allegedly.ngrok-free.app/upload-image";
      const apiUrl =
        customApiUrl &&
        (customApiUrl.trim() !== "" || customApiUrl.trim() !== null)
          ? customApiUrl
          : defaultApiUrl;

      let response;
      try {
        response = await axios.post(apiUrl, formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        });
      } catch (error) {
        if (
          (error.response &&
            error.response.status === 404 &&
            apiUrl !== defaultApiUrl) ||
          (error.message &&
            error.message.includes("Network Error") &&
            apiUrl !== defaultApiUrl)
        ) {
          response = await axios.post(defaultApiUrl, formData, {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          });
        } else {
          throw error;
        }
      }

      console.log("Image uploaded successfully:", response.data);

      // Decode the base64 encoded image
      const imageSrc = `data:image/jpeg;base64,${response.data.rectified_image}`;

      setResults({ src: imageSrc, alt: "Recognized Image" });
    } catch (error) {
      console.error("Error uploading image:", error);
      setResults(null); // Set results to null in case of an error
      const errorMessage =
        error.response && error.response.data && error.response.data.message
          ? handleError(error)
          : "Connection error: Make sure you are connected to the internet, otherwise the server might be unavailable.";
      setIsModalOpen({
        open: true,
        message: errorMessage,
      });
      if (onError) onError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <CheckboxGroup
        geometricUnwrapping={geometricUnwrapping}
        setGeometricUnwrapping={setGeometricUnwrapping}
        illuminationRectifying={illuminationRectifying}
        setIlluminationRectifying={setIlluminationRectifying}
        loading={loading}
      />
      <AnimatePresence>
        {loading && (
          <motion.div
            initial={{ opacity: 0, height: 0, marginTop: "0px" }}
            animate={{ opacity: 1, height: "auto", marginTop: "20px" }}
            exit={{ opacity: 0, height: 0, marginTop: "0px" }}
          >
            <ScaleLoader color="#595959" />
          </motion.div>
        )}
      </AnimatePresence>
      <AnimatePresence>
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
        >
          <Modal
            isOpen={isModalOpen.open}
            errorMessage={isModalOpen.message}
            onClose={() => setIsModalOpen({ open: false, message: "" })}
          />
        </motion.div>
      </AnimatePresence>
      <button
        className="recognize-button"
        onClick={handleClick}
        disabled={loading}
      >
        {loading ? "Loading..." : "Recognize"}
      </button>
    </>
  );
};

RecognizeButton.propTypes = {
  image: PropTypes.object,
  setResults: PropTypes.func.isRequired,
  onError: PropTypes.func,
};

export default RecognizeButton;
