from mysql.connector import connection, cursor as MySQLCursor, errors
from datetime import datetime
# Local dependencies
from utils import *
from submenu import main as more_options


def main():
    conn_params = {"user": "cs4430", "password": "cs4430", "host": "localhost", "database": "northwind"}

    try:
        conn = connection.MySQLConnection(**conn_params)
    except errors.ProgrammingError:
        print("ERROR: Unable to connect to database! Halting Execution.")
        return

    clear_screen()

    # Generated at: https://www.coolgenerator.com/ascii-text-generator
    print(
          "\n"  
          "███╗   ██╗ ██████╗ ██████╗ ████████╗██╗  ██╗██╗    ██╗██╗███╗   ██╗██████╗ \n"
          "████╗  ██║██╔═══██╗██╔══██╗╚══██╔══╝██║  ██║██║    ██║██║████╗  ██║██╔══██╗\n"
          "██╔██╗ ██║██║   ██║██████╔╝   ██║   ███████║██║ █╗ ██║██║██╔██╗ ██║██║  ██║\n"
          "██║╚██╗██║██║   ██║██╔══██╗   ██║   ██╔══██║██║███╗██║██║██║╚██╗██║██║  ██║\n"
          "██║ ╚████║╚██████╔╝██║  ██║   ██║   ██║  ██║╚███╔███╔╝██║██║ ╚████║██████╔╝\n"
          "╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝ ╚══╝╚══╝ ╚═╝╚═╝  ╚═══╝╚═════╝ \n"
    )
    print("Welcome to the Northwind Frontend UI!")
    
    # Main execution loop, iterates until user inputs '7'
    while True:
        print(
              "\n"
              " _________________________ \n"
              "|                         |\n"
              "| 1. Add a Customer       |\n"
              "| 2. Add an Order         |\n"
              "| 3. Remove an Order      |\n"
              "| 4. Ship an Order        |\n"
              "| 5. Print Pending Orders |\n"
              "| 6. More Options         |\n"
              "| 7. Exit                 |\n"
              "|_________________________|\n"
        )

        usr_inp = input("Please input an option: ").strip()

        if usr_inp == '1':
            add_customer(conn)
        elif usr_inp == '2':
            add_order(conn)
        elif usr_inp == '3':
            delete_order(conn)
        elif usr_inp == '4':
            ship_order(conn) 
        elif usr_inp == '5':
            print_pending(conn)
        elif usr_inp == '6':
            more_options(conn)
        elif usr_inp == '7':
            break
        else:
            print("ERROR: Bad Input! Please enter an integer in range [0-7].")

    conn.close()
    
    print("\nGoodbye!")


# Walks a user through adding a customer to the DB
# param conn - Active connection to the Northwind DB
def add_customer(conn: connection.MySQLConnection):
    cursor = conn.cursor()
    
    clear_screen()
    print("Please input the following information to add a customer to the database:\n")
    
    values = []
    
    # Calculate new Customer ID
    cursor.execute("SELECT MAX(ID) FROM Customers")
    values.append(cursor.fetchall()[0][0] + 1)
    
    # Get user input for each other field
    values.append(get_user_input("Input Company: "))
    values.append(get_user_input("Input Last Name: "))
    values.append(get_user_input("Input First Name: "))
    values.append(get_user_input("Input E-Mail: ", True))
    values.append(get_user_input("Input Job Title: "))
    values.append(get_user_input("Input Business Phone: "))
    values.append(get_user_input("Input Home Phone: ", True))
    values.append(get_user_input("Input Mobile Phone: ", True))
    values.append(get_user_input("Input Fax: "))
    values.append(get_user_input("Input Address: "))
    values.append(get_user_input("Input City: "))
    values.append(get_user_input("Input State: "))
    values.append(get_user_input("Input ZIP: "))
    values.append(get_user_input("Input Country: "))
    values.append(get_user_input("Input Website: ", True))
    values.append(get_user_input("Input Customer Notes: ", True))
    
    query = "INSERT INTO Customers ( " \
            "    ID, Company, LastName, FirstName, Email, JobTitle, BusinessPhone, HomePhone, " \
            "    MobilePhone, Fax, Address, City, State, ZIP, Country, Web, Notes " \
            ") " \
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(query, values)
    
    conn.commit()
    cursor.close()

    print(f"\nCustomer #{values[0]} successfully added to the database!")


