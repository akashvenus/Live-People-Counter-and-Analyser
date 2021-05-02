import mysql.connector

db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "root",
    database = "mydatabase"
)

mycursor = db.cursor()

try:
    sql = "DROP TABLE aisles"
    mycursor.execute(sql)
    print("DB removed successfully")

except:
    print("DB already removed, does not exist")
