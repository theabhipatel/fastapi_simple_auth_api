from langchain_groq import ChatGroq
from dotenv import load_dotenv
from app.tools import multipy, divide
from langgraph.graph import StateGraph, MessagesState, START
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()

llm = ChatGroq(model="openai/gpt-oss-120b")
tools = [multipy, divide]

llm_with_tools = llm.bind_tools(tools)

def call_llm(state:MessagesState):
    messages = [
 ("system", "You are a helpfull assistant you name is Gravitas, for math operations use the provided tools and give asnwer in short and simple and without markdown."),
        *state["messages"]
    ]
    response = llm_with_tools.invoke(messages) 

    return {"messages":[response]}


graph = StateGraph(MessagesState)

graph.add_node("llm", call_llm)
graph.add_node("tools", ToolNode(tools))

graph.add_edge(START, "llm")
graph.add_conditional_edges("llm", tools_condition)
graph.add_edge("tools", "llm")

memory = InMemorySaver()
agent = graph.compile(checkpointer=memory)