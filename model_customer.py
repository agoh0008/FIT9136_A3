from model_user import User

class Customer(User):
    def __init__(self, user_id="u_1234567890", user_name="cust_one", user_password="password1", user_register_time="00-00-0000_00:00:00",
                 user_role="customer", user_email="cust1@gmail.com", user_mobile="0412345678"):
        super().__init__(user_id, user_name, user_password, user_register_time, user_role)
        self.user_email = user_email
        self.user_mobile = user_mobile


    def __str__(self):
        return str({"user_id": self.user_id, "user_name": self.user_name, "user_password": self.user_password,
                "user_register_time": self.user_register_time, "user_role": self.user_role,
                "user_email": self.user_email, "user_mobile": self.user_mobile})


