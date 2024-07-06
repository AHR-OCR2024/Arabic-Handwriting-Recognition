import React, { useState, useEffect } from "react";
import Backbutton from "../../Components/BackButton/Backbutton";

import ImageUploader from "../../Components/ImageUploader/ImageUploader";
import RecognizeButton_Exam_Grader from "../../Components/Page.Exam_Grader/RecognizeButton_Exam_Grader/RecognizeButton_Exam_Grader";
import Side_Bar from "../../Components/Side_Bar/Side_Bar";
import Title_Bar from "../../Components/Title_Bar/Title_Bar.jsx";
import icon from "../../assets/exam.png";
import Results_Exam_Grader from "../../Components/Page.Exam_Grader/Results_Exam_Grader/Results_Exam_Grader";

const exam_grader = () => {
  const [image, setImage] = useState(null);
  const [results, setResults] = useState("");
  const [questions, setQuestions] = useState(""); // New state for questions

  useEffect(() => {
    setResults("");
  }, [image]);

  return (
    <div className="flex md:min-h-screen justify-center">
      <Side_Bar icon={icon} title="Exam Grader">
        <p>
          How it works: You upload an image with a student's answers, and you
          provide the questions and the correct answers. We OCR the student's
          answers and correctly format them. We make a request to an LLM to
          verify the provided data. We then make another request consisting of
          the OCR-ed exam answers, exam questions, and exam correct answers.
          Finally, another LLM reviews and the data and format the grades to be
          displayed.
        </p>
      </Side_Bar>
      <div className="flex m-10 md:w-full">
        <div className="hidden md:block">
          <Backbutton />
        </div>
        <div className="w-full flex flex-col items-center md:pr-10">
          <Title_Bar title="Exam Grading" />
          <div className="flex flex-col items-center lg:flex-row md:items-start md:justify-between w-full">
            <div className="flex flex-col items-center md:w-1/2">
              <ImageUploader image={image} setImage={setImage} />
            </div>
            <div className="flex flex-col items-baseline md:w-1/2 mt-4 md: md:mt-16">
              <div className="flex flex-col items-center">
                <hr className="w-full md:hidden" />
                <p className="text-center font-bold">
                  Enter the questions and the{" "}
                  <span className="text-teal-800">correct answers</span>
                </p>
                <textarea
                  dir="rtl"
                  className="h-[150px] w-full rounded-[10px] border border-teal-800 pr-2 placeholder:text-right focus:outline-none"
                  placeholder="أدخل الاسئلة والاجابات الصحيحة"
                  value={questions} // Bind the state to the textarea
                  onChange={(e) => setQuestions(e.target.value)} // Update the state on change
                />
                <Results_Exam_Grader results={results} />
              </div>
            </div>
          </div>
          <RecognizeButton_Exam_Grader
            image={image}
            setResults={setResults}
            questions={questions}
          />{" "}
          {/* Pass questions to the component */}
        </div>
      </div>
    </div>
  );
};

export default exam_grader;
