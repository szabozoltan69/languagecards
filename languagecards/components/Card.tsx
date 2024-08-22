import React, { useState } from 'react';
import useSwipe from '../components/useSwipe';

function Card(props_) {
  const { handleChange, mode, ...props } = props_;

  const [position, setPosition] = useState(0);
  const [removed, setRemoved] = useState(false);
  const [isClicked, setIsClicked] = useState(false);
  const p = 600; // position change
  const t = 50; // flash time for the solution before swiping
  const T = 500; // travel time

  const swipeHandler = useSwipe({
    onSwipedLeft: () => {
      setIsClicked(true);
      setTimeout(() => {setPosition(position - p)}, t);
      setTimeout(() => {setRemoved(true)}, T);
      setTimeout(() => {handleChange(props.id, false)}, T);
    },
    onSwipedRight: () => {
      setIsClicked(true);
      setTimeout(() => {setPosition(position + p)}, t);
      setTimeout(() => {setRemoved(true)}, T);
      setTimeout(() => {handleChange(props.id, true)}, T);
    },
  });

  const handleClick = () => {setIsClicked(!isClicked)};

  const divStyle = {
    position: 'relative',
    transition: 'left ' + (T + 9).toString() + 'ms ease-in-out',
    left: `${position}px`,
  };

  const hideMe = {
    display: 'none',
  };

// <div className="sheetUrl">{props.id}</div>
  return (
    <div {...swipeHandler} onClick={handleClick} style={removed && hideMe || divStyle }>
        { mode === "foreign" ?
          <div className="verticalSpace">{props.text2} {isClicked && <div>– {props.text1}<br/><i>{props.pronunciation}</i>{!!props.grammars.length ? <><br/><i>{props.grammars[0].grammar}</i></> : ""}</div>}</div> :
          <div className="verticalSpace">{props.text1} {isClicked && <div>– {props.text2}<br/><i>{props.pronunciation}</i>{!!props.grammars.length ? <><br/><i>{props.grammars[0].grammar}</i></> : ""}</div>}</div> }
    <br/>
    </div>
  );
}

export default Card;