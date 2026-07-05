from fastapi import FastAPI

app = FastAPI(title= "Enterprise Knowledge Assistant")

@app.get("/")
def root():
    return {"message": "Enterprise Knowledge Assistant API"}