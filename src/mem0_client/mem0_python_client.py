import os
import json
from mem0 import MemoryClient

def initialize_mem0_client():
    # MEM0_API_KEY should be set as an environment variable
    if "MEM0_API_KEY" not in os.environ:
        raise ValueError("MEM0_API_KEY environment variable not set.")
    return MemoryClient()

def add_memory(memory_client, data, user_id=None, metadata=None, category=None):
    try:
        memory_client.add(data, user_id=user_id, metadata=metadata, category=category)
        return {"status": "success", "message": "Memory added successfully."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def search_memory(memory_client, query, user_id=None, category=None, limit=5):
    try:
        results = memory_client.search(query, user_id=user_id, category=category, limit=limit)
        # Convert Memory objects to dictionaries for JSON serialization
        serialized_results = []
        for mem in results:
            serialized_results.append({
                "id": mem.id,
                "data": mem.data,
                "metadata": mem.metadata,
                "category": mem.category,
                "created_at": mem.created_at.isoformat() if mem.created_at else None,
                "updated_at": mem.updated_at.isoformat() if mem.updated_at else None,
            })
        return {"status": "success", "results": serialized_results}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    # This block allows the script to be called from the command line
    # and process JSON input/output.
    import sys

    client = None
    try:
        client = initialize_mem0_client()
    except ValueError as e:
        print(json.dumps({"status": "error", "message": str(e)}))
        sys.exit(1)

    action = sys.argv[1]
    input_data = json.loads(sys.argv[2])

    if action == "add":
        result = add_memory(client, input_data["data"], input_data.get("user_id"), input_data.get("metadata"), input_data.get("category"))
    elif action == "search":
        result = search_memory(client, input_data["query"], input_data.get("user_id"), input_data.get("category"), input_data.get("limit", 5))
    else:
        result = {"status": "error", "message": "Unknown action"}

    print(json.dumps(result))

