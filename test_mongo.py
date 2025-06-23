from tools.mongodb_tool import MongoDBTool
from dotenv import load_dotenv
import os

load_dotenv()

uri = os.getenv("MONGODB_URI")
db_tool = MongoDBTool(uri)

#Here I Test client lookup
client = db_tool.find_client("Priya Sharma")
print("Client:", client)

#Here I Test order status
order = db_tool.get_order_status("12345")
print("Order:", order)

#Here I Test upcoming classes
classes = db_tool.list_upcoming_classes()
print("Upcoming Classes:", classes)
