import mysql.connector
import pandas as pd
from datetime import datetime

db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "root",
    database = "mydatabase"
)

df = pd.read_sql("SELECT * FROM aisles",db)
df["Day"] = pd.to_datetime(df["Day"])
print("Enter start and end date to get total count in each aisle (yyyy-mm-dd)")
date1inp = input()
date2inp = input()
date1 = datetime.strptime(f'{date1inp}', '%Y-%m-%d').date()
date2 = datetime.strptime(f'{date2inp}', '%Y-%m-%d').date()
df.set_index('Day', inplace=True)
print((df.loc[date1:date2]).sum())
