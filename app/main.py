from fastapi import FastAPI
from .routers import data, plot, screener
app = FastAPI()
app.include_router(data.router)
app.include_router(plot.router)
app.include_router(screener.router)

@app.get("/")
def root():
    return {"message": "Hello World"}

