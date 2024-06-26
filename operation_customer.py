import re
import time
from operation_user import UserOperation
from model_customer import Customer

class CustomerOperation:
    def validate_email(self, user_email):
        '''
        Validates format of customer email is correct
        :param: user_email
        :return: True if format is correct, False otherwise
        '''
        while True:
            if user_email == "":
                return False, "Email cannot be empty."
            else:
                useremail_check = bool(re.match(r'^\w+@(?:[a-z]+\.)+(?:com|net|org|edu|gov|int)$', user_email))
                if useremail_check is False:
                    return False, "Email address must be in the format username@domain.com. " \
                                  "Domains accepted are .com, .net, .org, .edu, .gov and .int only."
                break

        return True, ""


    def validate_mobile(self, user_mobile):
        '''
        Validates format of customer mobile is correct
        :param: user_mobile
        :return: True if format is correct, False otherwise
        '''
        pattern = r'^(04|03)\d{8}$'

        while True:
            if user_mobile == "":
                return False, "Mobile number cannot be empty."
            elif not user_mobile.isdigit():
                return False, "Mobile number should consist only of numbers."
            elif len(user_mobile) != 10:
                return False, "Mobile number should be exactly 10 digits long."
            elif not re.match(pattern, user_mobile):
                return False, "Mobile number should start with '04' or '03'."
            break

        return True, ""

    def register_customer(self, user_name, user_password, user_email, user_mobile):
        '''
        Creates new customer and adds new customer information to users.txt upon creation
        :param: user_name
        :param: user_password
        :param: user_email
        :param: user_mobile
        :return: True if format of all attributes pass validation checks, False otherwise
        '''
        uo = UserOperation()
        user_id = uo.generate_unique_user_id()
        user_register_time = time.strftime("%d-%m-%Y_%H:%M:%S")
        user_role = "customer"

        username_valid, username_error = uo.validate_username(user_name) # check if username already exists and if it's valid format
        password_valid, password_error = uo.validate_password(user_password)
        email_valid, email_error = self.validate_email(user_email)
        mobile_valid, mobile_error = self.validate_mobile(user_mobile)

        error_messages = "" # store error messages

        if not username_valid:
            error_messages += username_error + " "

        if not password_valid:
            error_messages += password_error + " "

        if not email_valid:
            error_messages += email_error + " "

        if not mobile_valid:
            error_messages += mobile_error + " "

        if error_messages:
            return False, error_messages.strip()

        encrypted_password = uo.encrypt_password(user_password)

        new_customer = Customer(user_id, user_name, encrypted_password, user_register_time, user_role, user_email,
                                user_mobile)
        with open("data/users.txt", "a", encoding='utf-8') as f_user:
            f_user.write(str(new_customer).strip() + "\n") # add new customer
        return True, ""


    def update_profile(self, attribute_name, value, customer_object):
        '''
        Lets customer update either username, password, email or mobile
        :param: attribute_name
        :param: value
        :param: customer_object
        :return: True if updated attribute passes validation checks, False otherwise
        '''
        uo = UserOperation()
        error_messages = []  # list to store error messages

        # Validations check for attribute_name and value:
        if attribute_name == "user_name":
            valid, error_message = uo.validate_username(value)
            if not valid:
                error_messages.append(error_message)
                return False, error_messages
            customer_object.user_name = value
        elif attribute_name == "user_password":
            valid, error_message = uo.validate_password(value)
            if not valid:
                error_messages.append(error_message)
                return False, error_messages
            value = uo.encrypt_password(value)
            customer_object.user_password = value
        elif attribute_name == "user_email":
            valid, error_message = self.validate_email(value)
            if not valid:
                error_messages.append(error_message)
                return False, error_messages
            customer_object.user_email = value
        elif attribute_name == "user_mobile":
            valid, error_message = self.validate_mobile(value)
            if not valid:
                error_messages.append(error_message)
                return False, error_messages
            customer_object.user_mobile = value
        else:
            return False, error_messages

        # Update changes to users.txt file:
        with open("data/users.txt", "r", encoding='utf-8') as f:
            lines = f.readlines()
        with open("data/users.txt", "w", encoding='utf-8') as f:
            for line in lines:
                user_info = eval(line.strip())
                if user_info["user_id"] == customer_object.user_id:
                    user_info[attribute_name] = value # update respective attribute name
                f.write(str(user_info) + "\n")

        return True, error_messages

    def delete_customer(self, customer_id):
        '''
        Deletes customer from users.txt based on provided customer ID
        :param: customer_id
        :return: True if customer is not admin and can be deleted, False if customer is either admin or cannot be found
        '''
        uo = UserOperation()
        user_found = uo.check_userid_exist(customer_id)  # check if customer exists
        is_admin = False  # flag variable to track if an admin is encountered

        with open("data/users.txt", "r", encoding='utf-8') as user_file:
            lines = user_file.readlines()
            if user_found: # customer exists
                for line in lines:
                    user_info = eval(line.strip())
                    if str(user_info["user_id"]) == customer_id and user_info["user_role"] == "customer":
                        lines.remove(line)  # delete specific customer
                        break
                    elif str(user_info["user_id"]) == customer_id and user_info["user_role"] == "admin":
                        is_admin = True  # set flag to True if an admin is encountered

                with open("data/users.txt", "w", encoding='utf-8') as user_file:
                    user_file.writelines(lines)

                return not is_admin # returns True if successful deletion because not admin

        return False  # return False if no user is found with the given ID

    def get_customer_list(self, page_number):
        '''
        Retrieves one page of customers from users.txt based on relevant page number
        :param: page_number
        :return: customers, page_number, total_pages
        '''
        customers_per_page = 10
        start_index = (page_number - 1) * customers_per_page
        end_index = start_index + customers_per_page

        with open("data/users.txt", "r", encoding='utf-8') as user_file:
            lines = user_file.readlines()
            customers = []
            for line in lines[start_index:end_index]:
                customer = eval(line.strip())
                if customer["user_role"] == "customer": # skip admin (don't append)
                    customers.append(customer)

        total_pages = (len(lines) + customers_per_page - 1) // customers_per_page # count total number of pages

        return customers, page_number, total_pages

    def delete_all_customers(self):
        '''
        Deletes all customers from users.txt
        :param: None
        :return: None
        '''
        with open("data/users.txt", "r", encoding='utf-8') as user_file:
            lines = user_file.readlines()

        non_customers = [line for line in lines if "'user_role': 'customer'" not in line] # find non-customers

        if len(non_customers) != len(lines):
            with open("data/users.txt", "w", encoding='utf-8') as user_file:
                user_file.writelines(non_customers)

    def get_customer_by_username(self, user_name):
        '''
        Checks if randomly generated new customers have been added and exist in users.txt
        -> used for generate_random_customers in Order Operation class
        :param: user_name
        :return: customer if customer exists in users.txt, None otherwise
        '''
        with open("data/users.txt", "r", encoding='utf-8') as user_file:
            lines = user_file.readlines()
            for line in lines:
                customer = eval(line.strip())
                if customer['user_name'] == user_name:
                    return customer
        # Customer not found:
        return None
