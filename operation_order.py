import random
import re
import time
import string
import matplotlib.pyplot as plt
import numpy as np
from model_order import Order
from operation_customer import CustomerOperation

class OrderOperation:
    def generate_unique_order_id(self):
        '''
        Generates unique order ID
        :param: None
        :return: randomly generated order_id if order ID doesn't exist in orders.txt
        '''
        self.order_id = f"o_{random.randint(10000, 99999)}"
        with open("data/orders.txt", "r", encoding='utf-8') as order_file:
            lines = order_file.readlines()
            existing_ids = [line.strip().split(",")[0] for line in lines]  # store all existing order IDs
            while True:
                if self.order_id not in existing_ids:
                    order_file.close()
                    return self.order_id
                else:
                    self.order_id = f"o_{random.randint(10000, 99999)}" # if order ID already exists
                    continue

    def create_an_order(self, customer_id, product_id, create_time=None):
        '''
        Creates a new order and saves it to orders.txt
        :param: customer_id
        :param: product_id
        :param: create_time
        :return: False if order details already exists in orders.txt, otherwise return True
        '''
        customer_id = customer_id
        product_id = product_id
        if create_time is None:
            create_time = time.strftime("%d-%m-%Y_%H:%M:%S")

        # Check for duplicate orders
        with open("data/orders.txt", "r", encoding='utf-8') as f_order:
            existing_orders = f_order.readlines()
            for order_line in existing_orders:
                existing_order = eval(order_line.strip())
                if (
                        existing_order['user_id'] == customer_id
                        and existing_order['pro_id'] == product_id
                        and existing_order['order_time'] == create_time
                ):
                    return False

        order_id = self.generate_unique_order_id()
        new_order = Order(order_id, customer_id, product_id, create_time)

        # Write new order to orders.txt
        with open("data/orders.txt", "a", encoding='utf-8') as f_order:
            f_order.write(str(new_order).strip() + "\n")

        return True

    def delete_order(self, order_id):
        '''
        Deletes an existing order
        :param: order_id
        :return: True if order is found and deleted, False otherwise
        '''
        order_found = self.check_orderid_exist(order_id)  # check if order exists

        with open("data/orders.txt", "r", encoding='utf-8') as order_file:
            lines = order_file.readlines()
            if order_found:
                for line in lines:
                    order_info = eval(line.strip())
                    if order_info["order_id"] == order_id:
                        lines.remove(line)  # delete specific order
                        break
                with open("data/orders.txt", "w", encoding='utf-8') as order_file:
                    order_file.writelines(lines)
                return True
            else:
                return False

    def get_order_list(self, customer_id, page_number):
        '''
        Retrieves one page of orders from orders.txt based on relevant page number
        :param: customer_id
        :param: page_number
        :return: orders, page_number, total_pages
        '''
        orders_per_page = 10
        start_index = (page_number - 1) * orders_per_page
        end_index = start_index + orders_per_page

        with open("data/orders.txt", "r", encoding='utf-8') as order_file:
            lines = order_file.readlines()
            orders = []
            count = 0
            for line in lines:
                order = eval(line.strip())
                if customer_id == "" or order['user_id'] == customer_id:
                    if count >= start_index and count < end_index:
                        orders.append(order) # add to order list
                    count += 1

        total_pages = (count + orders_per_page - 1) // orders_per_page

        return orders, page_number, total_pages


    def generate_test_order_data(self):
        '''
        Randomly generate 10 customers and 50-200 orders for each customer
        :param: None
        :return: None
        '''
        customers = self.generate_random_customers(10)

        products = self.get_all_products()

        # Generate orders for each customer
        for customer in customers:
            customer_id = customer['user_id']
            num_orders = customer['num_orders']

            for _ in range(num_orders):
                # Generate random order information
                product_id = random.choice(products)['pro_id']
                create_time = self.generate_random_order_time()

                # Create an order
                self.create_an_order(customer_id, product_id, create_time)


    def generate_single_customer_consumption_figure(self, customer_id):
        '''
        Generate bar chart showing consumption of 12 different months for a given customer
        :param: customer_id
        :return: None
        '''
        months = [str(i) for i in range(1, 13)]  # List of month numbers from 1 to 12
        consumption = {month: 0 for month in months}  # Dictionary to store the consumption for each month

        # Read and process the orders data
        with open("data/orders.txt", "r", encoding='utf-8') as orders_file:
            for line in orders_file:
                order = eval(line)  # Convert the line to a dictionary
                if order['user_id'] == customer_id:
                    order_time = time.strptime(order['order_time'], "%d-%m-%Y_%H:%M:%S")
                    month = str(order_time.tm_mon) # retrieving month of order
                    pro_id = order['pro_id']
                    order_price = self.get_product_price(pro_id)
                    consumption[month] += order_price # add order price to each respective month

        # Create the graph
        plt.bar(consumption.keys(), consumption.values())
        plt.xlabel('Month')
        plt.ylabel('Total Order Price (USD $)')
        plt.title('Monthly Consumption for Customer ' + customer_id)

        # Save figure
        figure_path = "data/figure/generate_single_customer_consumption_figure.png"
        plt.savefig(figure_path)
        plt.close()

    def generate_all_customers_consumption_figure(self):
        '''
        Generate line graph showing consumption of 12 different months for all customers
        :param: None
        :return: None
        '''
        months = [str(i) for i in range(1, 13)]  # List of month numbers from 1 to 12
        consumption = {month: 0 for month in months}  # Dictionary to store the consumption for each month

        # Read and process the orders data
        with open("data/orders.txt", "r", encoding='utf-8') as orders_file:
            for line in orders_file:
                order = eval(line)  # Convert the line to a dictionary
                order_time = time.strptime(order['order_time'], "%d-%m-%Y_%H:%M:%S")
                month = str(order_time.tm_mon)  # Retrieve the month of the order
                pro_id = order['pro_id']
                order_price = self.get_product_price(pro_id)
                consumption[month] += order_price  # Add the order price to the respective month

        # Create the graph
        plt.plot(consumption.keys(), consumption.values(), marker='o')
        plt.xlabel('Month')
        plt.ylabel('Total Order Price (USD $)')
        plt.title('Monthly Consumption for All Customers')

        # Save figure
        figure_path = "data/figure/generate_all_customers_consumption_figure.png"
        plt.savefig(figure_path)
        plt.close()

    def generate_all_top_10_best_sellers_figure(self):
        '''
        Generate bar chart showing top 10 best-selling products in descending order
        :param: None
        :return: None
        '''
        with open("data/products.txt", "r", encoding='utf-8') as product_file:
            product_lines = product_file.readlines()

        pattern = r"'pro_id': '(.*?)', 'pro_model': '(.*?)', 'pro_category': '(.*?)', 'pro_name': '(.*?)', 'pro_current_price': '(.*?)', 'pro_raw_price': '(.*?)', 'pro_discount': '(.*?)', 'pro_likes_count': '(.*?)'"
        products = []
        for product_line in product_lines:
            match = re.search(pattern, product_line)
            if match:
                product = {
                    'pro_id': match.group(1),
                    'pro_model': match.group(2),
                    'pro_category': match.group(3),
                    'pro_name': match.group(4),
                    'pro_current_price': match.group(5),
                    'pro_raw_price': match.group(6),
                    'pro_discount': match.group(7),
                    'pro_likes_count': match.group(8)
                }
                products.append(product)

        with open("data/orders.txt", "r", encoding='utf-8') as orders_file:
            order_lines = orders_file.readlines()

        product_counts = {}
        for order_line in order_lines:
            order = eval(order_line)
            pro_id = order['pro_id']
            if pro_id in product_counts:
                product_counts[pro_id] += 1
            else:
                product_counts[pro_id] = 1

        # Sort the products by count in descending order
        sorted_products = sorted(products, key=lambda x: product_counts.get(x['pro_id'], 0), reverse=True)

        # Take the top 10 best-selling products
        top_products = sorted_products[:10]

        # Create a list to store truncated names
        truncated_names = []

        # Extract the product names and truncate them
        for product in top_products:
            name = product['pro_name']
            truncated_name = name[:30] + '...' if len(name) > 5 else name

            # Add the truncated name to the list
            truncated_names.append(truncated_name)

        # Create a list to store the final names with indexes for duplicate truncated names
        final_names = []

        # Iterate through truncated names and handle duplicates
        for i, name in enumerate(truncated_names):
            count = truncated_names[:i].count(name)  # Count occurrences of the name before the current index

            if count > 0:
                final_name = f"{name} ({count})"
            else:
                final_name = name

            final_names.append(final_name)

        # Extract the product counts
        product_counts = [product_counts.get(product['pro_id'], 0) for product in top_products]

        # Create the x coordinates for the bars
        x = np.arange(len(final_names))

        # Set the width of the bars
        bar_width = 0.7

        # Set the additional space between the bars
        bar_spacing = 0.3

        # Create the bar plot with adjusted spacing
        plt.figure(figsize=(10, 6))  # Adjust figure size as per your preference
        plt.bar(x, product_counts, width=bar_width, align='center', tick_label=final_names)

        # Rotate the x-axis labels diagonally
        plt.xticks(rotation=45, ha='right', fontsize=8)

        # Add labels and title
        plt.xlabel('Product')
        plt.ylabel('Count')
        plt.title('Top 10 Best-Selling Products')

        # Adjust layout to prevent label cutoff
        plt.tight_layout()

        # Save the figure
        figure_path = "data/figure/generate_all_top_10_best_sellers_figure.png"
        plt.savefig(figure_path)
        plt.close()

    def delete_all_orders(self):
        '''
        Removes all order details from orders.txt
        :param: None
        :return: None
        '''
        with open("data/orders.txt", 'w', encoding='utf-8') as order_file:
            order_file.truncate()


    def check_orderid_exist(self, order_id):
        '''
        Checks if order ID already exists in orders.txt
        :param: order_id
        :return: True if order ID exists in orders.txt, False otherwise
        '''
        self.order_id = order_id
        with open("data/orders.txt", "r", encoding='utf-8') as order_file:
            liner_orderid = []
            for line in order_file:
                order_info = eval(line)  # parse each line/string as dictionary
                found_order = order_info["order_id"]  # extract value of "order_id" key
                liner_orderid.append(found_order) # add to liner_orderid list
            if order_id not in liner_orderid:
                return False
            else:
                return True

    # Randomisation for generate_test_order_data:
    def generate_random_string(self, pattern): # defining patterns for randomisation of username, password, email, phone
        '''
        Generates random variations of username, password, email and mobile for creating test data (customers)
        :param: pattern
        :return: randomly generated username, password, email and mobile values
        '''
        if pattern == r'^[A-Za-z_]{5,}$':
            return ''.join(random.choices(string.ascii_letters + '_', k=random.randint(5, 15)))

        elif pattern == r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{5,}$':
            while True:
                password = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(5, 15)))
                if re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{5,}$', password):
                    return password

        elif pattern == r'^\w+@(?:[a-z]+\.)+(?:com|net|org|edu|gov|int)$':
            username = ''.join(random.choices(string.ascii_lowercase, k=random.randint(5, 10)))
            domain = ''.join(random.choices(string.ascii_lowercase, k=random.randint(5, 10)))
            domain_extension = random.choice(["com", "net", "org", "edu", "gov", "int"])
            return f'{username}@{domain}.{domain_extension}'

        elif pattern == r'^(04|03)\d{8}$':
            return random.choice(['04', '03']) + ''.join(random.choices(string.digits, k=8))

        else:
            # Default case: return a random string of length 10
            return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

    def generate_random_customers(self, num_customers=10):  # creating 10 random customers
        '''
        Generates 10 random customers based on pattern from generate_random_string method
        :param: num_customers = 10
        :return: customers
        '''
        co = CustomerOperation()
        customers = []

        for _ in range(num_customers):
            # Generate random customer information
            user_name = self.generate_random_string(r'^[A-Za-z_]{5,}$')
            user_password = "password123"
            user_email = self.generate_random_string(r'^\w+@(?:[a-z]+\.)+(?:com|net|org|edu|gov|int)$')
            user_mobile = self.generate_random_string(r'^(04|03)\d{8}$')

            # Register the customer
            result = co.register_customer(user_name, user_password, user_email, user_mobile)

            if result:  # Check if registration was successful and generate random number of orders for each customer
                customer = {
                    'user_id': co.get_customer_by_username(user_name)['user_id'],
                    'num_orders': random.randint(50, 200)
                }
                customers.append(customer)

        return customers

    def generate_random_order_time(self):
        '''
        Generates random time for order (only year is fixed)
        :param: None
        :return: randomly generated order date
        '''
        months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
        day = random.randint(1, 28)
        month = random.choice(months)
        year = '2023'  # Adjust the desired year as needed
        hour = random.randint(0, 23)
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        return f"{day}-{month}-{year}_{hour:02d}:{minute:02d}:{second:02d}"

    def get_all_products(self): # retrieving all products from products.txt
        '''
        Retrieves all product data from products.txt
        :param: None
        :return: products
        '''
        with open("data/products.txt", "r", encoding='utf-8') as product_file:
            lines = product_file.readlines()

        products = []
        pattern = r"'pro_id': '(.*?)', 'pro_model': '(.*?)', 'pro_category': '(.*?)', 'pro_name': '(.*?)', 'pro_current_price': '(.*?)', 'pro_raw_price': '(.*?)', 'pro_discount': '(.*?)', 'pro_likes_count': '(.*?)'"
        for line in lines:
            match = re.search(pattern, line)
            if match:
                product = {
                    'pro_id': match.group(1),
                    'pro_model': match.group(2),
                    'pro_category': match.group(3),
                    'pro_name': match.group(4),
                    'pro_current_price': match.group(5),
                    'pro_raw_price': match.group(6),
                    'pro_discount': match.group(7),
                    'pro_likes_count': match.group(8)
                }
                products.append(product)
        return products

    def generate_random_product_id(self):  # randomly selecting products
        '''
        Randomly selects product ID from products list to be included in randomly generated order
        :param: None
        :return: randomly generated product ID
        '''
        products = self.get_all_products()
        product_ids = [product['pro_id'] for product in products]
        return random.choice(product_ids)

    def get_product_price(self, pro_id):
        '''
        Retrieves product price from products.txt
        :param: pro_id
        :return: product current price if found, 0.0 if not found
        '''
        with open("data/products.txt", "r", encoding='utf-8') as product_file:
            lines = product_file.readlines()

        pattern = r"'pro_id': '{}', 'pro_model': '(.*?)', 'pro_category': '(.*?)', 'pro_name': '(.*?)', 'pro_current_price': '(.*?)', 'pro_raw_price': '(.*?)', 'pro_discount': '(.*?)', 'pro_likes_count': '(.*?)'"

        for line in lines:
            match = re.search(pattern.format(pro_id), line)
            if match:
                return float(match.group(4))

        return 0.0  # default price if product not found

    def delete_customer_order(self, customer_id):
        '''
        Deletes customer order from orders.txt (used if customer is deleted by admin)
        :param: customer_id
        :return: True if orders' successfully deleted, False otherwise
        '''
        with open("data/orders.txt", "r", encoding='utf-8') as order_file:
            lines = order_file.readlines()

        orders_to_keep = []
        orders_deleted = False

        for line in lines:
            order_info = eval(line.strip())
            if order_info["user_id"] == customer_id:
                orders_deleted = True
            else:
                orders_to_keep.append(line) # keep remaining others

        if orders_deleted:
            with open("data/orders.txt", "w", encoding='utf-8') as order_file:
                order_file.writelines(orders_to_keep)
            return True
        else:
            return False


    def delete_product_order(self, product_id):
        '''
        Deletes product order from orders.txt (used if product is deleted by admin)
        :param: product_id
        :return: True if orders' successfully deleted, False otherwise
        '''
        with open("data/orders.txt", "r", encoding='utf-8') as order_file:
            lines = order_file.readlines()

        orders_to_keep = []
        orders_deleted = False

        for line in lines:
            order_info = eval(line.strip())
            if order_info["pro_id"] == product_id:
                orders_deleted = True
            else:
                orders_to_keep.append(line) # keep remaining orders

        if orders_deleted:
            with open("data/orders.txt", "w", encoding='utf-8') as order_file:
                order_file.writelines(orders_to_keep)
            return True
        else:
            return False

