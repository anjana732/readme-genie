from fastapi import FastAPI

app = Fastapi()

@app.get("/")
def read_root():
    return {"Testing String" : "Hello World !!"}