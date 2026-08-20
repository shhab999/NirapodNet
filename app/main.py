from fast api import FastAPI

app = FastAPI(title="NirapodNet")

@app.get("/")
def root():
    return {
        "system": "NirapodNet",
        "status": "online",
    }