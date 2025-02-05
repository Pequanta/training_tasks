import { useState } from 'react'
import './App.css'

function App() {


  const [userRequest, setUserRequest] = useState();
  const [llmResponse, setLlmResponse] = useState();

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
  
  return (
    <div className="main-container">
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
