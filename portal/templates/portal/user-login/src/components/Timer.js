import { useEffect, useState } from "react";

export default function Timer({hours, seconds, minutes}){
    const [hour, setHour] = useState(0);
    const [minute, setMinute] = useState(0);
    const [second, setSecond] = useState(0);
    const [timeUp, setTimeUp] = useState(false);

    useEffect(() => {
        setHour(hours);
        setMinute(minutes);
        setSecond(seconds);
    }, [])

    const setTimer = () => {
        if(hour === 0 && minute === 0 && second === 0){
            setTimeUp(true);
            clearInterval(intervalId)
        }

        if(hour <= 0 || minute <= 0 || second <= 0){
            clearInterval(intervalId);
        }

        setSecond(second-1);

        if(second === 0){
            setMinute(minute-1);
            setSecond(59);
        }


        if(minute === 0){
            setHour(hour-1);
            setMinute(59);
            setSecond(59);
        }
    }

    const intervalId = setInterval(setTimer, 1000)

    return(
        <>
            {!timeUp 
            ? (<p className="text-lg font-semibold">{hour}:{minute}:{second}</p>) 
            : (<p className="text-lg font-semibold">Time Up!</p>)}
        </>        
    );
}