from fastapi import APIRouter, Request
from langchain.chains import SimpleSequentialChain


from typing import Dict
router = APIRouter()


@router.get("/")
async def get_the_message(request: Request):
    return {"message": ""}
@router.update("/dorner-parameters")
async def adjust_dorner_parameters(request: Request, paramters: Dict[str, int]):
    for paramter in paramters:
        request.app.dorner_parameters[paramter] = paramters[paramter]
    return {"message": request.app.dorner_parameters}
@router.post("llm-response")
async def get_ai_response(request: Request):
    overall_chain = SimpleSequentialChain(chains=[request.app.first_chain, request.app.second_chain], verbose=True)
