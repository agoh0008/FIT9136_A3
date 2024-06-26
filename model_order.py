class Order:
    def __init__(self, order_id = "u_12345", user_id = "u_1234567890", pro_id = "1234567", order_time = "00-00-0000_00:00:00"):
        self.order_id = order_id
        self.user_id = user_id
        self.pro_id = pro_id
        self.order_time = order_time

    def __str__(self):
        return str({"order_id": self.order_id, "user_id": self.user_id, "pro_id": self.pro_id, "order_time": self.order_time})


