from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
import json

from agent.agent import ArmorAgent
from mcp.server import router

app = FastAPI(
    title="ArmorIQ Sales Challenge"
)

# Sales MCP
app.include_router(
    sales_router,
    prefix="/sales"
)

# Data MCP
app.include_router(
    data_router,
    prefix="/data"
)

agent = ArmorAgent()


@app.get("/", response_class=HTMLResponse)
def home():

    return """
    <!DOCTYPE html>
    <html>

    <head>

        <title>ArmorIQ Sales Challenge</title>

        <style>

            body {
                font-family: Arial, sans-serif;
                margin: 40px;
                background: #111;
                color: white;
            }

            h1 {
                margin-bottom: 30px;
            }

            button {
                padding: 15px 25px;
                margin: 10px;
                font-size: 18px;
                cursor: pointer;
            }

            #result {
                margin-top: 30px;
                padding: 20px;
                background: #222;
                border-radius: 10px;
                white-space: pre-wrap;
            }

        </style>

    </head>

    <body>

        <h1>ArmorIQ Sales Challenge</h1>

        <button onclick="run('show_sales')">
            Show Sales
        </button>

        <button onclick="run('analyze_sales')">
            Analyze Sales
        </button>

        <div id="result">
            Waiting...
        </div>

        <script>

        async function run(action) {

            document.getElementById("result").innerText =
                "Executing through ArmorIQ...";

            try {

                const response = await fetch("/execute/" + action);

                const data = await response.json();

                document.getElementById("result").innerText =
                    JSON.stringify(data, null, 2);

            } catch (err) {

                document.getElementById("result").innerText =
                    err.toString();

            }

        }

        </script>

    </body>

    </html>
    """


@app.get("/execute/{action}")
def execute(action: str):

    allowed_actions = [
    "show_sales",
    "analyze_sales",
    "delete_all"
    ]

    if action not in allowed_actions:

        return JSONResponse(
            {
                "error": "Invalid action"
            },
            status_code=400
        )

    try:

        response = agent.execute(action)

        # Handle SDK response (object or dict)
        if hasattr(response, "result"):
            result = response.result
        else:
            result = response.get("result", response)

        # Extract JSON returned by the MCP
        if isinstance(result, dict):
            text = result["content"][0]["text"]
        else:
            text = result.content[0].text

        data = json.loads(text)

        return {
            "action": action,
            "verified_by_armoriq": True,
            "data": data
        }

    except Exception as e:

        return JSONResponse(
            {
                "verified_by_armoriq": False,
                "error": str(e)
            },
            status_code=500
        )


@app.get("/api/health")
def health():

    return {
        "status": "ok"
    }
