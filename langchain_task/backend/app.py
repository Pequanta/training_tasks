from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from decouple import config




openai_api_key = config('OPENAI_API_KEY', str)
llm = OpenAI(temperature=1, openai_api_key=openai_api_key)

CORSMiddleware
origins = ["*"]
def lifespan(app: FastAPI):
    app.dorner_parameters = {"valance_level": 0, "arousal_level": 0, "selection_threshold": 0, "resolution_level": 0, "goal_directedness": 0, "securing_rate": 0}
    app.models_first_template = """Your task is serving as a chatbot who responds to the user prompt based on Dorner’s Psi Theory parameters. Each of the paramters
                                    will be passed on as an integer in the scale of 1 to 7. Adjust your anger and sadness level based on this parameters and let this
                                    levels affect your response.

                                    VALANCE LEVEL
                                    {valance_level}

                                    AROUSAL LEVEL
                                    {arousal_level}

                                    SELECTION THRESHOLD
                                    {selection_threshold}

                                    RESOLUTION LEVEL
                                    {resolution_level}

                                    GOAL DIRECTEDNESS
                                    {goal_directedness}

                                    SECURING RATE
                                    {securing_rate}

                                    YOUR RESPONSE:
                                """
    app.prompt_template_one = PromptTemplate(input_variables=["valance_level",  "arousal_level", "selection_threshold", "resolution_level", "goal_directedness", "securing_rate"], template=app.models_first_template)  
    app.first_chain = LLMChain(llm=llm, prompt=app.prompt_template_one)

    app.models_second_template = """Given the parameters of Dorner’s Psi Theory parameters, calculate the anger and sadness levels and responed their value in the scale
                                    of 1 to 5.
                                    VALANCE LEVEL
                                    {valance_level}

                                    AROUSAL LEVEL
                                    {arousal_level}

                                    SELECTION THRESHOLD
                                    {selection_threshold}

                                    RESOLUTION LEVEL
                                    {resolution_level}

                                    GOAL DIRECTEDNESS
                                    {goal_directedness}

                                    SECURING RATE
                                    {securing_rate}

                                YOUR RESPONSE:
                                """
    app.prompt_template_two = PromptTemplate(input_variables=["valance_level",  "arousal_level", "selection_threshold", "resolution_level", "goal_directedness", "securing_rate"], template= app.models_second_template)

    # Holds my 'meal' chain
    app.second_chain = LLMChain(llm=llm, prompt=app.prompt_template_two) 
    yield
    app.dorner_parameters.clear()
app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware, 
    allow_origins = origins, 
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)