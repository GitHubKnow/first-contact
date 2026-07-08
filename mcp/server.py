from fastapi import APIRouter, Request
import json

from .fetch_sales import fetch_sales
from .analyze_sales import analyze_sales


router = APIRouter()


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


@router.post("/mcp")
async def mcp(request: Request):

    body = await request.json()

    method = body.get("method")
    msg_id = body.get("id")


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
                    "name": "armoriq-sales-mcp",
                    "version": "1.0.0"
                }
            }
        }


    elif method == "tools/list":

        response = {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "tools": TOOLS
            }
        }


    elif method == "tools/call":

        tool = body["params"]["name"]


        if tool == "fetch_sales":
            result = fetch_sales()


        elif tool == "analyze_sales":
            result = analyze_sales()


        else:
            result = {
                "error": "Unknown tool"
            }


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


    return response
