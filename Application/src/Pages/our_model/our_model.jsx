//our_model.jsx
import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import ImageUploader from "../../Components/ImageUploader/ImageUploader";
import RecognizeButton from "../../Components/Page.our_model/RecognizeButton_our_model/RecognizeButton_our_model";
import Results from "../../Components/Page.our_model/Results_our_model/Results_our_model";
import Title_Bar from "../../Components/Title_Bar/Title_Bar";
import Side_Bar from "../../Components/Side_Bar/Side_Bar";
import icon from "../../assets/ocr.png";
import Backbutton from "../../Components/BackButton/Backbutton";

function App() {
  const [image, setImage] = useState(null);
  const [results, setResults] = useState([]);

  useEffect(() => {
    setResults([]);
  }, [image]);

  return (
    <div className="min-h-screen w-full flex flex-col md:flex-row">
      <Side_Bar icon={icon} title="Handwriting OCR (our model)">
        <p style={{ fontWeight: "bold" }}>How it works:</p>
        <p>
          OCR Consists of two stages: The segmentation stage divides the image
          into the smallest possible unit of words / sub words (we call them
          "islands").
        </p>
        <p>The recognition stage converts the segments to text using AI.</p>
        <p style={{ fontWeight: "bold" }}>How to use it:</p>
        <p>Upload an image. Click "Recognize".</p>
        <p style={{ color: "red" }}>
          Note: Our model is a proof of concept, it has been trained on limited
          data.
        </p>
      </Side_Bar>
      <div className="md:w-1/2 flex m-10">
        <div className="hidden md:block">
          <Backbutton />
        </div>

        <div className="w-full flex flex-col items-end pr-0 md:pr-10">
          <div className="flex flex-col items-center">
            <Title_Bar title="Handwriting OCR (our model)" />
            <ImageUploader image={image} setImage={setImage} />
            <RecognizeButton image={image} setResults={setResults} />
          </div>
        </div>
      </div>
      <div className="w-full md:w-auto mt-0 md:mt-24 mb-5 flex md:block justify-center">
        <Results results={results} />
      </div>
    </div>
  );
}

export default App;
