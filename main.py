'''
Name: Alexandra Goh
Student ID: 29796431
Creation Date: 21/05/2023
Last Modified Date: 08/06/2023

This is a simple e-commerce information management system which allows admins to add/view/delete customers/products/orders,
generate statistical figures and more whereas customers can view products and history orders,
generate consumption figures and register as a new customer.
'''

from model_admin import Admin
from model_customer import Customer
from model_user import User
from operation_admin import AdminOperation
from operation_customer import CustomerOperation
from operation_order import OrderOperation
from operation_product import ProductOperation
from operation_user import UserOperation
from io_interface import IOInterface
import os


def login_control():
    '''
    controls Main Menu functions
    :param: None
    :return: None
    '''
    io = IOInterface()
    user1 = User()
    uo = UserOperation()
    co = CustomerOperation()
    approve = None

    io.main_menu()
    start = io.get_user_input("Enter number:", 1)[0]  # Access the first element of the returned list

    if start == "1":
        user1.user_name = io.get_user_input("Enter username:", 1)[0]  # Access the first element of the returned list
        user1.user_password = io.get_user_input("Enter password:", 1)[0]  # Access the first element of the returned list
        approve = uo.login(user1.user_name, user1.user_password)  # returns either Customer or Admin object

        if not approve:  # Check if the return value is False
            io.print_error_message("UserOperation.login:", "Invalid username or password. Try again.")
            login_control()
        else:
            io.print_message("Login successful!")
            if isinstance(approve, Customer):
                with open("data/users.txt", "r", encoding='utf-8') as file:
                    lines = file.readlines()
                    for line in lines:
                        user_data = eval(line)
                        if (user_data["user_name"] == approve.user_name and user_data["user_role"] == "customer"):
                            approve.user_email = user_data["user_email"]
                            approve.user_mobile = user_data["user_mobile"]
                            break
                customer_control(approve)
            elif isinstance(approve, Admin):
                admin_control(approve)

    elif start == "2":
        user1.user_name = io.get_user_input("Enter username:", 1)[0]
        user1.user_password = io.get_user_input("Enter password:", 1)[0]
        user1.user_email = io.get_user_input("Enter email:", 1)[0]
        user1.user_mobile = io.get_user_input("Enter mobile:", 1)[0]

        # Perform username, password, email, and mobile validation
        registration_valid, registration_error = co.register_customer(user1.user_name, user1.user_password,
                                                                      user1.user_email, user1.user_mobile)

        if not registration_valid:
            io.print_error_message("CustomerOperation.register_customer:", f"{registration_error}")
            login_control()
        else:
            io.print_message("Registration successful!")
            login_control()

    elif start == "3":
        io.print_message("Exiting program...")
        os._exit(0)

    elif start == "": # check if input is empty
        io.print_message("You did not enter anything.")
        login_control()

    elif approve is None:  # check if the login was unsuccessful
        io.print_message("Invalid option: enter using only the numbers in the menu.")
        login_control()

    else:
        io.print_message("Invalid option: enter using only the numbers in the menu.")
        login_control()


