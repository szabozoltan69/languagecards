import { StrictMode, useEffect, React } from 'react'
import ReactDom from 'react-dom/client'
import useSwipe from '../components/useSwipe';
// import TSComponentTest from '../components/useTS';

let text = {};

function NewTitle() {
  useEffect(() => {
    document.title = text.T0;
  }, []);
}

function Debug(props) {console.log('ddd', props);}

const Title = (props) => (<li key={props.idx}><a className="noUnderline" href={`#${props.idx + 1}`}>{props.text1}</a></li>)

const Card = (props) => (
  <>
    <br/><div className="songNr"><a className="noUnderline" id={props.idx + 1} href="#§">&mdash; {props.idx + 1} &mdash;</a></div><br/>
    <i>{props.text2}</i>
  </>
);

function App(props) {
  text = props[0];
  const rows = Object.keys(props).filter((k, idx) => idx > 0);
  const swipeHandler = useSwipe({ onSwipedLeft: () => console.log('left'), onSwipedRight: () => console.log('right') });
  NewTitle()
  return (
    <div>
      <h2 id="§">{text.T0}</h2>
      <div className="d-flex flex-column">
        <p className="italics">{text.t0}
        </p>
        <div {...swipeHandler}>some swipeable div aaaaaaaa aaaaaaaa aaaaaaaa aaaaaaaa aaaaaaaa aaaaaaaa aaaaaaaa aaaaaaaa aaaaaaaa aaaaaaaa aaaaaaaa   aaaaaaaa</div>
      </div>
      <ol>
        {rows.map((k, idx) => (<Title key={k} idx={idx} {...props[k]} />))}
      </ol>
      <ul>
        {rows.map((k, idx) => (<Card key={k} idx={idx} {...props[k]} />))}
      </ul>
      <div className="d-flex flex-column">
        <p className="otherUrl">
          <a key="h" target="_blank"
          href={text.T6}>{text.t6}</a><br/>
          <a key="i" target="_blank"
          href={text.Tm}>{text.tm}</a><br/>
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
