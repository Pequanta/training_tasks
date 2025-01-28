import { useState } from 'react'
import './App.css'

function App() {
  const [valance, setValance] = useState(0);
  const [arousal, setArousal] = useState(0);
  const [selectionThreshold, setSelectionThreshold] = useState(0);
  const [resolution, setResolution ] = useState(0);
  const [goalDirectedness, setGoalDirectedness] = useState(0);
  const [securingRate, setSecuringRate] = useState(0);
  const handleChange = (event, slideName) =>{
    const value = event.target.value;
    switch(slideName){
      case "valance":
        setValance(value);
        break;
      case "arousal":
        setArousal(value);
        break;
      case "selectionThreshold":
        setSelectionThreshold(value);
        break;
      case "resolution":
        setResolution(value);
        break;
      case "goalDirectedness":
        setGoalDirectedness(value);
        break;
      case "securingRate":
        setSecuringRate(value);
        break;
      default:
        console.log(value);
    }
    
  }
  return (
    <div className="main-container">
      <div className="configuration-div">
        <div className="slider-div">
          <span className="slide-names">Valance Level</span>
          <input type="range" min="1" max="7" value={valance} className="slider" id="myRange" onChange={(event) => handleChange(event, "valance")}/>
          <span>{valance}</span>
        </div>
        <div className="slider-div">
          <span className="slide-names">Arousal Level</span>
          <input type="range" min="1" max="7" value={arousal} className="slider" id="myRange" onChange={(event) => handleChange(event, "arousal")}/>
          <span>{arousal}</span>
        </div>
        <div className="slider-div">
          <span className="slide-names">Selection Threshold</span>
          <input type="range" min="1" max="7" value={selectionThreshold} className="slider" id="myRange" onChange={(event) => handleChange(event, "selectionThreshold")}/>
          <span>{selectionThreshold}</span>
        </div>
        <div className="slider-div">
          <span className="slide-names">Resolution Level</span>
          <input type="range" min="1" max="7" value={resolution} className="slider" id="myRange" onChange={(event) => handleChange(event, "resolution")}/>
          <span>{resolution}</span>
        </div>
        <div className="slider-div">
          <span className="slide-names">Goal Directedness</span>
          <input type="range" min="1" max="7" value={goalDirectedness} className="slider" id="myRange" onChange={(event) => handleChange(event, "goalDirectedness")}/>
          <span>{goalDirectedness}</span>
        </div>
        <div className="slider-div">
          <span className="slide-names">Securing Rate</span>
          <input type="range" min="1" max="7" value={securingRate} className="slider" id="myRange" onChange={(event) => handleChange(event, "securingRate")}/>
          <span>{securingRate}</span>
        </div>
        <div className="apply-button">
          <input type="button" value="Apply" />
        </div>
      </div>
      <div className="chat-box">
        <div className="chat-display-div"></div>
        <div className="chat-input-div">
          <textarea type="textarea" rows="3" className="chat-input"/>
          <input type="submit" className="chat-send" value="send" />
        </div>
      </div>
    </div>
  )
}

export default App
