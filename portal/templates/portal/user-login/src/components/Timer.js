import React, { useState, useEffect } from 'react';

const CountdownTimer = ({ remainingTime, onTimerEnd }) => {
  const [time, setTime] = useState(remainingTime);

  useEffect(() => {
    console.log(remainingTime);
    setTime(remainingTime);
  }, [remainingTime]);

  useEffect(() => {
    if (time === null) return;

    const intervalId = setInterval(() => {
      // Decrease time by 1 second
      setTime(prevTime => prevTime - 1);

      // Check if the timer has reached zero
      if (time === 0) {
        clearInterval(intervalId);
        // Call the callback function when the timer reaches zero
        onTimerEnd();
      }
    }, 1000);

    // Cleanup the interval when the component is unmounted
    return () => clearInterval(intervalId);
  }, [time, onTimerEnd]);

  if (time === null) {
    return <p>Loading...</p>;
  }

  // Calculate hours, minutes, and seconds
  const hours = Math.floor(time / 3600);
  const minutes = Math.floor((time % 3600) / 60);
  const seconds = time % 60;

  // Format the time as HH:MM:SS
  const formattedTime = `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;

  return (
    <div>
      <p>Time Remaining: {formattedTime}</p>
    </div>
  );
};

export default CountdownTimer;
