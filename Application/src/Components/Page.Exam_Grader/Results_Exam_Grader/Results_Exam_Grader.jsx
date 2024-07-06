import React from "react";

const Results_Exam_Grader = ({ results }) => {
  return (
    <div className="mt-4 p-4 border border-teal-800 rounded-[10px] w-full text-center bg-white">
      <p className="whitespace-pre-wrap">
        {results
          ? results
          : "سيظهر التصحيح هنا\nمع مراجعة الإجابات\nبهذا الشكل"}
      </p>
    </div>
  );
};

export default Results_Exam_Grader;
