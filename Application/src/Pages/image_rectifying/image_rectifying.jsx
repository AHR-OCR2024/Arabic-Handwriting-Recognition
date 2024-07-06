import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import ImageUploader from "../../Components/ImageUploader/ImageUploader";
import RecognizeButton from "../../Components/Page.Doc_Rect/RecognizeButton_Doc_Rect/RecognizeButton_Doc_Rect";
import Results from "../../Components/Page.Doc_Rect/Results_Doc_Rect/Results_Doc_Rect";
import Title_Bar from "../../Components/Title_Bar/Title_Bar";
import Side_Bar from "../../Components/Side_Bar/Side_Bar";
import icon from "../../assets/scanning.png";
import Backbutton from "../../Components/BackButton/Backbutton";

function ImageRectifying() {
  const [image, setImage] = useState(null);
  const [results, setResults] = useState(null);

  useEffect(() => {
    setResults(null);
  }, [image]);

  return (
    <div className="min-h-screen w-full flex flex-col md:flex-row">
      <Side_Bar icon={icon} title="Document Scanner">
        <p style={{ fontWeight: "bold" }}>How it works:</p>
        <p>Document Rectification corrects distortions using:</p>
        <p>
          <b>Geometric Unwarping:</b> Corrects any warp or fold in the document,
          making it appear as if it was scanned flat.
        </p>
        <p>
          <b>Illumination Correction:</b> Adjusts lighting and removes shadows.
        </p>
        <p style={{ fontWeight: "bold" }}>How to use it:</p>
        <p>
          1. Upload a document.<br></br>
          2. Select warp correction, illumination correction, or both.<br></br>
          3. Click "Rectify".
        </p>
        <p style={{ color: "red" }}>
          Note: This environment runs on CPU. Geometric unwarping could be fast,
          but illumination correction will be very slow.
        </p>
      </Side_Bar>
      <div className="md:w-1/2 flex m-10">
        <div className="hidden md:block">
          <Backbutton />
        </div>

        <div className="w-full flex flex-col items-center md:items-end pr-0 md:pr-10">
          <div className="flex flex-col items-center">
            <Title_Bar title="Document Scanner" />
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

export default ImageRectifying;
