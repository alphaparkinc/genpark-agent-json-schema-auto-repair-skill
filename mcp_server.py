import sys, json
from client import AgentJsonSchemaAutoRepair

def handle_mcp():
    repairer = AgentJsonSchemaAutoRepair()
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print(json.dumps(repairer.run_benchmark_schema_repair(), indent=2))
        return

    for line in sys.stdin:
        if not line.strip(): continue
        try:
            req = json.loads(line)
            method = req.get("method")
            msg_id = req.get("id")
            
            if method == "initialize":
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {
                    "protocolVersion": "2024-11-05",
                    "serverInfo": {"name": "genpark-agent-json-schema-auto-repair-skill", "version": "1.0.0"},
                    "capabilities": {"tools": {}}
                }}
            elif method == "tools/list":
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {"tools": [
                    {"name": "repair_malformed_json", "description": "Heal broken JSON strings without LLM round-trips.", "inputSchema": {"type": "object", "properties": {"raw_str": {"type": "string"}}}},
                    {"name": "coerce_to_schema", "description": "Cast string numbers to typed schema equivalents.", "inputSchema": {"type": "object", "properties": {"data_dict": {"type": "object"}, "expected_types": {"type": "object"}}}},
                    {"name": "run_benchmark_schema_repair", "description": "Benchmark schema healing accuracy.", "inputSchema": {"type": "object"}}
                ]}}
            elif method == "tools/call":
                tname = req.get("params", {}).get("name")
                args = req.get("params", {}).get("arguments", {})
                if tname == "repair_malformed_json":
                    res = repairer.repair_malformed_json(args.get("raw_str", ""))
                elif tname == "coerce_to_schema":
                    res = repairer.coerce_to_schema(args.get("data_dict", {}), args.get("expected_types", {}))
                else:
                    res = repairer.run_benchmark_schema_repair()
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
            else:
                resp = {"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": "Method not found"}}
            
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "error": {"code": -32000, "message": str(e)}}) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    handle_mcp()