def customer_control(approve):
    '''
    controls Customer Menu functions
    :param: approve
    :return: None
    '''
    io = IOInterface()
    co = CustomerOperation()
    po = ProductOperation()
    op = OrderOperation()

    while True:
        io.customer_menu()
        user_input = io.get_user_input("Enter number:", 2)  # retrieve the entire list
        cust_input = user_input[0]  # access the first element
        keyword = user_input[1]  # access the second element

        if cust_input == "1":
            io.print_object(approve)

        elif cust_input == "2":
            io.attribute_menu()
            attribute_input = io.get_user_input("Enter attribute you wish to update:", 1)[0]
            if attribute_input == "1":
                attribute_name = "user_name"
            elif attribute_input == "2":
                attribute_name = "user_password"
            elif attribute_input == "3":
                attribute_name = "user_email"
            elif attribute_input == "4":
                attribute_name = "user_mobile"
            else:
                io.print_message("Invalid option: enter using only the numbers in the menu.")
                continue  # Go back to the start of the loop

            value = io.get_user_input("Enter new attribute:", 1)[0]
            success, error_messages = co.update_profile(attribute_name, value, approve)

            if not success:
                io.print_message("Invalid input.")
                for error_message in error_messages:
                    io.print_error_message("CustomerOperation.update_profile:", error_message)
            else:
                io.print_message(f"{attribute_name} successfully updated!")
                continue  # Go back to the start of the loop

        elif cust_input.startswith("3"):
            if keyword:
                product = po.get_product_list_by_keyword(keyword)
                io.print_object(product)
                if not product:
                    io.print_error_message("ProductOperation.get_product_list_by_keyword:", f"No products found with keyword = '{keyword}'.")
            else:
                keyword = io.get_user_input("Enter keyword:", 1)[0]
                if keyword:
                    product = po.get_product_list_by_keyword(keyword)
                    io.print_object(product)
                    if not product:
                        io.print_error_message("ProductOperation.get_product_list_by_keyword:",
                                               f"No products found with keyword = '{keyword}'.")
                else:
                    io.print_message("You did not enter any keyword.")
                    continue

        elif cust_input == "4":
            break_flag = False  # Flag variable to control the outer loop
            while True:
                page_number_list = io.get_user_input("Enter page number for order list:", 1)
                if page_number_list and page_number_list[0].isdigit():
                    page_number = int(page_number_list[0])
                    customer_id = approve.user_id
                    user_role = approve.user_role
                    object_list = op.get_order_list(customer_id, page_number)
                    list_type = "order"
                    if object_list is None:
                        io.print_error_message("OrderOperation.get_order_list:",
                                               f"please enter a page number from 1 to {page_number}.")
                    else:
                        order_list = io.show_list(user_role, list_type, object_list)
                        total_pages = object_list[2]
                        if page_number > total_pages and total_pages != 0:
                            io.print_message(
                                f"Invalid page number: please enter a page number from 1 to {total_pages}.")
                        elif page_number == 0 and total_pages != 0:
                            io.print_message(
                                f"Invalid page number: please enter a page number from 1 to {total_pages}.")
                        elif page_number >= 0 and total_pages == 0:
                            io.print_message(f"Invalid page number: you have no orders placed yet.")

                        # Allow navigation to previous or next page only if the page number is valid
                        if 1 <= page_number <= total_pages:
                            while True:
                                navigation_input = io.get_user_input(
                                    "Enter 'p' for previous page, 'n' for next page, or 'q' to quit:", 1)
                                if navigation_input and navigation_input[0].lower() == "p":
                                    if page_number > 1:
                                        page_number -= 1
                                        object_list = op.get_order_list(customer_id, page_number)
                                        if object_list is None:
                                            io.print_error_message("OrderOperation.get_order_list:",
                                                                   f"please enter a page number from 1 to {page_number}.")
                                        else:
                                            order_list = io.show_list(user_role, list_type, object_list)
                                    else:
                                        io.print_message("You are already on the first page.")
                                elif navigation_input and navigation_input[0].lower() == "n":
                                    if page_number < total_pages:
                                        page_number += 1
                                        object_list = op.get_order_list(customer_id, page_number)
                                        if object_list is None:
                                            io.print_error_message("OrderOperation.get_order_list:",
                                                                   f"please enter a page number from 1 to {page_number}.")
                                        else:
                                            order_list = io.show_list(user_role, list_type, object_list)
                                    else:
                                        io.print_message("You are already on the last page.")
                                elif navigation_input and navigation_input[0].lower() == "q":
                                    break_flag = True
                                    break  # Break out of the inner loop
                                else:
                                    io.print_message("Invalid input. Please try again.")
                            if break_flag:
                                break  # Break out of the outer loop
                elif page_number_list and page_number_list[0] == "":
                    io.print_message("You did not enter a page number.")
                    continue
                else:
                    io.print_message("Invalid page number.")
                    continue

        elif cust_input == "5":
            customer_id = approve.user_id
            order_found = False
            with open("data/orders.txt", "r", encoding='utf-8') as orders_file:
                for line in orders_file:
                    order = eval(line)  # Convert the line to a dictionary
                    if order['user_id'] == customer_id:
                        op.generate_single_customer_consumption_figure(customer_id)
                        io.print_message(f"Consumption figure generated for {customer_id}! Check data/figure folder.")
                        order_found = True
                        break
            if not order_found:
                io.print_error_message("OrderOperation.generate_single_customer_consumption_figure:",
                                       f"Customer {customer_id} has not placed any orders yet.")

        elif cust_input == "6":
            product_id = io.get_user_input("Enter product ID:", 1)[0]
            product = None  # Initialize product with None
            if product_id:
                product = po.get_product_by_id(product_id)
                if not product:
                    io.print_error_message("ProductOperation.get_product_by_id:",
                                           f"No products found with product ID = '{product_id}'.")
                else:
                    io.print_object(product)
            else:
                io.print_message("You did not enter a product ID.")

        elif cust_input == "7":
            io.print_message("Logging out...")
            return login_control()

        elif cust_input == "":
            io.print_message("You did not enter anything.")

        else:
            io.print_message("Invalid option: enter using only the numbers in the menu.")


