import { useEffect, useState } from "react";
import sokalp from "./sokalp.png";
import style from "./styles.css";
import QuestionPalette from "./components/QuestionPalette";
import Timer from "./components/Timer";

function App() {

  const [question, setQuestion] = useState({});
  const [selectedOption, setSelectedOption] = useState(null);
  const [currQuestionNumber, setCurrQuestionNumber] = useState(0);
  const [savedAnswers, setSavedAnswers] = useState([]);

  let questions = [
    {
      id: 1,
      question: "<h1>What is the full form of DSA</h1>",
      op1: "DSA",
      op2: "DS2",
      op3: "DS3",
      op4: "DS4",
    },
    {
      id: 2,
      question: "What is the acronym of DSA?",
      op1: "DS5",
      op2: "DS6",
      op3: "DS7",
      op4: "DS8",
    },
    {
      id: 3,
      question: "What is queue?",
      op1: "DS9",
      op2: "DS10",
      op3: "DS11",
      op4: "DS12",
    },
    {
      id: 4,
      question: "What is stack?",
      op1: "DSA12",
      op2: "DS13",
      op3: "DS14",
      op4: "DS15",
    },
    {
      id: 5,
      question: "What is a linked list?",
      op1: "DSA16",
      op2: "DSA7",
      op3: "DS18",
      op4: "DS19",
    },
    {
      id: 6,
      question: "What is the structure of the node of the linked list?",
      op1: "DSA20",
      op2: "DS21",
      op3: "DS32",
      op4: "DS43",
    },
  ]

  useEffect(() => {
    setQuestion(questions[0]);
  }, [])

  useEffect(() => {
    let flag = 0;

    for(let i=0; i<savedAnswers.length; i++){
      if(savedAnswers[i]['id'] === question['id']){
        flag = 1;
        setSelectedOption(`${savedAnswers[i]['selected_option']}`)

        return;
      }
    }

    setSelectedOption(null);
  }, [question])

  const handleOnOptionSelect = (e) => {
    console.log(e.target.value)
    setSelectedOption(e.target.value)
  }

  const handleQuestionChangeClick = (id, index) => {
    setQuestion(questions[id - 1]);
    setCurrQuestionNumber(index);
  }

  const handleNext = () => {
    let index = currQuestionNumber;

    if (index + 1 >= questions.length) {
      return;
    }
    else {
      setQuestion(questions[index + 1]);
      setCurrQuestionNumber(index + 1)
    }
  }

  const handleBack = () => {
    let index = currQuestionNumber;

    if (index - 1 < 0) {
      return;
    }
    else {
      setQuestion(questions[index - 1])
      setCurrQuestionNumber(index - 1)
    }
  }

  const handleSave = () => {
 
    const selectedAnswer = selectedOption === null ? null : parseInt(selectedOption);
    let flag = 0;
    for(let i=0; i<savedAnswers.length; i++){
      if(savedAnswers[i]['id'] === question['id']){
        const updatedArray = savedAnswers.filter(answer => answer['id'] !== question['id']);
        setSavedAnswers(updatedArray);
        flag = 1;
      }
    }

    if(flag === 0){
      setSavedAnswers(
        [...savedAnswers, {
            id: question['id'],
            selected_option: selectedAnswer,
          }
        ]
      )
    }

    return new Promise((resolve) => {
      setTimeout(() => { // instead of timeout we can exchange it for the fetch
        console.log('Questino saved');
        resolve();
      }, 2000);
    });
  }

  const handleSaveAndNext = () => {
    handleSave()
    handleNext()
  }

  const handleClear = () => {
    setSelectedOption(null);
    const updatedArray = savedAnswers.filter((item) => item['id'] !== question['id']);
    setSavedAnswers(updatedArray);
    
    return new Promise((resolve) => {
      setTimeout(() => { // instead of timeout we can exchange it for the fetch
        console.log('Question answer deleted');
        resolve();
      }, 2000);
    });
  }

  return (
    <>
      <nav>
        <div className="bg-white p-4 shadow-sm flex justify-center items-center">
          <div className="w-full mx-9 flex items-center justify-between">
            <img className="h-8" src={sokalp} alt="sokalp-logo" />
            <Timer hours={0} minutes={0} seconds={10}  />
          </div>
        </div>
      </nav>

      <div className="flex items-start justify-between w-full mt-14 gap-6">
        <div className="question-div p-6 rounded-md flex-grow bg-white shadow-sm ml-11">
          <h1 className='text-[18px] font-semibold mb-9'>Question {currQuestionNumber + 1} / {questions.length}</h1>
          <div className="question-para mb-9" dangerouslySetInnerHTML={{ '__html': question['question'] }}>
          </div>
          <div className="op-div flex w-full items-center mb-5 gap-3 flex-wrap">
            <input className="size-6" checked={selectedOption === '1'} onChange={handleOnOptionSelect} type="radio" name='answer' value={'1'} id='op1-r' />
            <label htmlFor="op1-r" dangerouslySetInnerHTML={{ '__html': question['op1'] }}></label>
          </div>
          <div className="op-div flex w-full items-center mb-5 gap-3 flex-wrap">
            <input className="size-6" checked={selectedOption === '2'} onChange={handleOnOptionSelect} type="radio" name='answer' value={'2'} id='op2-r' />
            <label htmlFor="op2-r" dangerouslySetInnerHTML={{ '__html': question['op2'] }}></label>
          </div>
          <div className="op-div flex w-full items-center mb-5 gap-3 flex-wrap">
            <input className="size-6" checked={selectedOption === '3'} onChange={handleOnOptionSelect} type="radio" name='answer' value={'3'} id='op3-r' />
            <label htmlFor="op3-r" dangerouslySetInnerHTML={{ '__html': question['op3'] }}></label>
          </div>
          <div className="op-div flex w-full items-center mb-5 gap-3 flex-wrap">
            <input className="size-6" checked={selectedOption === '4'} onChange={handleOnOptionSelect} type="radio" name='answer' value={'4'} id='op4-r' />
            <label htmlFor="op4-r" dangerouslySetInnerHTML={{ '__html': question['op4'] }}></label>
          </div>

          <div className="buttons flex gap-3 mt-8">
            <button
              onClick={handleSaveAndNext}
              className="p-3 transition-all rounded-md border-slate-300 border-[2px] hover:text-orange-400 hover:border-orange-400"
            >
              Save and Next
            </button>
            <button
              onClick={handleNext}
              className="p-3 transition-all rounded-md border-slate-300 border-[2px] hover:text-orange-400 hover:border-orange-400"
            >
              Next
            </button>
            <button
              onClick={handleBack}
              className="p-3 transition-all rounded-md border-slate-300 border-[2px] hover:text-orange-400 hover:border-orange-400"
            >
              Back
            </button>
            <button
              onClick={handleClear}
              className="p-3 transition-all rounded-md border-slate-300 border-[2px] hover:text-orange-400 hover:border-orange-400"
            >
              Clear
            </button>
          </div>
        </div>
        <QuestionPalette currQuestion={question} handleQuestionChangeClick={handleQuestionChangeClick} questions={questions} />
      </div>
    </>
  );
}


export default App;
