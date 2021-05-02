import mysql.connector

db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "root",
    database = "mydatabase"
)

mycursor = db.cursor()
try:
    mycursor.execute("CREATE TABLE aisles(A1 int, A2 int,Day CHAR(25))")
    print("DB created successfully")

except:
    print("DB already created")
# mycursor.execute("SELECT * FROM aisles")
# myresult = mycursor.fetchall()
#
# for x in myresult:
#     print(x)
