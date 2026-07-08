from fastapi import FastAPI

from mcp.server import router


app = FastAPI(
    title="ArmorIQ Challenges"
)


app.include_router(router)


@app.get("/")
def home():

    return {
        "status": "running",
        "service": "ArmorIQ MCP Challenge"
    }


@app.get("/api/health")
def health():

    return {
        "status": "ok"
    }
