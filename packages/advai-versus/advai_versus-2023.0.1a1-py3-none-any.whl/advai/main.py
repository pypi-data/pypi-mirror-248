from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    """
    Root GET request.

    Returns:
        dict: A welcome message.
    """
    return {"Hello": "Advai"}
