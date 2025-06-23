from tools.mongodb_tool import MongoDBTool
from agents.support_agent import SupportAgent
from dotenv import load_dotenv
import os

load_dotenv() 

uri = os.getenv("MONGODB_URI")
db_tool = MongoDBTool(uri)
agent = SupportAgent(db_tool)

print(agent.handle_query("What classes are available this week?"))
print(agent.handle_query("Has order #12345 been paid?"))
