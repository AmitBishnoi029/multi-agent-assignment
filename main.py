from langdetect import detect
from googletrans import Translator

from fastapi import FastAPI, Request
from pydantic import BaseModel
from tools.mongodb_tool import MongoDBTool
from agents.support_agent import SupportAgent
from agents.dashboard_agent import DashboardAgent
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv
import os

load_dotenv()

translator = Translator()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
uri = os.getenv("MONGODB_URI")
db_tool = MongoDBTool(uri)

support_agent = SupportAgent(db_tool)
dashboard_agent = DashboardAgent(db_tool)

class QueryRequest(BaseModel):
    query: str

@app.get("/")
def root():
    return {"message": "FastAPI is working"}

@app.post("/ask-support")
def ask_support(request: QueryRequest):
    print("Received Query:", request.query)

    #here we Skip language detection + translation
    translated_query = request.query.lower()

    response = support_agent.handle_query(translated_query)

    print("Response:", response)
    return {"response": response}

@app.post("/ask-dashboard")
def ask_dashboard(request: QueryRequest):
    original_lang = detect(request.query)
    translated_query = translator.translate(request.query, src=original_lang, dest='en').text

    response = dashboard_agent.handle_query(translated_query)

    if original_lang != 'en':
        response = translator.translate(response, src='en', dest=original_lang).text

    return {"response": response}
