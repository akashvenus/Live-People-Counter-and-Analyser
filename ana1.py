import mysql.connector
import pandas as pd

db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "root",
    database = "mydatabase"
)

df = pd.read_sql("SELECT * FROM details",db)
# df["Day"] = pd.to_datetime(df["Day"])
# df['InTime'] = pd.to_datetime(df['InTime'],format= '%H:%M:%S' ).dt.time

df['datetime'] = pd.to_datetime(df['Day'] + ' ' + df['InTime'])
# df1 = df[df['datetime'].between('2021-02-28 19:00:00', '2021-02-28 20:00:00')]
# print (df1)
print("Enter the starting date in yyyy-mm-dd format ")
date1 = input()
print("Enter the starting time in hh:mm:ss format ")
time1 = input()

print("Enter the ending date in yyyy-mm-dd format ")
date2 = input()
print("Enter the ending time in hh:mm:ss format ")
time2 = input()

filter = df.loc[df['datetime'].between(f'{date1} {time1}', f'{date2} {time2}'), 'count']
print (filter)
# s = df.loc[df['datetime'].between('2021-02-28 19:00:00', '2021-02-28 20:00:00'), 'count']
# print (s)
