from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import json

from fetch_sales import fetch_sales
from analyze_sales import analyze_sales

app = FastAPI()


TOOLS = [
    {
        "name": "fetch_sales",
        "description": "Returns monthly sales data.",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "analyze_sales",
        "description": "Analyzes monthly sales data.",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    }
]


def sse(data):
    return f"event: message\ndata: {json.dumps(data)}\n\n"


@app.post("/mcp")
async def mcp(request: Request):

    body = await request.json()

    method = body.get("method")
    msg_id = body.get("id")

    # --------------------------
    # initialize
    # --------------------------

    if method == "initialize":

        response = {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": {
                    "name": "first-contact-mcp",
                    "version": "1.0.0"
                }
            }
        }

    # --------------------------
    # tools/list
    # --------------------------

    elif method == "tools/list":

        response = {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "tools": TOOLS
            }
        }

    # --------------------------
    # tools/call
    # --------------------------

    elif method == "tools/call":

        tool = body["params"]["name"]

        if tool == "fetch_sales":
            result = fetch_sales()

        elif tool == "analyze_sales":
            result = analyze_sales()

        else:
            result = {"error": "Unknown tool"}

        response = {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps(result)
                    }
                ]
            }
        }

    else:

        response = {
            "jsonrpc": "2.0",
            "id": msg_id,
            "error": {
                "code": -32601,
                "message": "Method not found"
            }
        }

    async def stream():
        yield sse(response)

    return StreamingResponse(
        stream(),
        media_type="text/event-stream"
    )
