from client import AgentJsonSchemaAutoRepair
import json

def test():
    r = AgentJsonSchemaAutoRepair()
    print("=== Testing Agent JSON Schema Auto-Repair Skill ===")
    res = r.run_benchmark_schema_repair()
    print(json.dumps(res, indent=2))

if __name__ == "__main__":
    test()
