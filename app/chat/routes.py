from fastapi import APIRouter, Depends
from app.middleware import get_current_user
from pydantic import BaseModel
from app.agent import agent

router = APIRouter(prefix="/chat", tags=["Chat"], dependencies=[Depends(get_current_user)])

class ChatAgentRequest(BaseModel):
    user_message:str

@router.post("/")
def chat_agent(body:ChatAgentRequest):
    messages = [
        ("human", body.user_message)
    ]

    
    result = agent.invoke({"messages":messages}, 
                      config={
                          "configurable":{
                              "thread_id":"user_1"
                          }
                      },  
                          )

    return {
        "response": result["messages"][-1].content,
        "result":result
    }
