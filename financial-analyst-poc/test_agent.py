import json
import sys
sys.path.append('.')
from agent.financial_agent import FinancialAgent

agent = FinancialAgent()

# Test different queries
queries = [
    "Price of INFY",
    "Compare TCS and INFY",
    "Market updates"
]

for q in queries:
    print(f"\n{'='*60}")
    print(f"Query: {q}")
    print(f"{'='*60}")
    try:
        result = agent.run(q)
        print(json.dumps(result, indent=2, default=str)[:1000])
    except Exception as e:
        import traceback
        print(f"ERROR: {traceback.format_exc()[:500]}")
