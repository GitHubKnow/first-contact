from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
import json

from agent.agent import ArmorAgent


app = FastAPI(
    title="ArmorIQ Sales Challenge"
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


        <h1>
            ArmorIQ Sales Challenge
        </h1>


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


            const response = await fetch(
                "/execute/" + action
            );


            const data = await response.json();



            document.getElementById("result").innerText =
                JSON.stringify(
                    data,
                    null,
                    2
                );

        }


        </script>



    </body>


    </html>
    """



@app.get("/execute/{action}")
def execute(action: str):


    allowed_actions = [
        "show_sales",
        "analyze_sales"
    ]


    if action not in allowed_actions:

        return JSONResponse(
            {
                "error": "Invalid action"
            },
            status_code=400
        )



    response = agent.execute(action)



    try:

        # Extract MCP text result

        text = response["content"][0]["text"]

        data = json.loads(text)


    except Exception:


        data = response



    return {

        "action": action,

        "verified_by_armoriq": True,

        "data": data

    }



@app.get("/api/health")
def health():

    return {
        "status": "ok"
    }
