from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from tools import search_airport_info, get_flight_status
import os
from dotenv import load_dotenv

# load enviroment variables
load_dotenv()

#initialize the OpenAI Model
llm= ChatOpenAI(
    model="gpt-5-nano",
    api_key=os.getenv("OPENAI_API_KEY"),
)

SYSTEM_PROMPT = """You are a passenger assistant for bandaranaike internation airport.
- For flight statis, gates or counters, ALWAYS use get_flight_status. Never guess flight details.
-for general airport questions. use search_airport_info and answer only from the results.
-if the tools don't contain the answer, say you dont know and suggest conatacting the airport information desk or the airline passenger is using.
- Only help with the airport-related topics. Keep answers short and clear."""

agent = create_agent(
    model=llm,
    tools=[search_airport_info],
    system_prompt=SYSTEM_PROMPT,
)

result = agent.invoke({
    "messages": [
        {"role":"user","content":"What's the status of UL503 and which gate should I go to?"}
    ]
})

print(result["messages"][-1].content)