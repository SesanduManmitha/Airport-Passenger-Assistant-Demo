import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT / "app"))
from agent import agent

question = json.loads((Path(__file__).parent / "eval_questions.json").read_text(encoding="utf-8"))

passed = 0
for i,t in enumerate(question, 1):
    result = agent.invoke({"messages": [{"role":"user", "content":t["q"]}]})
    reply = result["messages"][-1].content
    low = reply.lower().replace("’", "'")

    ok_any = any(k.lower() in low for k in t["contains_any"])
    ok_not = not any(k.lower() in low for k in t["not_contains"])

    if ok_any and ok_not:
        passed += 1
        print(f"PASS {i}: {t['q']}")
    else:
        print(f"FAIL {i}: {t['q']}")
        print(f"        reply: {reply[:200]}")

print(f"\n{passed}/{len(question)} passed")