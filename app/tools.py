import json 
from pathlib import Path
from langchain.tools import tool
from rag import search

FLIGHTS_FILE = Path(__file__).resolve().parent.parent / "data" / "flights.json"

@tool
def search_airport_info(question: str) -> str:
    """Search airport FAQ information: baggage rules, prohibited items, transport, parking,
    check-in times and transit. Use this for any general airport question."""
    results = search(question, k=3)
    return "\n\n".join(f"[{r['source']}] {r['text']}" for r in results)

@tool
def get_flight_status(flight_number: str) -> str:
    """Get status, gate and check-in counters for a flight, e.g. 'UL225'."""
    flights = json.loads(FLIGHTS_FILE.read_text(encoding="utf-8"))
    for f in flights:
        if f["flight"].lower() == flight_number.replace(" ", "").lower():
            return json.dumps(f)
    return f"No flight found with number {flight_number}."

