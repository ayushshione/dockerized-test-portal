import { useEffect } from "react";
import style from "../styles.css";

const QuestionPalette = ({bookmarkedQuestions, currQuestion, savedAnswers, questions, handleQuestionChangeClick }) => {
    return (
        <div className="palette-div mr-10 p-4 w-[400px] rounded-md bg-white shadow-sm flex flex-col justify-center items-center overflow-auto max-h-[410px]">
            <div className="grid grid-cols-5 gap-4 mt-3">
                {questions.map((question, index) => {
                    return (
                        question["id"] === currQuestion["id"]
                            ? (<div
                                    onClick={() => handleQuestionChangeClick(question["id"], index)}
                                    key={question["id"]}
                                    className={(question['id'] in savedAnswers ? "bg-green-400 " : "")  + "ind-ques text-orange-400 border-orange-400 border-[2px] rounded-md text-base p-1 h-12 w-12 flex items-center justify-center"}
                                    >
                                    {index+1}
                                </div>)

                            :(<div
                                    onClick={() => handleQuestionChangeClick(question["id"], index)}
                                    key={question["id"]}
                                    className={(question['id'] in savedAnswers ? "bg-green-400 text-white " : "") + "ind-ques hover:text-orange-400 hover:border-orange-400 border-[2px] rounded-md text-base p-1 h-12 w-12 flex items-center justify-center"}
                                    >
                                    {index+1}
                              </div>));
                })}
            </div>
        </div>
    );
};

export default QuestionPalette;
