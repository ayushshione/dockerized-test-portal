import { useEffect, useState } from "react";
import sokalp from "./sokalp.png";
import userCss from "./user-style.css";
import StartPage from "./components/user-page";
import TestPage from "./components/test-page";

function App() {
  const [testStart, setTestStart] = useState(0);

  const handleOnTestStart = (action) => {
    setTestStart(action);
  };

  return (
    <>
      <h1>Test Page!</h1>
    </>
  );
}

export default App;
