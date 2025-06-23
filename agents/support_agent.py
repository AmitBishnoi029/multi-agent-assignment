from tools.mongodb_tool import MongoDBTool
from googletrans import Translator
from datetime import datetime
import re
from tools.external_api import create_order, create_client_enquiry

class SupportAgent:
    def __init__(self, db_tool):
        self.db = db_tool
        self.translator = Translator()

    def handle_query(self, query: str):
        print("Query received:", query)

        try:
            if "create an order" in query:
                print("Running _create_order")
                return self._create_order(query)

            elif "create enquiry" in query or "new client" in query:
                print("Running _create_client_enquiry")
                return self._create_client_enquiry(query)

            elif "pending due" in query or "how much does" in query:
                print("Running _calculate_pending_dues")
                return self._calculate_pending_dues(query)

            elif "class" in query or "classes" in query:
                print("Running _list_upcoming_classes")
                return self._list_upcoming_classes()

            elif "order" in query:
                print("Running _check_order_status")
                return self._check_order_status(query)

            else:
                print("Fallback triggered")
                return "Sorry, I couldn't understand your request."

        except Exception as e:
            print("ERROR in handle_query:", str(e))
            return "An internal error occurred."

    def _list_upcoming_classes(self):
        classes = self.db.list_upcoming_classes()
        if not classes:
            return "No upcoming classes found."

        formatted_classes = []
        for c in classes:
            course = c['course']
            dt = datetime.fromisoformat(c['schedule'].replace('Z', '+00:00'))
            date_str = dt.strftime("%A, %d %B %Y")
            time_str = dt.strftime("%I:%M %p")
            formatted_classes.append(f"{course} - {date_str} at {time_str}")

        return "\n".join(formatted_classes)

    def _check_order_status(self, query):
        match = re.search(r"#?(\d+)", query)
        if not match:
            return "No order ID found in your query."

        order_id = match.group(1)
        order = self.db.get_order_status(order_id)
        if not order:
            return f"No order found with ID {order_id}."
        return f"Order #{order_id} status: {order['status']}"

    def _create_order(self, query):
        match = re.search(r'order for (.+) for client (.+)', query)
        if not match:
            return "Please specify course and client name."

        course = match.group(1).strip()
        client = match.group(2).strip()
        order = create_order(client, course)
        return f"Order created: {order}"

    def _create_client_enquiry(self, query):
        match = re.search(r'client (.+)', query)
        if not match:
            return "Please provide client name."

        client = match.group(1).strip()
        enquiry = create_client_enquiry(client)
        return f"Enquiry created: {enquiry}"

    def _calculate_pending_dues(self, query):
        match = re.search(r'for (.+)', query)
        if not match:
            return "Please provide client name."

        client = match.group(1).strip()
        total_due = self.db.get_pending_dues(client)
        return f"{client} has ₹{total_due} pending dues."
