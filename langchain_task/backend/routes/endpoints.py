from fastapi import APIRouter, Request, HTTPException, Body
from langchain_together import ChatTogether
from decouple import config
import logging

from typing import Dict
router = APIRouter()
logger = logging.getLogger(__name__)
together_api_key = config('TOGETHER_API_KEY', str)
llm =ChatTogether(
    api_key=together_api_key,
    model="meta-llama/Llama-3-70b-chat-hf",
)




@router.get("/dorner-parameters")
async def get_dorner_parameters(request: Request):
    #This will simply returns the dorner_parameters set by the user
    return {"message": request.app.dorner_parameters }


@router.post("/parameters")
async def adjust_model_parameters(request: Request, paramters: Dict[str, int]= Body(...)):
    #The dorner parameters are set according to the users adjustment in the following part. 
    for paramter in paramters:
        request.app.dorner_parameters[paramter] = paramters[paramter]
    #emotion_level indicate the anger and sadness level
    parameter_values = request.app.dorner_parameters

    try:
        #The template definied in the app.py file is formatted to adjust the llms response level.
        emotion_prompt = request.app.prompt_template_one.format(
            valance_level= parameter_values["valance_level"],
            arousal_level= parameter_values["arousal_level"],
            selection_threshold= parameter_values["selection_threshold"],
            resolution_level= parameter_values["resolution_level"],
            goal_directedness= parameter_values["goal_directedness"],
            securing_rate= parameter_values["securing_rate"],

        )
        #The following code prompts the llm with the formatted template.
        #This query only makes the llm to adjust its tone
        emotion_level = llm.invoke(emotion_prompt) 
        print(emotion_level.content)
        request.app.emotion_level = emotion_level.content.split("\n")
        return request.app.emotion_level
    except Exception as e:
        logger.exception(e)
    except:
        raise HTTPException(status_code=404)

@router.post("/llm-response")
async def get_ai_response(request: Request, user_request: str):
    request.app.history.add_user_message(user_request)
    try:
        """
            The second template which will take the user_request and the angry and sadness level as the input is rendered 
            in the following code. The user request is taken from the frontend request while the emotional level is taken
            from the llms earlier response.
        """ 
        user_response_prompt = request.app.prompt_template_two.format(
            emotion_level_text=request.app.emotion_level,
            user_request=user_request
        )
        ai_response = llm.invoke(user_response_prompt)
        request.app.history.add_ai_message(ai_response.content)
        return ai_response.content
    except Exception as e:
        logger.exception(e)
    except:
        return HTTPException(status_code=404)
    