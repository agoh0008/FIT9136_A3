import time
from operation_user import UserOperation
from model_admin import Admin

class AdminOperation:
    def register_admin(self):
        '''
        Creates admin account and adds admin information into users.txt
        :param: None
        :return: None
        '''
        uo = UserOperation()
        user_id = uo.generate_unique_user_id()

        while True:
            user_name = "admin_one"
            user_password = "password1"
            encrypted_password = uo.encrypt_password(user_password)
            admin_pass = self.check_admin_username_exist(user_name)
            if admin_pass is True: # if admin username already exists
                user_name = "admin_two"
                break
            else:
                break

        user_register_time = time.strftime("%d-%m-%Y_%H:%M:%S")
        user_role = "admin"

        new_admin = Admin(user_id, user_name, encrypted_password, user_register_time, user_role)
        with open("data/users.txt", "a", encoding='utf-8') as f_user:
            f_user.write(str(new_admin).strip() + "\n")

    def check_admin_username_exist(self, user_name):
        '''
        Checks if admin username already exists in user.txt
        :param: user_name
        :return: exist
        '''
        uo = UserOperation()
        exist = bool(uo.check_username_exist(user_name))
        return exist

