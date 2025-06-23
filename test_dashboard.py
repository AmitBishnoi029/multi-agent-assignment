from tools.mongodb_tool import MongoDBTool
from agents.dashboard_agent import DashboardAgent
from dotenv import load_dotenv
import os

load_dotenv() 

uri = os.getenv("MONGODB_URI")
db_tool = MongoDBTool(uri)
agent = DashboardAgent(db_tool)

# Test queries
print(agent.handle_query("How much revenue did we generate this month?"))
print(agent.handle_query("How many inactive clients do we have?"))
print(agent.handle_query("What is the attendance percentage for Pilates?"))
print(agent.handle_query("How many inactive clients do we have?"))
print(agent.handle_query("What is the attendance percentage for Pilates?"))

