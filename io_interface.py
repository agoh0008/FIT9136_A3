class IOInterface:
    def get_user_input(self, message, num_of_args):
        '''
        displays user input message and receives user input
        :param: message
        :param: num_of_args
        :return: args
        '''
        user_input = input(message)
        args = user_input.split()[:num_of_args]  # gets required arguments (ignores unwanted ones)
        if len(args) < num_of_args:
            args += [""] * (
                        num_of_args - len(args))  # appends list of empty strings (based on how many args missed out)
        return args

    def main_menu(self):
        '''
        prints Main Menu
        :param: None
        :return: None
        '''
        border = "=" * 37
        menu_title = "|       MAIN MENU        |"

        print(border)
        print(menu_title.center(37, " "))
        print(border)
        print("1. Login")
        print("2. Register as customer")
        print("3. Quit")
        print(border)

    def admin_menu(self):
        '''
        prints Admin Menu
        :param: None
        :return: None
        '''
        border = "+" + "-" * 13 + "+"
        menu_title = "| ADMIN MENU |"

        print(border)
        print(menu_title)
        print(border)
        print("1. Show products")
        print("2. Add customers")
        print("3. Show customers")
        print("4. Show orders")
        print("5. Generate test data")
        print("6. Generate statistical figures")
        print("7. Delete all data")
        print("8. Delete customer using customer id")
        print("9. Delete order using order id")
        print("10. Delete product using product id")
        print("11. Logout")
        print(border)

    def customer_menu(self):
        '''
        prints Customer Menu
        :param: None
        :return: None
        '''
        border = "+" + "-" * 14 + "+"
        menu_title = "| CUSTOMER MENU |"

        print(border)
        print(menu_title)
        print(border)
        print("1. Show profile")
        print("2. Update profile")
        print("3. Show products")
        print("4. Show history orders")
        print("5. Generate all consumption figures")
        print("6. Get product using product id")
        print("7. Logout")
        print(border)

    def show_list(self, user_role, list_type, object_list):
        '''
        Prints either Customers, Products, or Orders list as well as page number and total pages
        :param user_role: User role (customer or admin)
        :param list_type: Type of list (customer, product, or order)
        :param object_list: List of objects to be printed
        :return: None
        '''
        headers = {
            'customer': ['user_id', 'user_name', 'user_password', 'user_register_time', 'user_role', 'user_email', 'user_mobile'],
            'product': ['pro_id', 'pro_model', 'pro_category', 'pro_name', 'pro_current_price', 'pro_raw_price',
                        'pro_discount', 'pro_likes_count'],
            'order': ['order_id', 'user_id', 'pro_id', 'order_time']
        }

        if list_type not in headers:
            return

        if user_role == 'customer' and list_type != 'product' and list_type != 'order':
            return

        if user_role == 'admin' and list_type == 'customer':
            print("Customers:")
        elif list_type == 'product':
            print("Products:")
        elif list_type == 'order':
            print("Orders:")

        data = object_list[0]
        page_number = object_list[1]
        total_pages = object_list[2]

        if not data:
            return

        # Calculate the maximum width for each column
        column_widths = [max(len(str(item.get(field, ''))) for item in data) for field in headers[list_type]]

        # Add extra padding for better alignment
        column_widths = [width + 2 for width in column_widths]

        if list_type == 'customer':
            # Adjust width for user_email and user_mobile columns to ensure proper spacing
            email_index = headers[list_type].index('user_email')
            mobile_index = headers[list_type].index('user_mobile')
            max_email_width = column_widths[email_index]
            max_mobile_width = column_widths[mobile_index]
            if max_email_width + max_mobile_width > sum(column_widths):
                padding = 2  # Minimum padding between user_email and user_mobile
                if max_email_width > max_mobile_width:
                    column_widths[email_index] += padding
                else:
                    column_widths[mobile_index] += padding

        if list_type == 'product':
            # Adjust width for the last four columns in Products list
            last_four_columns = headers[list_type][-4:]
            last_four_indices = [headers[list_type].index(field) for field in last_four_columns]
            for item in data:
                for index in last_four_indices:
                    value = str(item.get(headers[list_type][index], ''))
                    column_widths[index] = max(column_widths[index], len(value))
            column_widths[-4:] = [max(13, width) for width in column_widths[-4:]]

        header_row = "  ".join(
            "{{:^{}}}".format(width).format(field) for field, width in zip(headers[list_type], column_widths))
        print(header_row)
        print("-" * len(header_row))

        for i, item in enumerate(data, start=1):
            row_parts = []
            for field, width in zip(headers[list_type], column_widths):
                value = str(item.get(field, ''))
                if len(value) > width:
                    value = value.replace(' ', '\n')  # Insert line breaks for long values
                row_parts.append("{{:>{}}}".format(width).format(value)) # Format and align value with right alignment and specified width
            row = "  ".join(row_parts)
            print(f"{i}. {row}")
            print()

        print("Page:", page_number)
        print("Total Pages:", total_pages)

    def print_error_message(self, error_source, error_message):
        '''
        prints error message
        :param: error_source
        :param: error_message
        :return: None
        '''
        print(error_source, error_message)

    def print_message(self, message):
        '''
        prints message
        :param: message
        :return: None
        '''
        print(message)

    def print_object(self, target_object):
        '''
        prints object
        :param: target_object
        :return: None
        '''
        if isinstance(target_object, (list, tuple)):
            for item in target_object:
                print(item)
        else:
            print(target_object)

    def attribute_menu(self):
        '''
        prints Attribute Menu for 'Update profile' option in Customer Menu
        :param: None
        :return: None
        '''
        border = "+" + "-" * 31 + "+"
        menu_title = "| ATTRIBUTES THAT YOU CAN UPDATE |"

        print(border)
        print(menu_title)
        print(border)
        print("1. Username")
        print("2. Password")
        print("3. Email")
        print("4. Mobile")
        print(border)

    def admin_product_menu(self):
        '''
        prints Admin Product Menu for 'Show products' option in Admin Menu
        :param: None
        :return: None
        '''
        border = "+" + "-" * 28 + "+"
        menu_title = "| WAYS TO SHOW PRODUCT(S) |"

        print(border)
        print(menu_title)
        print(border)
        print("1. Show products by list")
        print("2. Show product by keyword")
        print(border)

    def admin_delete_all_data_menu(self):
        '''
        prints next action choice for admin after all data is deleted
        :param: None
        :return: None
        '''
        border = "+" + "-" * 28 + "+"
        menu_title = "| DELETION OF ALL DATA - NEXT ACTION |"

        print(border)
        print(menu_title)
        print(border)
        print("1. Regenerate all customers/orders/products data")
        print("2. Log out and exit program completely")
        print(border)

