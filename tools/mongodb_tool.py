from pymongo import MongoClient

class MongoDBTool:
    def __init__(self, uri):
        self.client = MongoClient(uri)
        self.db = self.client["fitnessDB"]

    def find_client(self, identifier):
        return self.db.clients.find_one({
            "$or": [
                {"name": identifier},
                {"email": identifier},
                {"phone": identifier}
            ]
        })

    def get_order_status(self, order_id):
        return self.db.orders.find_one({"order_id": order_id})

    def list_upcoming_classes(self):
        return list(self.db.classes.find({"status": "upcoming"}))

    def get_payment_for_order(self, order_id):
        return self.db.payments.find_one({"order_id": order_id})

    def get_courses_by_instructor(self, instructor):
        return list(self.db.courses.find({"instructor": instructor}))
    def get_pending_dues(self, client_name):
        orders = self.db.orders.find({
        "client": {"$regex": f"^{client_name}$", "$options": "i"}
        })
        due = 0
        for order in orders:
            payment = self.db.payments.find_one({"order_id": order['order_id']})
            if not payment or payment.get("status") != "paid":
                due += order.get("amount", 0)
        return due
        
    def get_attendance_percentage(self, course):
        total = self.db.attendance.count_documents({"course": course})
        if total == 0:
          return 0
        attended = self.db.attendance.count_documents({"course": course, "attended": True})
        return round((attended / total) * 100, 2)