# Walks a user through adding an order to the DB
# param conn - Active connection to the Northwind DB 
def add_order(conn: connection.MySQLConnection):
    cursor = conn.cursor()
    
    clear_screen()
    
    print("Please input the following information to add an order to the database: \n")

    values = []

    # Calculate new Order ID
    cursor.execute("SELECT MAX(OrderID) FROM Orders")
    values.append(cursor.fetchall()[0][0] + 1)
    
    # Get user input for Employee ID, ensuring it is found in Employees
    result = None
    usr_inp = None
    while not result:
        if usr_inp:
            print("ERROR: Invalid Employee ID!")
        usr_inp = get_user_input("Input Employee ID: ")
        try:
            cursor.execute(f"SELECT * FROM Employees WHERE ID = {usr_inp}")
        except errors.ProgrammingError:
            continue
        result = cursor.fetchall()
    values.append(usr_inp)
    
    # Get user input for Customer ID, ensuring it is found in Customers
    result = None
    usr_inp = None
    while not result:
        if usr_inp:
            print("ERROR: Invalid Customer ID!")
        usr_inp = get_user_input("Input Customer ID: ")
        try:
            cursor.execute(f"SELECT * FROM Customers WHERE ID = {usr_inp}")
        except errors.ProgrammingError:
            continue
        result = cursor.fetchall()
    values.append(usr_inp)

    # Use today's date for Order Date
    values.append(datetime.today().isoformat(sep = ' ', timespec = "seconds"))

    # Pull shipping information from Customer table using Customer ID
    cursor.execute(f"SELECT FirstName, LastName, Address, City, State, ZIP, Country "
                   f"FROM Customers "
                   f"WHERE ID = {values[2]}")
    result = cursor.fetchall()[0]
    
    # Combine Firs tName & Last Name into one string for Ship To Name
    values.append(' '.join(result[:2]))
    
    # Add Address, City, State, Zip, & Country from query result
    values.extend(result[2:])

    # Shipping fee of 0 for a new order
    values.append(0)
    
    # Get user input for Taxes, defaulting to 0 with no input
    usr_inp = get_user_input("Input Taxes: ", True)
    if not usr_inp:
        usr_inp = '0'
    values.append(usr_inp)

    # Get user input for Payment Type, ensuring it's a valid type
    usr_inp = ""
    while usr_inp.lower() not in ("check", "credit card", "cash"):
        if usr_inp:
            print("ERROR: Invalid Payment Type. Please input 'Check', 'Credit Card', or 'Cash'")
        usr_inp = get_user_input("Input Payment Type: ", True)
        if not usr_inp:
            break
        usr_inp = usr_inp.title()
    values.append(usr_inp)

    # Get user input for Payment Date only if a Payment Type was entered, ensuring the date entered is valid
    if usr_inp:
        while True:
            usr_inp = get_user_input("Input Payment Date: ")
            try:
                pay_date = datetime.fromisoformat(usr_inp)
            except ValueError:
                print("ERROR: Bad Date! Please input date in the format YYYY-MM-DD")
                continue
            values.append(pay_date.isoformat(sep = ' ', timespec = "seconds"))
            break
    else:
        values.append(None)
    
    # Get user input for Notes
    values.append(get_user_input("Input Order Notes: ", True))

    # Get user input for Tax Rate, defaulting to 0 with no input
    usr_inp = get_user_input("Input Tax Rate: ", True)
    if not usr_inp:
        usr_inp = '0'
    values.append(usr_inp)

    # Get user input for Tax Status, ensuring it's a valid Tax Status ID
    result = None
    usr_inp = None
    while not result:
        if usr_inp:
            print("ERROR: Invalid Tax Status!")
        usr_inp = get_user_input("Input Tax Status ID: ", True)
        if not usr_inp:
            break
        try:
            cursor.execute(f"SELECT * FROM Orders_Tax_Status WHERE ID = {usr_inp}")
        except errors.ProgrammingError:
            continue
        result = cursor.fetchall()
    values.append(usr_inp)
    
    # Order status of 0 representing a new order
    values.append(0)

    query = "INSERT INTO Orders ( " \
            "    OrderID, EmployeeID, CustomerID, OrderDate, ShipName, ShipAddress, " \
            "    ShipCity, ShipState, ShipZIP, ShipCountry, ShippingFee, Taxes, PaymentType, " \
            "    PaidDate, Notes, TaxRate, TaxStatus, StatusID " \
            ") " \
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(query, values)

    # Add Order Items until user wishes to stop
    while True:
        add_order_item(cursor, values[0])
        if input("\nAdd another order item? (y, n): ").lower()[0] == 'n':
            break

    conn.commit()
    cursor.close()

    print(f"\nOrder #{values[0]} successfully added to the database!")


