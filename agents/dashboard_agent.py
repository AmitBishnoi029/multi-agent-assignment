from tools.mongodb_tool import MongoDBTool
from datetime import datetime
from bson.regex import Regex
from dateutil import parser

class DashboardAgent:
    def __init__(self, db_tool: MongoDBTool):
        self.db = db_tool

    def handle_query(self, query: str):
        query = query.lower()

        if "revenue" in query:
            return self.get_total_revenue()

        elif "outstanding payments" in query or "pending revenue" in query:
            return self.get_outstanding_payments()

        elif "inactive clients" in query:
            return self.get_inactive_clients()

        elif "active clients" in query:
            return self.get_active_clients()

        elif "birthday" in query:
            return self.get_birthday_reminders()

        elif "new clients" in query and "this month" in query:
            return self.get_new_clients_this_month()

        elif "enrollment trend" in query:
            return self.get_enrollment_trends()

        elif "top services" in query:
            return self.get_top_services()

        elif "completion rate" in query:
            return self.get_course_completion_rates()

        elif "drop-off" in query:
            return self.get_drop_off_rates()

        elif "attendance" in query:
            return self.get_attendance_percentage(query)

        else:
            return "Sorry, I can't answer that query."

    def get_total_revenue(self):
        pipeline = [
            {"$match": {"status": "paid"}},
            {"$group": {"_id": None, "total": {"$sum": "$amount"}}}
        ]
        result = list(self.db.db.payments.aggregate(pipeline))
        if result:
            return f"Total revenue: ₹{result[0]['total']}"
        return "No paid payments found."

    def get_outstanding_payments(self):
        pipeline = [
            {"$match": {"status": {"$ne": "paid"}}},
            {"$group": {"_id": None, "total": {"$sum": "$amount"}}}
        ]
        result = list(self.db.db.payments.aggregate(pipeline))
        if result:
            return f"Outstanding payments: ₹{result[0]['total']}"
        return "No outstanding payments."

    def get_inactive_clients(self):
        inactive = list(self.db.db.clients.find({"status": "inactive"}))
        return f"Inactive clients: {len(inactive)}"

    def get_active_clients(self):
        active = list(self.db.db.clients.find({"status": "active"}))
        return f"Active clients: {len(active)}"

    def get_birthday_reminders(self):
        today = datetime.today().strftime("%m-%d")
        birthdays = list(self.db.db.clients.find({
            "dob": {"$regex": f".*-{today}$"}
        }))
        if not birthdays:
            return "No birthdays today."
        return "Today's birthdays: " + ", ".join(c['name'] for c in birthdays)

    def get_new_clients_this_month(self):
        start = datetime(datetime.today().year, datetime.today().month, 1)
        new_clients = list(self.db.db.clients.find({"created_at": {"$gte": start}}))
        return f"New clients this month: {len(new_clients)}"

    def get_enrollment_trends(self):
        pipeline = [
            {"$group": {"_id": "$course", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        trends = list(self.db.db.orders.aggregate(pipeline))
        return "Enrollment Trends:\n" + "\n".join(f"{t['_id']}: {t['count']}" for t in trends)

    def get_top_services(self):
        pipeline = [
            {"$group": {"_id": "$course", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 3}
        ]
        top = list(self.db.db.orders.aggregate(pipeline))
        return "Top Services:\n" + "\n".join(f"{t['_id']}: {t['count']}" for t in top)

    def get_course_completion_rates(self):
        courses = list(self.db.db.courses.find())
        report = []
        for c in courses:
            total = c.get("total_sessions", 0)
            completed = c.get("completed_sessions", 0)
            if total > 0:
                rate = (completed / total) * 100
                report.append(f"{c['name']}: {rate:.2f}% completed")
        if not report:
            return "No course data available."
        return "Course Completion Rates:\n" + "\n".join(report)

    def get_drop_off_rates(self):
        pipeline = [
            {"$match": {"status": "cancelled"}},
            {"$group": {"_id": "$course", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        dropoffs = list(self.db.db.orders.aggregate(pipeline))
        return "Drop-off Rates:\n" + "\n".join(f"{d['_id']}: {d['count']} cancellations" for d in dropoffs)

    def get_attendance_percentage(self, query):
        import re
        match = re.search(r"for (.+)", query)
        if not match:
            return "Please specify the class name."

        class_name = match.group(1).strip().lower().rstrip("?.!")

        total = self.db.db.attendance.count_documents({
            "course": {"$regex": f"^{class_name}$", "$options": "i"}
        })

        present = self.db.db.attendance.count_documents({
            "course": {"$regex": f"^{class_name}$", "$options": "i"},
            "attended": True
        })

        if total == 0:
            return f"No attendance records for {class_name.title()}."

        percentage = (present / total) * 100
        return f"Attendance for {class_name.title()}: {percentage:.2f}%"
