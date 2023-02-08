███╗   ██╗ ██████╗ ██████╗ ████████╗██╗  ██╗██╗    ██╗██╗███╗   ██╗██████╗ 
████╗  ██║██╔═══██╗██╔══██╗╚══██╔══╝██║  ██║██║    ██║██║████╗  ██║██╔══██╗
██╔██╗ ██║██║   ██║██████╔╝   ██║   ███████║██║ █╗ ██║██║██╔██╗ ██║██║  ██║
██║╚██╗██║██║   ██║██╔══██╗   ██║   ██╔══██║██║███╗██║██║██║╚██╗██║██║  ██║
██║ ╚████║╚██████╔╝██║  ██║   ██║   ██║  ██║╚███╔███╔╝██║██║ ╚████║██████╔╝
╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝ ╚══╝╚══╝ ╚═╝╚═╝  ╚═══╝╚═════╝

Northwind Frontend UI Documentation

####################################
# Compilation Instructions         #
####################################
 * Requirements:
	- Python v3.8 or greater
	- pip v19.3.1 or greater
	- mysql v8.0.0 or greater

 * First-time setup:
      execute `pip install mysql-connector-python`

 * Running the program:
	- execute `python3 ./a3.py`

####################################
# Explanation of Main Functions    #
####################################
 * Add a Customer
	- Walks user through adding a new Customer to the DB
	- Required Fields:
		* Company
		* Last Name
		* First Name
		* Job Title
		* Business Phone
		* Fax
		* Address
		* City
		* State
		* ZIP
		* Country

 * Add an Order
	- Walks user through adding a new Order to the DB
	- Required Fields:
		* Employee ID (Must match record from Employees)
		* Customer ID (Must match record from Customer)
		* Payment Date (Only Required if Payment Type added, must be in YYYY-MM-DD format)
	- Required Fields for Adding Order Items:
		* Product ID (Must match record from Products)
		* Quantity (Must be a positive integer)

 * Remove an Order
	- Walks user through removing an Order from the DB
	- Required Fields:
		* Order ID (Must match record from Orders) 

 * Ship an Order
	- Walks user through shipping a pending Order from the DB
	- Will halt execution if there is not enough stock for an Order Item in the Order
	- Required Fields:
		* Order ID (Must match record from Orders)
		* Shipper ID (Must match record from Shippers)
		* Shipping Fee (Must be a non-negative integer)

 * Print Pending Orders
	- Prints all orders that have not been shipped to the terminal

 * More Options
	- Opens a submenu with additional actions

 * Exit
	- Halts execution of the program

####################################
# Explanation of Submenu Functions #
####################################
 * Remove a Customer
	- Walks user through deleting a customer from the DB
	- Required Fields:
		* Customer ID (Must match record from Customer)

* Add an Employee
	- Walks user through adding an Employee to the DB
	- Required Fields:
		* Last Name
		* First Name
		* Email
		* Job Title
		* Business Phone
		* Home Phone
		* Fax
		* Address
		* City
		* State
		* Zip
		* Country
