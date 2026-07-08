from fastapi import FastAPI

app = FastAPI(title="First Contact")

@app.get("/")
def home():
    return {
        "challenge": "First Contact",
        "status": "running"
    }