# Walks user through adding an Order Item to the DB
# param  cursor - Active cursor for the Northwind DB
# param orderID - Foreign key used to tie the Order Items to an Order
def add_order_item(cursor: MySQLCursor, orderID: str):
    print("\nPlease input the following information to add an order item to the database: \n")

    values = []

    # Calculate new Order Item ID
    cursor.execute("SELECT MAX(ID) FROM Order_Details")
    values.append(cursor.fetchall()[0][0] + 1)
    
    # Use argument Order ID
    values.append(orderID)
    
    # Get user input for Product ID, ensuring it exists in Products and is not discontinued
    usr_inp = None
    while True:
        if usr_inp:
            print("ERROR: Invalid Product ID!")
        usr_inp = get_user_input("Input Product ID: ")
        try:
            cursor.execute(f"SELECT ListPrice, Discontinued FROM Products WHERE ID = {usr_inp}")
        except errors.ProgrammingError:
            continue
        result = cursor.fetchall()
        if not result:
            continue
        result = result[0]
        if result[1] == 0:
            break
        print("ERROR: Item discontinued!")
        usr_inp = None
    values.append(usr_inp)

    # Get user input for Quantity, ensuring it's a valid positive number
    while True:
        usr_inp = get_user_input("Input Quantity: ")
        try:
            usr_inp = float(usr_inp)
        except ValueError:
            print("ERROR: Invalid Input! Please enter only decimal numbers.")
            continue
        if usr_inp > 0:
            break
        print("ERROR: Bad Range! Please enter only positive values.")
    values.append(usr_inp)

    # Use List Price from Products query as Unit Price
    values.append(result[0])

    # Get user input for Discount, ensuring it's a valid non-negative number. Defaults to zero on no input
    while True:
        usr_inp = get_user_input("Input Discount: ", True)
        if not usr_inp:
            usr_inp = 0.0
            break
        try:
            usr_inp = float(usr_inp)
        except ValueError:
            print("ERROR: Invalid Input! Please enter only decimal numbers.")
            continue
        if usr_inp >= 0:
            break
        print("ERROR: Bad Range! Please enter only positive values.")
    values.append(usr_inp)

    # Use zero for Status ID indicating "None" status
    values.append(0)

    query = "INSERT INTO Order_Details (ID, OrderID, ProductID, Quantity, UnitPrice, Discount, StatusID) " \
            "VALUES (%s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(query, values)

    print(f"\nOrder item #{values[0]} successfully added to the database!")
    

# Deletes an order from the DB
# param conn - Active connection to the Northwind DB
def delete_order(conn: MySQLCursor):
    cursor = conn.cursor()

    clear_screen()

    # Get user input for the Order # to be deleted, ensuring it exists within Orders
    usr_inp = get_user_input("Input the Order # to be deleted: ")
    try:
        cursor.execute(f"SELECT * FROM Orders WHERE OrderID = {usr_inp}")
    except errors.ProgrammingError:
        print("ERROR: Invalid Input!")
        cursor.close()
        return
    if not cursor.fetchall():
        print(f"ERROR: No order with ID #{usr_inp} found!")
        cursor.close()
        return

    cursor.execute(f"DELETE FROM Order_Details WHERE OrderID = {usr_inp}")
    cursor.execute(f"DELETE FROM Orders WHERE OrderID = {usr_inp}")

    conn.commit()
    cursor.close()

    print(f"Order with ID {usr_inp} successfully removed from the database!")


