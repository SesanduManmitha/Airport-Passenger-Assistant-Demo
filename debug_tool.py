import sys
sys.path.append("app")
from app.tools import get_flight_status
from agent import agent

#print(get_flight_status.invoke({"flight_number":"UL503"}))

result = agent.invoke({"messages": [{"role":"user","content":"what's th status of UL503?"}]})
for m in result["messages"]:
    print(type(m).__name__, "|", getattr(m, "tool_calls", None),"|", str(m.content)[:150])

tests = ["UL503", "ul 503", "UL99999", "../../.env", "","UL503; DROP TABLE FLIGHTS"]
for t in tests:
    print(repr(t), "->", get_flight_status.invoke({"flight_number": t})[:70])