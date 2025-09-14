from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Ecommerce API is running"}
