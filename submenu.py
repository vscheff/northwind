from mysql.connector import connection, errors
# Local dependencies
from utils import *

def main(conn: connection.MySQLConnection):
    clear_screen()

    while True:
        print(
               " _________________________ \n"
               "|                         |\n"
               "| 1. Remove a Customer    |\n"
               "| 2. Add an Employee      |\n"
               "| 3. Main Menu            |\n"
               "|_________________________|\n"
        )      
        
        usr_inp = input("Please input an option: ").strip()

        if usr_inp == '1':
            delete_customer(conn)
        elif usr_inp == '2':
            add_employee(conn)
        elif usr_inp =='3':
            return
        else:
            print("ERROR: Bad Input! Please enter an integer in range [0-7]")


# Walks user through deleting a customer from the DB
# param conn - Active connection to the Northwind DB
def delete_customer(conn: connection.MySQLConnection):
    cursor = conn.cursor()

    clear_screen()

    # Get user input for the Customer # to be deleted, ensuring it exists within Customers
    usr_inp = get_user_input("Input the Customer # to be deleted: ")
    try:
        cursor.execute(f"SELECT * FROM Customers WHERE ID = {usr_inp}")
    except errors.ProgrammingError:
        print("ERROR: Invalid Input!")
        cursor.close()
        return
    result = cursor.fetchall()
    if not result:
        print(f"ERROR: No Customer with ID #{usr_inp} found!")
        cursor.close()
        return
    
    # Ensure this customer does not have Order entries
    cursor.execute(f"SELECT * FROM Orders WHERE CustomerID = {usr_inp}")
    if cursor.fetchall():
        print(f"ERROR: Customer #{usr_inp} has Orders in the DB! Unable to remove customer.")
        cursor.close()
        return

    cursor.execute(f"DELETE FROM Customers WHERE ID = {usr_inp}")

    conn.commit()
    cursor.close()

    print(f"Customer #{usr_inp} successfully removed from the database!")


# Walks user through adding an Employee to the DB
# param conn - Active connection to the Northwind DB
def add_employee(conn: connection.MySQLConnection):
    cursor = conn.cursor()

    clear_screen()
    print("Please input the following information to add an Employee to the database (* = required): \n")

    values = []
    
    # Calculate new Employee ID
    cursor.execute("SELECT MAX(ID) FROM Employees")
    values.append(cursor.fetchall()[0][0] + 1)

    # Default company name
    values.append("Northwind Traders")

    values.append(get_user_input("* Input Last Name: "))
    values.append(get_user_input("* Input First Name: "))
    values.append(get_user_input("* Input Email: "))
    values.append(get_user_input("* Input Job Title: "))
    values.append(get_user_input("* Input Business Phone: "))
    values.append(get_user_input("* Input Home Phone: "))
    values.append(get_user_input("  Input Mobile Phone: ", True))

    # Default company Fax
    values.append("(123)555-0103")
    
    values.append(get_user_input("* Input Address: "))
    values.append(get_user_input("* Input City: "))
    values.append(get_user_input("* Input State: "))
    values.append(get_user_input("* Input ZIP: "))
    values.append(get_user_input("* Input Country: "))

    # Default company website
    values.append("http://northwindtraders.com")
    
    values.append(get_user_input("  Input Notes: ", True))

    query = "INSERT INTO Employees ( " \
            "   ID, Company, LastName, FirstName, Email, JobTitle, BusinessPhone, HomePhone, " \
            "   MobilePhone, Fax, Address, City, State, ZIP, Country, Web, Notes " \
            ") " \
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(query, values)
    
    privileges_added = []

    # Allow user to enter Employee Privileges
    while True:
        usr_inp = input("\nAdd Privileges for this Employee? (y/n): ").strip().lower()
        if not usr_inp:
            print("ERROR: Empty Input!")
            continue
        if usr_inp[0] == 'n':
            break
        if usr_inp[0] != 'y':
            print("ERROR: Invalid Input! Please enter only 'y' or 'n'.")
            continue

        usr_inp = get_user_input("Input Privilege ID: ")
        try:
            cursor.execute(f"SELECT * FROM Privileges WHERE PrivilegeID = {usr_inp}")
        except errors.ProgrammingError:
            print("ERROR: Invalid Input!")
            continue
        if not cursor.fetchall():
            print(f"ERROR: No Priviledge with ID {usr_inp} found!")
            continue
        if usr_inp in privileges_added:
            print(f"ERROR: Privilege #{usr_inp} already added!")
            continue

        query = "INSERT INTO Employee_Privileges (EmployeeID, PrivilegeID) VALUES (%s, %s)"
        cursor.execute(query, [values[0], usr_inp])
        
        privileges_added.append(usr_inp)

        print("Priviledge successfully added!")

    
    conn.commit()
    cursor.close()

    print(f"Employee #{values[0]} successfully added to the DB!")


if __name__ == "__main__":
    main()
