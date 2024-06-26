import random
import re
from model_admin import Admin
from model_customer import Customer

class UserOperation:
    def generate_unique_user_id(self):
        '''
        Generates and creates unique user ID for new user
        :param: None
        :return: None
        '''
        self.user_id = f"u_{random.randint(1000000000, 9999999999)}"
        with open("data/users.txt", "r", encoding='utf-8') as user_file:
            lines = user_file.readlines()
            existing_ids = [line.strip().split(",")[0] for line in lines] # store all existing user IDs
            while True:
                if self.user_id not in existing_ids:
                    user_file.close()
                    return self.user_id
                else:
                    self.user_id = f"u_{random.randint(1000000000,999999999)}"
                    continue

    def encrypt_password(self, user_password):
        '''
        Encrypts user password
        :param: user_password
        :return: newly encrypted user password
        '''
        set_1 = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

        random_pass = ''.join(random.choices(set_1, k = len(user_password) * 2)) # generate random string with length = x2 length of user_password

        encrypted_password = ''.join([r1 + r2 + p for r1, r2, p in zip(random_pass[::2], random_pass[1::2], user_password)]) # iterate each character(s) from random_pass and user_password, then join
        return "^^" + encrypted_password + "$$"

    def decrypt_password(self, encrypted_password):
        '''
        Decrypts user password
        :param: encrypted_password
        :return: decrypted_password
        '''
        decrypted_password = ""
        encrypted = encrypted_password[2:-2] # extract encrypted password (excluding "^^" and "$$")

        for i in range(0, len(encrypted), 3): # iterate over encrypted password in steps of 3
            decrypted_password += encrypted[i + 2]  # append character of original password

        return decrypted_password

    def check_username_exist(self, user_name):
        '''
        Checks if username already exists in users.txt
        :param: user_name
        :return: True if username is found in users.txt, False otherwise
        '''
        self.user_name = user_name
        with open("data/users.txt", "r", encoding='utf-8') as user_file:
            liner_username = []
            for line in user_file:
                user_info = eval(line) # parse each line/string as dictionary
                found_user_name = user_info["user_name"] # extract value of "user_name" key
                liner_username.append(found_user_name)
            if user_name not in liner_username:
                return False
            else:
                return True

    def validate_username(self, user_name):
        '''
        Validates format of username is correct
        :param: user_name
        :return: True if format is correct, False otherwise
        '''
        while True:
            if user_name == "":
                return False, "Username cannot be empty."
            if user_name == "_____" or re.match(r'^_+$', user_name):
                return False, "Username must consist of letters."
            username_check = bool(re.match(r'^[A-Za-z_]{5,}$', user_name))
            if username_check is True:
                check_exist = self.check_username_exist(user_name)
                if check_exist is False:
                    return True, ""
                    break
                elif check_exist is True:
                    return False, "Username already exists. Create a new one."
                    break
            else:
                if len(user_name) < 5:
                    return False, "Username needs to be at least 5 characters."
                else:
                    return False, "Username can only contain letters or underscores."
                break

        return True, ""


    def validate_password(self, user_password):
        '''
        Validates format of password is correct
        :param: user_password
        :return: True if format is correct, False otherwise
        '''
        while True:
            if user_password == "":
                return False, "Password cannot be empty."
            userpassword_check = bool(re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{5,}$', user_password))
            if userpassword_check is False:
                if len(user_password) < 5:
                    return False, "Password needs to be at least 5 characters."
                elif re.search(r'[^A-Za-z0-9]', user_password):
                    return False, "Password must not contain symbols."
                else:
                    return False, "Password must contain at least one letter and one number."
                break
            break

        return True, ""


    def login(self, user_name, user_password):
        '''
        Verifies if provided username and password matches information against stored data in users.txt
        Also determines authorization status for accessing the program (i.e. whether it's Customer or Admin)
        :param: user_name
        :param: user_password
        :return: customer if Customer object, admin if Admin object, False if username and password do not match
        '''
        # Check if username exists
        if self.check_username_exist(user_name):
            # Compare provided username and password combination against users data
            with open("data/users.txt", "r", encoding='utf-8') as user_file:
                for line in user_file:
                    user_info = eval(line)
                    if user_info["user_name"] == user_name:
                        # Decrypt the stored password
                        stored_password = self.decrypt_password(user_info["user_password"])
                        if user_password == stored_password:
                            # Return Customer/Admin object based on user role
                            if user_info["user_role"] == "customer":
                                customer = Customer(user_info["user_id"], user_info["user_name"],
                                                    user_info["user_password"],
                                                    user_info["user_register_time"], user_info["user_role"])
                                return customer
                            elif user_info["user_role"] == "admin":
                                admin = Admin(user_info["user_id"], user_info["user_name"], user_info["user_password"],
                                              user_info["user_register_time"], user_info["user_role"])
                                return admin
        return False  # Return False if the username and password do not match

    def check_userid_exist(self, user_id):
        '''
        Checks if user ID exists in users.txt --> used for delete_customer method in Customer Operation class
        :param: user_id
        :return: False if user ID does not exist, True if user ID exists in users.txt
        '''
        self.user_id = user_id
        with open("data/users.txt", "r", encoding='utf-8') as user_file:
            liner_userid = []
            for line in user_file:
                user_info = eval(line) # parse each line/string as dictionary
                found_user = user_info["user_id"] # extract value of "user_id" key
                liner_userid.append(found_user)
            if user_id not in liner_userid:
                return False
            else:
                return True

