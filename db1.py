import mysql.connector

db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "root",
    database = "mydatabase"
)

mycursor = db.cursor()
try:
    mycursor.execute("CREATE TABLE details(count smallint, InTime CHAR(50), Day CHAR(50))")
    print("DB successfully created")

except:
    print("DB already created ")
