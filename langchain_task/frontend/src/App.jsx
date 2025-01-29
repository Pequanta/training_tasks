import { useState } from 'react'
import './App.css'

function App() {


  const [userRequest, setUserRequest] = useState();
  const [llmResponse, setLlmResponse] = useState();
  const [emotionLevel, setEmotionLevel] = useState({
    "sadness": 1,
    "anger": 1
  });
  const [dornerParameters, setDornerParameters] = useState({
    valance_level: 1,
    arousal_level: 1,
    selection_threshold: 1,
    resolution_level: 1,
    goal_directedness: 1,
    securing_rate: 1
  })


  const [backendApi, setBackendApi] = useState("http://0.0.0.0:8000/llm-response")

  const adjustDornerParameters = async () =>{
    const response = await fetch(backendApi + "/dorner-parameters", {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(dornerParameters)
    }); 
    const data = await response.json();
    setEmotionLevel({
      "sadness": data[0][data[0].length - 1],
      "anger": data[1][data[1].length - 1]
    })
  }

  const getLlmResponse = async () =>{
    const response = await fetch(backendApi + `/llm-response?user_request=${userRequest}`, {
      method: 'POST'
    }); 

    const data = await response.json();
    setLlmResponse(data)
  }

  const handleUserRequest = (event) =>{
    const value = event.target.value;
    setUserRequest(value);
  }
  
  const handleChange = (event, slideName) =>{
    const value = event.target.value;
    switch(slideName){
      case "valance":
        setDornerParameters({...dornerParameters, valance_level: value})
        break;
      case "arousal":
        setDornerParameters({...dornerParameters, arousal_level: value})
        break;
      case "selectionThreshold":
        setDornerParameters({...dornerParameters, selection_threshold: value})
        break;
      case "resolution":
        setDornerParameters({...dornerParameters, resolution_level: value})
        break;
      case "goalDirectedness":
        setDornerParameters({...dornerParameters, goal_directedness: value})
        break;
      case "securingRate":
        setDornerParameters({...dornerParameters, securing_rate: value})
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
          <input type="range" min="1" max="7" value={dornerParameters["valance_level"]} className="slider" id="myRange" onChange={(event) => handleChange(event, "valance")}/>
          <span>{dornerParameters["valance_level"]}</span>
        </div>
        <div className="slider-div">
          <span className="slide-names">Arousal Level</span>
          <input type="range" min="1" max="7" value={dornerParameters["arousal_level"]} className="slider" id="myRange" onChange={(event) => handleChange(event, "arousal")}/>
          <span>{dornerParameters["arousal_level"]}</span>
        </div>
        <div className="slider-div">
          <span className="slide-names">Selection Threshold</span>
          <input type="range" min="1" max="7" value={dornerParameters["selection_threshold"]} className="slider" id="myRange" onChange={(event) => handleChange(event, "selectionThreshold")}/>
          <span>{dornerParameters["selection_threshold"]}</span>
        </div>
        <div className="slider-div">
          <span className="slide-names">Resolution Level</span>
          <input type="range" min="1" max="7" value={dornerParameters["resolution_level"]} className="slider" id="myRange" onChange={(event) => handleChange(event, "resolution")}/>
          <span>{dornerParameters["resolution_level"]}</span>
        </div>
        <div className="slider-div">
          <span className="slide-names">Goal Directedness</span>
          <input type="range" min="1" max="7" value={dornerParameters["goal_directedness"]} className="slider" id="myRange" onChange={(event) => handleChange(event, "goalDirectedness")}/>
          <span>{dornerParameters["goal_directedness"]}</span>
        </div>
        <div className="slider-div">
          <span className="slide-names">Securing Rate</span>
          <input type="range" min="1" max="7" value={dornerParameters["securing_rate"]} className="slider" id="myRange" onChange={(event) => handleChange(event, "securingRate")}/>
          <span>{dornerParameters["securing_rate"] }</span>
        </div>
        <div className="apply-button">
          <span>Anger: {emotionLevel["sadness"]}</span>
          <span>Sadness: {emotionLevel["anger"]}</span>
          <input type="button" value="Apply" onClick={event => adjustDornerParameters(event)}/>
        </div>
      </div>
      <div className="chat-box">
        <div className="chat-display-div">
          <div className="chat-content">
            {llmResponse}
          </div>
        </div>
        <div className="chat-input-div">
          <textarea type="textarea" rows="3" className="chat-input" onChange={event => handleUserRequest(event)}/>
          <input type="submit" className="chat-send" onClick={(event) => getLlmResponse(event)} value="send" />
        </div>
      </div>
    </div>
  )
}

export default App
