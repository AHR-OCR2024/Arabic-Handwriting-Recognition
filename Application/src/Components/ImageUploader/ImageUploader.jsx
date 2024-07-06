import "./ImageUploader.css";
import { FaCloudUploadAlt } from "react-icons/fa";
import { IconContext } from "react-icons";
import { motion, AnimatePresence } from "framer-motion";
import Modal from "../Modal/Modal";
import { useState } from "react";
import PropTypes from "prop-types";

const ImageUploader = ({ image, setImage, onError, className, style }) => {
  const [isModalOpen, setIsModalOpen] = useState({
    open: false,
    title: "",
    message: "",
  });

  const handleDrop = (e) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    if (file && /image\/(jpe?g|png|bmp|webp)$/i.test(file.type)) {
      setImage(file);
    } else {
      setImage(null);
      const errorMessage =
        "No valid image was uploaded, only JPEG, PNG, BMP, and WEBP images are supported.";
      setIsModalOpen({
        open: true,
        message: errorMessage,
        title: "Error",
      });
      if (onError) onError(errorMessage);
    }
  };

  const handleClick = () => {
    const fileInput = document.createElement("input");
    fileInput.type = "file";
    fileInput.accept = "image/png, image/jpeg, image/bmp, image/webp";
    fileInput.onchange = (e) => {
      const file = e.target.files[0];
      setImage(file);
    };
    fileInput.click();
  };

  const handleRemove = (e) => {
    setImage(null);
    e.stopPropagation();
  };

  return (
    <>
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
      <div
        className={`drop-area ${className}`}
        style={style}
        onDrop={handleDrop}
        onDragOver={(e) => e.preventDefault()}
        onClick={handleClick}
      >
        {!image && (
          <IconContext.Provider
            value={{
              size: "100",
              color: "#cccccc",
              className: "upload-icon",
            }}
          >
            <FaCloudUploadAlt />
          </IconContext.Provider>
        )}
        <AnimatePresence>
          {image && (
            <motion.img
              src={URL.createObjectURL(image)}
              alt="Uploaded"
              initial={{ scale: 0.7, opacity: 0 }}
              animate={{
                scale: 1,
                opacity: 1,
              }}
              exit={{
                rotate: -50,
                scale: 0,
                opacity: 0,
                position: "absolute",
              }}
            />
          )}
        </AnimatePresence>
        {image && (
          <button className="close-icon-1" onClick={handleRemove}>
            ×
          </button>
        )}
      </div>
      <p className="bottom_text">Upload an image or click to browse</p>
    </>
  );
};

ImageUploader.propTypes = {
  image: PropTypes.object,
  setImage: PropTypes.func.isRequired,
  onError: PropTypes.func,
  className: PropTypes.string,
  style: PropTypes.object,
};

export default ImageUploader;