def admin_control(approve):
    '''
    controls Admin Menu functions
    :param: approve
    :return: None
    '''
    io = IOInterface()
    ad = Admin()
    ao = AdminOperation()
    co = CustomerOperation()
    po = ProductOperation()
    op = OrderOperation()

    admin_product_choice = None  # Assign a default value outside the loop

    while True:
        io.admin_menu()
        user_input = io.get_user_input("Enter number:", 5)  # retrieve the entire list
        admin_input = user_input[0]  # access the first element
        user_name = user_input[1]
        user_password = user_input[2]
        user_email = user_input[3]
        user_mobile = user_input[4]

        if admin_input == "1":
            io.admin_product_menu()
            admin_product_choice = io.get_user_input("Do you wish to show product(s) by list or by keyword:", 1)[0]
            # Option 1 for admin_menu:
            if admin_product_choice == "1":
                while True:
                    page_number_list = io.get_user_input("Enter page number for product list:", 1)
                    if page_number_list and page_number_list[0].isdigit():
                        page_number = int(page_number_list[0])
                        user_role = approve.user_role
                        object_list = po.get_product_list(page_number)
                        list_type = "product"
                        if object_list is None:
                            io.print_error_message("ProductOperation.get_product_list:",
                                                   f"please enter a page number from 1 to {page_number}.")
                        else:
                            product_list = io.show_list(user_role, list_type, object_list)
                            total_pages = object_list[2]
                            if page_number == 0 or page_number > total_pages:
                                io.print_message(
                                    f"Invalid page number: please enter a page number from 1 to {total_pages}.")
                            else:
                                break
                    elif page_number_list and page_number_list[0] == "":
                        io.print_message("You did not enter a page number.")
                    else:
                        io.print_message("Invalid page number.")

                # Allow navigation to previous or next page
                while True:
                    navigation_input = io.get_user_input(
                        "Enter 'p' for previous page, 'n' for next page, or 'q' to quit:", 1)
                    if navigation_input and navigation_input[0].lower() == "p":
                        if page_number > 1:
                            page_number -= 1
                            object_list = po.get_product_list(page_number)
                            if object_list is None:
                                io.print_error_message("ProductOperation.get_product_list:",
                                                       f"please enter a page number from 1 to {page_number}.")
                            else:
                                product_list = io.show_list(user_role, list_type, object_list)
                        else:
                            io.print_message("You are already on the first page.")
                    elif navigation_input and navigation_input[0].lower() == "n":
                        if page_number < total_pages:
                            page_number += 1
                            object_list = po.get_product_list(page_number)
                            if object_list is None:
                                io.print_error_message("ProductOperation.get_product_list:",
                                                       f"please enter a page number from 1 to {page_number}.")
                            else:
                                product_list = io.show_list(user_role, list_type, object_list)
                        else:
                            io.print_message("You are already on the last page.")
                    elif navigation_input and navigation_input[0].lower() == "q": # go back admin menu
                        break
                    else:
                        io.print_message("Invalid input. Please try again.")
            elif admin_product_choice == "2":
                keyword = io.get_user_input("Enter keyword:", 1)[0]
                if keyword:
                    product = po.get_product_list_by_keyword(keyword)
                    io.print_object(product)
                    if not product:
                        io.print_error_message("ProductOperation.get_product_list_by_keyword:",
                                               f"No products found with keyword = '{keyword}'.")
                else:
                    io.print_message("You did not enter any keyword.")
            elif admin_product_choice == "":
                io.print_message("You did not enter anything.")
            else:
                io.print_message("Invalid option: enter using only the numbers in the menu.")
                continue


        elif admin_input.startswith("2"):
            if user_name and user_password and user_email and user_mobile:
                registration_valid, registration_error = co.register_customer(user_name, user_password, user_email,
                                                                          user_mobile)
                if not registration_valid:
                    io.print_error_message("CustomerOperation.register_customer:", f"{registration_error}")
                    continue
                else:
                    io.print_message(f"New customer '{user_name}' added!")
                    continue
            else:
                while not user_name or not user_password or not user_email or not user_mobile:
                    if not user_name:
                        user_name = io.get_user_input("Enter username:", 1)[0]
                        if not user_name:
                            io.print_message("You did not enter a username.")

                    if not user_password:
                        user_password = io.get_user_input("Enter password:", 1)[0]
                        if not user_password:
                            io.print_message("You did not enter a password.")

                    if not user_email:
                        user_email = io.get_user_input("Enter email:", 1)[0]
                        if not user_email:
                            io.print_message("You did not enter an email.")

                    if not user_mobile:
                        user_mobile = io.get_user_input("Enter mobile:", 1)[0]
                        if not user_mobile:
                            io.print_message("You did not enter a mobile number.")

                if user_name and user_password and user_email and user_mobile:
                    registration_valid, registration_error = co.register_customer(user_name, user_password, user_email,
                                                                                  user_mobile)
                    if not registration_valid:
                        io.print_error_message("CustomerOperation.register_customer:", f"{registration_error}")
                        continue
                    else:
                        io.print_message(f"New customer '{user_name}' added!")
                        continue


        elif admin_input == "3":
            break_flag = False  # Flag variable to control the outer loop
            while True:
                page_number_list = io.get_user_input("Enter page number for customer list:", 1)
                if page_number_list and page_number_list[0].isdigit():
                    page_number = int(page_number_list[0])
                    user_role = approve.user_role
                    object_list = co.get_customer_list(page_number)
                    list_type = "customer"
                    if object_list is None:
                        io.print_error_message("CustomerOperation.get_customer_list:",
                                               f"please enter a page number from 1 to {page_number}.")
                        continue
                    else:
                        cust_list = io.show_list(user_role, list_type, object_list)
                        total_pages = object_list[2]
                        if page_number > total_pages and total_pages != 0:
                            io.print_message(
                                f"Invalid page number: please enter a page number from 1 to {total_pages}.")
                        elif page_number == 0 and total_pages != 0:
                            io.print_message(
                                f"Invalid page number: please enter a page number from 1 to {total_pages}.")

                        if 1 <= page_number <= total_pages:
                            while True:
                                navigation_input = io.get_user_input(
                                    "Enter 'p' for previous page, 'n' for next page, or 'q' to quit:", 1)
                                if navigation_input and navigation_input[0].lower() == "p":
                                    if page_number > 1:
                                        page_number -= 1
                                        object_list = co.get_customer_list(page_number)
                                        if object_list is None:
                                            io.print_error_message("OrderOperation.get_order_list:",
                                                                   f"please enter a page number from 1 to {page_number}.")
                                        else:
                                            cust_list = io.show_list(user_role, list_type, object_list)
                                    else:
                                        io.print_message("You are already on the first page.")
                                elif navigation_input and navigation_input[0].lower() == "n":
                                    if page_number < total_pages:
                                        page_number += 1
                                        object_list = co.get_customer_list(page_number)
                                        if object_list is None:
                                            io.print_error_message("OrderOperation.get_order_list:",
                                                                   f"please enter a page number from 1 to {page_number}.")
                                        else:
                                            cust_list = io.show_list(user_role, list_type, object_list)
                                    else:
                                        io.print_message("You are already on the last page.")
                                elif navigation_input and navigation_input[0].lower() == "q":  # go back admin menu
                                    break_flag = True  # Set flag to break the outer loop
                                    break  # Break out of the inner loop
                                else:
                                    io.print_message("Invalid input. Please try again.")
                            if break_flag:
                                break  # Break out of the outer loop
                elif page_number_list and page_number_list[0] == "":
                    io.print_message("You did not enter a page number.")
                    continue
                else:
                    io.print_message("Invalid page number.")
                    continue


        elif admin_input == "4":
            break_flag = False  # Flag variable to control the outer loop
            while True:
                page_number_list = io.get_user_input("Enter page number for order list:", 1)
                if page_number_list and page_number_list[0].isdigit():
                    page_number = int(page_number_list[0])
                    customer_id = ""  # set to empty string to get all orders
                    user_role = approve.user_role
                    object_list = op.get_order_list(customer_id, page_number)
                    list_type = "order"
                    if object_list is None:
                        io.print_error_message("OrderOperation.get_order_list:",
                                               f"please enter a page number from 1 to {page_number}.")
                        continue
                    else:
                        order_list = io.show_list(user_role, list_type, object_list)
                        total_pages = object_list[2]
                        if page_number > total_pages and total_pages != 0:
                            io.print_message(
                                f"Invalid page number: please enter a page number from 1 to {total_pages}.")
                        elif page_number == 0 and total_pages != 0:
                            io.print_message(
                                f"Invalid page number: please enter a page number from 1 to {total_pages}.")

                        if 1 <= page_number <= total_pages:
                            while True:
                                navigation_input = io.get_user_input(
                                    "Enter 'p' for previous page, 'n' for next page, or 'q' to quit:", 1)
                                if navigation_input and navigation_input[0].lower() == "p":
                                    if page_number > 1:
                                        page_number -= 1
                                        object_list = op.get_order_list(customer_id, page_number)
                                        if object_list is None:
                                            io.print_error_message("OrderOperation.get_order_list:",
                                                                   f"please enter a page number from 1 to {page_number}.")
                                        else:
                                            order_list = io.show_list(user_role, list_type, object_list)
                                    else:
                                        io.print_message("You are already on the first page.")
                                elif navigation_input and navigation_input[0].lower() == "n":
                                    if page_number < total_pages:
                                        page_number += 1
                                        object_list = op.get_order_list(customer_id, page_number)
                                        if object_list is None:
                                            io.print_error_message("OrderOperation.get_order_list:",
                                                                   f"please enter a page number from 1 to {page_number}.")
                                        else:
                                            order_list = io.show_list(user_role, list_type, object_list)
                                    else:
                                        io.print_message("You are already on the last page.")
                                elif navigation_input and navigation_input[0].lower() == "q":  # go back admin menu
                                    break_flag = True  # Set flag to break the outer loop
                                    break  # break out of the inner loop
                                else:
                                    io.print_message("Invalid input. Please try again.")
                            if break_flag:
                                break  # Break out of the outer loop
                elif page_number_list and page_number_list[0] == "":
                    io.print_message("You did not enter a page number.")
                    continue
                else:
                    io.print_message("Invalid page number.")
                    continue


        elif admin_input == "5":
            op.generate_test_order_data()
            io.print_message("Test data successfully generated!")
            continue

        elif admin_input == "6":
            po.generate_category_figure()
            io.print_message("Category figure successfully generated!")
            po.generate_discount_figure()
            io.print_message("Discount figure successfully generated!")
            po.generate_likes_count_figure()
            io.print_message("Likes Count figure successfully generated!")
            po.generate_discount_likes_count_figure()
            io.print_message("Discount vs. Likes Count figure successfully generated!")
            op.generate_all_customers_consumption_figure()
            io.print_message("All Customers' Consumption figure successfully generated!")
            op.generate_all_top_10_best_sellers_figure()
            io.print_message("All Top 10 Best Sellers figure successfully generated!")

        elif admin_input == "7":
            co.delete_all_customers()
            io.print_message("All customers successfully deleted!")
            po.delete_all_products()
            io.print_message("All products successfully deleted!")
            op.delete_all_orders()
            io.print_message("All orders successfully deleted!")
            io.admin_delete_all_data_menu()
            io.print_message("Would you like to regenerate all data again, or exit program?")
            extract_choice = io.get_user_input("Enter choice:", 1)[0]
            if extract_choice == "1":
                po.extract_products_from_files()
                op.generate_test_order_data()
                io.print_message("All data successfully generated!")
            elif extract_choice == "2":
                io.print_message("Logging out and exiting program...")
                os._exit(0)
            elif extract_choice == "":
                io.print_message("You did not enter anything.")
            else:
                io.print_message("Invalid option: enter using only the numbers shown in the menu.")


        elif admin_input == "8":
            customer_id = io.get_user_input("Enter customer ID to delete:", 1)[0]
            if customer_id:
                deletion_successful = co.delete_customer(customer_id)
                order_deleted = op.delete_customer_order(customer_id) # delete related orders of that specific deleted customer
                if deletion_successful or order_deleted:
                    io.print_message(f"Customer with customer ID = {customer_id} successfully deleted!")
                    io.print_message(f"Orders containing customer ID = {customer_id} also successfully deleted!")
                else:
                    with open("data/users.txt", "r", encoding='utf-8') as user_file:
                        lines = user_file.readlines()
                        customer_exists = False
                        admin_exists = False
                        for line in lines:
                            user_info = eval(line.strip())
                            if str(user_info["user_id"]) == customer_id and user_info["user_role"] == "customer":
                                customer_exists = True
                            elif str(user_info["user_id"]) == customer_id and user_info["user_role"] == "admin":
                                admin_exists = True
                        if admin_exists:
                            io.print_error_message("CustomerOperation.delete_customer:", "Cannot delete admin.")
                        elif not customer_exists:
                            io.print_error_message("CustomerOperation.delete_customer:", f"No customer existing with customer ID = {customer_id}.")
            else:
                io.print_message("You did not enter a customer ID.")


        elif admin_input == "9":
            order_id = io.get_user_input("Enter order ID to delete:", 1)[0]
            if order_id:
                deletion_successful = op.delete_order(order_id)
                if deletion_successful:
                    io.print_message(f"Order with order ID = {order_id} successfully deleted!")
                else:
                    io.print_error_message("OrderOperation.delete_order:", f"No order existing with order ID = {order_id}.")
            else:
                io.print_message("You did not enter an order ID.")


        elif admin_input == "10":
            product_id = io.get_user_input("Enter product ID to delete:", 1)[0]
            if product_id:
                deletion_successful = po.delete_product(product_id)
                product_deleted = op.delete_product_order(product_id) # delete related orders of that specific product
                if deletion_successful or product_deleted:
                    io.print_message(f"Product with product ID = {product_id} successfully deleted!")
                    io.print_message(f"Orders containing product ID = {product_id} also successfully deleted!")
                else:
                    io.print_error_message("ProductOperation.delete_product:",
                                           f"No product existing with product ID = {product_id}.")
            else:
                io.print_message("You did not enter a product ID.")


        elif admin_input == "11":
            io.print_message("Logging out...")
            return login_control()

        elif admin_input == "":
            io.print_message("You did not enter anything.")
            continue

        else:
            io.print_message("Invalid option: enter using only the numbers in the menu.")
            continue


def main():
    '''
    main function
    :param: None
    :return: None
    '''
    po = ProductOperation()
    op = OrderOperation()

    # Extract products from files
    po.extract_products_from_files()
    op.generate_test_order_data()

    def begin():
        ao = AdminOperation()
        ao.register_admin()
        login_control()

    begin()

if __name__ == "__main__":
    main()

