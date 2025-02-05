from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langchain.prompts import PromptTemplate
from langchain.memory import ChatMessageHistory

from routes.endpoints import router







CORSMiddleware
origins = ["*"]
def lifespan(app: FastAPI):
    app.input_parameters = {"temperature": 0, "max_tokens": 50, "ai_history": "","user_history": "" }
    """
        The following templates will hold a prompt and the requirements for the llms response
    """
    app.user_prompt_with_llm_parameters = """
                                    You are a chatbot tasked with interacting with the user on philosophical topics. You will generate your conversation
                                    under the constraint of temperature and max_tokens size passed to you as an argument. The temperature parameter refers
                                    to the large language parameter and max token is the restriction for your response token. You will also recieve a previous
                                    chat histories of the user requests and your previous responses as a chat history that you will use to create a context. 
                                    
                                    USER REQUEST
                                    {user_request}

                                    TEMPERATURE
                                    {temperature}

                                    MAX TOKENS
                                    {max_tokens}

                                    CHAT HISTORY
                                    {chat_history}


                                    YOUR RESPONSE:
                                """
    app.user_prompt_with_llm_parameters = PromptTemplate(input_variables=["temperature", "max_tokens", "user_history" , "ai_history"],
                                            template=app.user_prompt_with_llm_parameters)  


    app.history = ChatMessageHistory()
    
    yield
    app.input_parameters.clear()
app = FastAPI(lifespan=lifespan)

app.include_router(router, prefix="/llm-response", tags=["llm-response"])


app.add_middleware(
    CORSMiddleware, 
    allow_origins = origins, 
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)