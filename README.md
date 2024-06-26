# FIT9136: Assignment 3 - E-commerce Information Management System

This repository contains the work and materials for Assignment 3 of the FIT9136 unit (Algorithms and programming foundations in Python).

## Project Description
This project aims to develop skills in designing, constructing, testing, and documenting a Python program according to specific programming standards. The application developed here is a simple e-commerce information management system.

## Application Features
The e-commerce system includes functionalities for both customers and admin users. The system operates through a command-line interface, providing a user-friendly and well-formatted interface with appropriate messages to guide users.

### Customer Functionalities
- **Login:** Customers can log in to the system.
- **Shopping:** Customers can purchase products.
- **Order History:** Customers can view their order history.
- **Consumption Reports:** Customers can view their consumption reports.

### Admin Functionalities
- **Manage Users:** Admins can create, delete, and view customers.
- **Manage Products:** Admins can delete and view products.
- **Manage Orders:** Admins can delete and view orders.
- **Statistical Reports:** Admins can view statistical figures about information in the system.

## System Design
There are four main parts:

1. **IOInterface Class:** Handles all input/output operations.
2. **Main Control Class:** Manages the main business logic.
3. **Operation Classes:** Handle data reading/writing and simulate database activities.
4. **Model Classes:** Represent the data templates for users, products, and orders.

### Class Structure:
- **User Class:** Base class for Customer and Admin classes.
- **Customer Class:** Inherits from the User class.
- **Admin Class:** Inherits from the User class.
- **Product Class:** Model class for products.
- **Order Class:** Model class for orders.
- **UserOperation Class:** Contains operations related to users.
- **CustomerOperation Class:** Contains operations related to customers.
- **AdminOperation Class:** Contains operations related to admins.
- **ProductOperation Class:** Contains operations related to products.
- **OrderOperation Class:** Contains operations related to orders.
- **Interface Class:** Handles all I/O operations.

### Main File
The main file constructs the main control logic for the application, including the menu items and user interaction flow.

To execute the application, run `main.py`. 


