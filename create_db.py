import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="new_password",
)

my_cursor = (
    mydb.cursor()
)  # create a cursor object, it will allow us to interact with the database it sort of like a pointer

my_cursor.execute("CREATE DATABASE our_users")  # create a database called our_users

my_cursor.execute("SHOW DATABASES")  # show all the databases
for db in my_cursor:
    print(db)  # print all the databases


# if we run this file again it will give us an error because the database already exists.
# dont run this file.
