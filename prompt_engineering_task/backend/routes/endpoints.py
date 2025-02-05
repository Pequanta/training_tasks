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



@router.post("/llm-response")
async def get_ai_response(request: Request, user_request: str):
    try:
        user_response_prompt = request.app.user_prompt_with_llm_parameters.format(
            user_request=user_request,
            temperature=request.app.input_parameters["temperature"],
            max_tokens=50,
            chat_history=request.app.history.messages
        )
        ai_response = llm.invoke(user_response_prompt)
        request.app.history.add_ai_message(ai_response.content)
        request.app.history.add_user_message(user_request)
        return ai_response.content
    except Exception as e:
        logger.exception(e)
    except:
        return HTTPException(status_code=404)
    