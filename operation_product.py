import os
import pandas as pd
import re
import matplotlib.pyplot as plt

class ProductOperation:

    def extract_products_from_files(self):
        '''
        Retrieves all product information from .csv files
        :param: None
        :return: None
        '''

        product_folder = "data/product"
        product_files = ["accessories.csv", "bags.csv", "beauty.csv", "house.csv", "jewelry.csv", "kids.csv", "men.csv", "shoes.csv", "women.csv"]
        product_data = []  # list to store extracted product information

        # Define desired attributes to extract from CSV files
        desired_attributes = ["category", "name", "current_price", "raw_price", "discount", "likes_count", "id",
                              "model"]

        # Iterate over each CSV file
        for file_name in product_files:
            # create full path to CSV file with forward slashes "/"
            file_path = os.path.join(product_folder, file_name).replace("\\", "/")

            # Read CSV file into pandas DataFrame
            df = pd.read_csv(file_path)
            columns = df.columns # get columns

            attribute_indices = [columns.get_loc(attr) for attr in desired_attributes] # get indices of desired attributes

            # Iterate over rows to extract product data
            for _, row in df.iterrows():
                product = {} # dictionary to store product information
                for index, attribute in zip(attribute_indices, desired_attributes):
                    if index < len(row): # check if the index is valid for the row
                        value = row[index]
                        # Add attribute and value to product dictionary
                        product[attribute] = value

                # Add product dictionary to product_data list
                product_data.append(product)

        # Write product_data list to products.txt
        with open("data/products.txt", "w", encoding="utf-8") as file:
            for product in product_data:
                # Create string in desired format
                formatted_product = f"{{'pro_id': '{product.get('id')}', 'pro_model': '{product.get('model')}', 'pro_category': '{product.get('category')}', 'pro_name': '{product.get('name')}', 'pro_current_price': '{product.get('current_price')}', 'pro_raw_price': '{product.get('raw_price')}', 'pro_discount': '{product.get('discount')}', 'pro_likes_count': '{product.get('likes_count')}'}}"
                file.write(formatted_product + "\n")


    def get_product_list(self, page_number):
        '''
        Retrieves one page of products from products.txt (contains 10 products per page)
        :param: page_number
        :return: products, page_number, total_pages
        '''
        products_per_page = 10
        start_index = (page_number - 1) * products_per_page
        end_index = start_index + products_per_page

        with open("data/products.txt", "r", encoding='utf-8') as product_file:
            lines = product_file.readlines()
            products = []
            pattern = r"{'pro_id': '(.*?)', 'pro_model': '(.*?)', 'pro_category': '(.*?)', 'pro_name': '(.*?)', 'pro_current_price': '(.*?)', 'pro_raw_price': '(.*?)', 'pro_discount': '(.*?)', 'pro_likes_count': '(.*?)'}"
            for line in lines[start_index:end_index]:
                match = re.match(pattern, line)
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

        total_pages = (len(lines) + products_per_page - 1) // products_per_page  # count total number of pages

        return products, page_number, total_pages


    def delete_product(self, product_id):
        '''
        Deletes product from products.txt
        :param: product_id
        :return: True if product successfully deleted, False otherwise
        '''
        product_found = self.check_productid_exist(product_id)  # check if product exists

        if product_found:
            with open("data/products.txt", "r", encoding='utf-8') as product_file:
                lines = product_file.readlines()

            with open("data/products.txt", "w", encoding='utf-8') as product_file:
                for line in lines:
                    if "'pro_id': '" + str(product_id) + "'" not in line:
                        product_file.write(line)

            return True
        else:
            return False


    def get_product_list_by_keyword(self, keyword):
        '''
        Retrieves all products whose name contains the given keyword
        :param: keyword
        :return: products
        '''
        with open("data/products.txt", "r", encoding='utf-8') as product_file:
            lines = product_file.readlines()

        products = []
        keyword_lower = keyword.lower()  # convert keyword to lowercase for case-insensitive comparison

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
                product_name = product[
                    'pro_name'].lower()  # convert product name to lowercase for case-insensitive comparison
                if re.search(r'\b{}\b'.format(re.escape(keyword_lower)), product_name):
                    if keyword_lower in product_name.split():  # check if exact word exists in the product name
                        products.append(product)
        return products


    def get_product_by_id(self, product_id):
        '''
        Retrieves product based on given product ID
        :param: product_id
        :return: product if product_id exists in products.txt, False otherwise
        '''
        with open("data/products.txt", "r", encoding='utf-8') as product_file:
            lines = product_file.readlines()

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
                if product_id == product['pro_id']:
                    return product
        # Product not found:
        return None

    def generate_category_figure(self):
        '''
        Generates bar chart showing total number of products for each category in descending order
        :param: None
        :return: None
        '''

        category_counts = {} # collect category data and counts

        with open("data/products.txt", "r", encoding='utf-8') as product_file:
            lines = product_file.readlines()

        pattern = r"'pro_id': '(.*?)', 'pro_model': '(.*?)', 'pro_category': '(.*?)', 'pro_name': '(.*?)', 'pro_current_price': '(.*?)', 'pro_raw_price': '(.*?)', 'pro_discount': '(.*?)', 'pro_likes_count': '(.*?)'"
        for line in lines:
            match = re.search(pattern, line)
            if match:
                category = match.group(3)
                if category in category_counts:
                    category_counts[category] += 1
                else:
                    category_counts[category] = 1

        # Sort categories in descending order
        sorted_categories = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)
        categories, counts = zip(*sorted_categories)

        # Generate bar chart
        plt.bar(categories, counts, linewidth = 1.5)
        plt.xlabel("Category")
        plt.ylabel("Number of Products")
        plt.title("Total Number of Products by Category")
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Save figure
        figure_path = "data/figure/generate_category_figure.png"
        plt.savefig(figure_path)
        plt.close()


    def generate_discount_figure(self):
        '''
        Generates pie chart showing proportion of products based on discount value range
        :param: None
        :return: None
        '''

        # Collect discount data and counts
        discount_counts = {
            "Less than 30%": 0,
            "30% to 60%": 0,
            "Greater than 60%": 0
        }

        with open("data/products.txt", "r", encoding='utf-8') as product_file:
            lines = product_file.readlines()

        pattern = r"'pro_id': '(.*?)', 'pro_model': '(.*?)', 'pro_category': '(.*?)', 'pro_name': '(.*?)', 'pro_current_price': '(.*?)', 'pro_raw_price': '(.*?)', 'pro_discount': '(.*?)', 'pro_likes_count': '(.*?)'"
        for line in lines:
            match = re.search(pattern, line)
            if match:
                discount = float(match.group(7))
                if discount < 30:
                    discount_counts["Less than 30%"] += 1
                elif 30 <= discount <= 60:
                    discount_counts["30% to 60%"] += 1
                else:
                    discount_counts["Greater than 60%"] += 1

        # Get counts and labels for pie chart
        counts = list(discount_counts.values())
        labels = list(discount_counts.keys())

        # Generate pie chart
        pie, texts, _ = plt.pie(counts, startangle=90, autopct='%1.1f%%')
        plt.axis('equal')
        plt.title("Proportion of Products by Discount Range")
        plt.tight_layout()

        # Create legend for labels
        plt.legend(pie, labels, loc="best")

        # Save figure
        figure_path = "data/figure/generate_discount_figure.png"
        plt.savefig(figure_path)
        plt.close()


    def generate_likes_count_figure(self):
        '''
        Generates bar chart showing total likes count for each category
        :param: None
        :return: None
        '''
        category_likes = {}

        with open("data/products.txt", "r", encoding='utf-8') as product_file:
            lines = product_file.readlines()

        pattern = r"'pro_id': '(.*?)', 'pro_model': '(.*?)', 'pro_category': '(.*?)', 'pro_name': '(.*?)', 'pro_current_price': '(.*?)', 'pro_raw_price': '(.*?)', 'pro_discount': '(.*?)', 'pro_likes_count': '(.*?)'"
        for line in lines:
            match = re.search(pattern, line)
            if match:
                category = match.group(3)
                likes_count = int(match.group(8))
                if category in category_likes:
                    category_likes[category] += likes_count
                else:
                    category_likes[category] = likes_count

        # Sort categories based on sum of likes_count in ascending order
        sorted_categories = sorted(category_likes, key=category_likes.get)

        # Get sum of likes_count for each category in ascending order
        likes_counts = [category_likes[category] for category in sorted_categories]

        # Generate bar chart
        plt.bar(range(len(sorted_categories)), likes_counts, align='center')
        plt.xticks(range(len(sorted_categories)), sorted_categories, rotation=45)
        plt.xlabel('Category')
        plt.ylabel('Likes Count (millions)')
        plt.title('Total Products\' Likes Count by Category')
        plt.tight_layout()

        # Save the figure
        figure_path = "data/figure/generate_likes_count_figure.png"
        plt.savefig(figure_path)
        plt.close()

    def generate_discount_likes_count_figure(self):
        '''
        Generates scatter chart showing relationship between likes count and discount for all products
        :param: None
        :return: None
        '''
        likes_counts = []
        discounts = []

        with open("data/products.txt", "r", encoding='utf-8') as product_file:
            lines = product_file.readlines()

        pattern = r"'pro_id': '(.*?)', 'pro_model': '(.*?)', 'pro_category': '(.*?)', 'pro_name': '(.*?)', 'pro_current_price': '(.*?)', 'pro_raw_price': '(.*?)', 'pro_discount': '(.*?)', 'pro_likes_count': '(.*?)'"
        for line in lines:
            match = re.search(pattern, line)
            if match:
                likes_count = int(match.group(8))
                discount = float(match.group(7))
                likes_counts.append(likes_count)
                discounts.append(discount)

        # Generate the scatter chart
        plt.scatter(discounts, likes_counts, alpha=0.5)
        plt.xlabel('Discount')
        plt.ylabel('Likes Count')
        plt.title('Relationship between Likes Count and Discount (All Categories)')
        plt.tight_layout()

        # Save the figure
        figure_path = "data/figure/generate_discount_likes_count_figure.png"
        plt.savefig(figure_path)
        plt.close()


    def delete_all_products(self):
        '''
        Deletes all product data from products.txt
        :param: None
        :return: None
        '''
        with open("data/products.txt", 'w', encoding='utf-8') as product_file:
            product_file.truncate()


    def check_productid_exist(self, product_id):
        '''
        Checks product ID exists in products.txt
        :param: product_id
        :return: True if product exists, False otherwise
        '''
        self.product_id = product_id
        with open("data/products.txt", "r", encoding='utf-8') as product_file:
            for line in product_file:
                if "'pro_id': '" + str(product_id) + "'" in line:
                    return True
            return False