# Walks the user through shipping an order
# param conn - Active connection to the Northwind DB
def ship_order(conn: MySQLCursor):
    cursor = conn.cursor()

    clear_screen()

    # Get user input for the Order ID to be shipped, unsuring it exists within Orders
    order_ID = get_user_input("Input the Order ID to be shipped: ")
    try:
        cursor.execute(f"SELECT * FROM Orders WHERE OrderID = {order_ID}")
    except errors.ProgrammingError:
        print("ERROR: Invalid Input!")
        cursor.close()
        return
    if not cursor.fetchall():
        print(f"ERROR: No Order with ID {order_ID} found!")
        cursor.close()
        return
   

    date_today = datetime.today().isoformat(sep = ' ', timespec = "seconds")
   
    cursor.execute(f"SELECT ProductID, Quantity FROM Order_Details WHERE OrderID = {order_ID}")

    # Loop once for each Product in the order 
    for prod_ID, quantity in cursor.fetchall():
        query = "SELECT TransactionType, Quantity FROM Inventory_Transactions WHERE ProductID = %s"
        cursor.execute(query, [prod_ID])
        total_quantity = 0
        
        # Iterate through each transaction, calculating the available stock
        for tx_type, tx_quantity in cursor.fetchall():
            if tx_type == 1:
                total_quantity += tx_quantity
            else:
                total_quantity -= tx_quantity
        
        # Halt execution of this function if there's not enough stock for a Product on the order
        if total_quantity < quantity:
            print(f"ERROR: Not enough stock for Product #{prod_ID}! Unable to ship Order #{order_ID}")
            conn.rollback()
            cursor.close()
            return
        
        values = []

        # Calculate new Transaction ID
        cursor.execute("SELECT MAX(TransactionID) FROM Inventory_Transactions")
        values.append(cursor.fetchall()[0][0] + 1)

        # TransactionType of 2 for "Sold"
        values.append(2)

        # Use today's date for Date Created and Date Modified
        values.append(date_today)
        values.append(date_today)

        values.append(prod_ID)

        values.append(quantity)

        # Get user input for Comments
        values.append(get_user_input("Input Transaction Comments: "))

        tx_query = "INSERT INTO Inventory_Transactions ( " \
                   "    TransactionID, TransactionType, TransactionCreatedDate, " \
                   "    TransactionModifiedDate, ProductID, Quantity, Comments " \
                   ") " \
                   "VALUES (%s, %s, %s, %s, %s, %s, %s)"
    
        cursor.execute(tx_query, values)

        cursor.execute(f"UPDATE Order_Details SET StatusID = 1 WHERE OrderID = {order_ID}")

    values = []

    # Use today's date for ShippedDate
    values.append(date_today)

    # Get user input for Shipper ID, ensuring it exists in the Shippers table 
    result = None
    usr_inp = None
    while not result:
        if usr_inp:
            print("ERROR: Invalid Shipper Id!")
        usr_inp = get_user_input("Input Shipper ID: ", True)
        if not usr_inp:
            break
        try:
            cursor.execute(f"SELECT * FROM Shippers WHERE ID = {usr_inp}")
        except errors.ProgrammingError:
            continue
        result = cursor.fetchall()
    values.append(usr_inp)
    
    # Get user input for shipping fee, ensuring it's a valid non-negative number
    while True:
        usr_inp = get_user_input("Input Shipping Fee: ")
        try:
            usr_inp = float(usr_inp)
        except ValueError:
            print("ERROR: Invalid Input! Please enter only valid decimal numbers.")
            continue
        if usr_inp >= 0:
            break
        print("ERROR: Invalid Input! Please enter only non-negative numbers.")
    values.append(usr_inp)

    # StatusID of 2 for "shipped"
    values.append(2)

    cursor.execute(f"UPDATE Orders " 
                   f"SET ShippedDate=%s, ShipperID=%s, ShippingFee=%s, StatusID=%s "
                   f"WHERE OrderID = {order_ID}", values)

    conn.commit()
    cursor.close()

    print(f"Order #{order_ID} successfully shipped!")


# Prints all orders with a NULL shipping date to the terminal
# param conn - Active connection to the Northwind DB 
def print_pending(conn: MySQLCursor):
    cursor = conn.cursor()

    clear_screen()
    
    cursor.execute("SELECT OrderID, EmployeeID, CustomerID, OrderDate, "
                   "       ShipName, ShipAddress, ShipCity, ShipState, ShipZIP, ShipCountry "
                   "FROM Orders "
                   "WHERE ShippedDate IS NULL")
    result = cursor.fetchall()

    result.sort(key=lambda x: x[3])
    print("\n Order Employee Customer  Order Date        Name        Ship To Address      City      State   ZIP   Country \n"
          " ----- -------- -------- ------------ ---------------- ----------------- ------------- ----- ------- -------")

    # Print each tuple nicely formatted
    for a, b, c, d, e, f, g, h, i, j in result:
        print(f"  {a:<8} {b:<7} {c:<6} {d.strftime('%Y-%m-%d'):<13} {e:<15} {f:<17} {g:<14} {h:<4} {i:<8} {j}")


if __name__ == "__main__":
    main()
