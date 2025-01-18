from fastapi import FastAPI
from dotenv import load_dotenv
load_dotenv() #loading the .env file by defualt
from routes import base
app = FastAPI()

app.include_router(base.base_router)
