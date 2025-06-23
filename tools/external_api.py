def create_order(client_name, course_name):
    return {
        "order_id": "ORD123456",
        "client": client_name,
        "course": course_name,
        "status": "pending"
    }

def create_client_enquiry(client_name, email=None):
    return {
        "enquiry_id": "ENQ987654",
        "client": client_name,
        "email": email or "unknown@example.com"
    }
