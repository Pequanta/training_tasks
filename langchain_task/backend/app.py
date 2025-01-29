from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langchain.prompts import PromptTemplate
from langchain.memory import ChatMessageHistory

from routes.endpoints import router







CORSMiddleware
origins = ["*"]
def lifespan(app: FastAPI):
    app.emotion_level = [] #holds the value of anger level and sadness level to be sent to frontend
    app.dorner_parameters = {"valance_level": 0, "arousal_level": 0, "selection_threshold": 0, "resolution_level": 0, "goal_directedness": 0, "securing_rate": 0}
    """
        The following templates will hold a prompt and the requirements for the llms response
    """
    app.models_emotion_calculation = """
                                    The following is a description for Dorner’s Psi Theory Parameters.
                                    Valence Level: Measures the spectrum of attraction (appetence) vs. aversion; corresponds to positive vs. negative reinforcement.
                                    Arousal Level: Reflects the agent’s readiness for action, similar to the function of the ascending reticular formation in humans.
                                    Selection Threshold: Indicates how easily the agent shifts between different intentions or balances multiple goals; reflects the dynamics of motive dominance. A higher selection threshold means the agent shifts less easily.
                                    Resolution Level: Describes the agent’s accuracy in perceiving the world, ranging from detailed cognition to rapid perception.
                                    Goal-Directedness: Represents the stability of the agent's motives; indicates how strongly the agent prioritizes its goals versus adapting or 'going with the flow.'
                                    Securing Rate: Refers to the frequency with which the agent checks its environment; involves reflective and orientation behaviors.

                                    Sample of Five Emotions (Directed Affect Plus Modulation) According to Psi Theory:
                                    Anger: Arises when an obstacle (often another agent) clearly prevents the achievement of a relevant goal. Characteristics: negative valence, high arousal, low resolution level, high action-readiness, high selection threshold, and goal redirection to counter the obstacle.
                                    Sadness: Occurs when all perceived paths to achieving active, relevant goals are blocked, without a specific obstacle. Characteristics: negative valence, low arousal, decreased action-readiness due to goal inhibition, and an increased demand for affiliation (support-seeking behavior)

                                    Your task is to adjust your anger and sadness level based on Dorner’s Psi Theory parameters.Parameters are passed to you and each of the paramters
                                    will be passed on as an integer in the scale of 1 to 7.The anger and sadness level ranges from 1 to 5.Avoid any comments and remarks in your response and return your anger and sadness level only. Let this
                                    levels affect your response later.

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
    app.prompt_template_one = PromptTemplate(input_variables=["valance_level", 
                                                              "arousal_level", 
                                                              "selection_threshold", 
                                                              "resolution_level",
                                                              "goal_directedness",
                                                              "securing_rate"],
                                            template=app.models_emotion_calculation)  

    app.models_user_response = """
                                  Given a user request your will respond to the request. You will also be given an anger level
                                  and a sadness level to which you will adjust your tone.For example if you get an anger level of 5
                                  you should be answering in annoying way.                                                                                                                                                                                                                                                                                                                                                                                              
                        
                        
                                  USER REQUEST                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
                                  {user_request}

                                  EMOTION_LEVEL_TEXT
                                  {emotion_level_text}

                                  YOUR RESPONSE:
                               """



    app.history = ChatMessageHistory()
    
    app.prompt_template_two = PromptTemplate(input_variables=["user_request", "emotion_level_text"], template= app.models_user_response)
    yield
    app.dorner_parameters.clear()
app = FastAPI(lifespan=lifespan)

app.include_router(router, prefix="/llm-response", tags=["llm-response"])


app.add_middleware(
    CORSMiddleware, 
    allow_origins = origins, 
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)