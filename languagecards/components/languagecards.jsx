import { StrictMode, useEffect, useState, React } from 'react'
import ReactDom from 'react-dom/client'
import Card from '../components/Card';

let text = {};
var learnings = JSON.parse(localStorage.getItem("learnings")) || [];
const rows = Object.keys(props).filter((k, idx) => idx > 0);
rows.map((k) => learnings[props[k].id] = 
  (learnings[props[k].id] === true ? true : false) || props[k].is_learned); // if locally true, we accept it as (truly) learned. False or null does not change the "or".
var len = learnings.filter((k) => k === false).length;

function NewTitle() {
  useEffect(() => {
    document.title = text.t6;
  }, []);
}

function Debug(props) {console.log('ddd', props);}

function App(props) {
  text = props[0]; // could not solve via decomposition neither shift(), because props is read only
  const [isClicked, setIsClicked] = useState(false);
  const [lastId, setLastId] = useState(0);

  const handleChange = (id, isRight) => {
    setLastId(id);
    setCount(count - 1);
    if (count === 1) {
      setCount(learnings.filter((k) => k === false).length);  // summarize the to-learn cards
      location.reload(); // not good, forget learnings
    }
    learnings[id] = isRight;
    localStorage.setItem("learnings", JSON.stringify(learnings));
  };

  const [count, setCount] = useState(len);
  localStorage.setItem("learnings", JSON.stringify(learnings));
  const handleClick = () => {setIsClicked(!isClicked);}
  const handleUndo = () => {delete(learnings[lastId]); setCount(learnings.filter((k) => k === false).length); location.reload();}
  const rebaseMe = () => {localStorage.removeItem("learnings"); location.reload();}

  NewTitle()
  return (
    <div>
      <h2 id="§">{count ? count + " " + text.T0 : text.t2}</h2>
      <div className="d-flex flex-column">
        <button onClick={rebaseMe}>{text.ta}</button>
        <span className="small">&nbsp;</span>
        <button onClick={handleClick} className="italics green">{text.ba}{text.t0}</button>
        <span className="small">&nbsp;</span>
        <button onClick={handleUndo} className="orange">{text.T7}</button>
      </div>
      <ul>
        {rows.map((k, idx) => (learnings[props[k].id] == false && <Card key={k} idx={idx} handleChange={handleChange} mode={isClicked && "foreign" || "motherTongue"} {...props[k]} />))}
      </ul>
      <div className="d-flex flex-column">
        <p className="otherUrl">
          <a key="l" target="_blank"
          href={text.T1}>{text.t1}</a></p>
      </div>
    </div>
  );  
}

const root = ReactDom.createRoot(document.getElementById('app'));
root.render(
<StrictMode>
  <App {...window.props} />
</StrictMode>
);
