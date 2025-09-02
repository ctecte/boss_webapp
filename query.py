import sqlite3
from matplotlib import pyplot as plt
import pandas as pd

db = "boss_data.db"
conn = sqlite3.connect(db)
cursor = conn.cursor()

# uncomment the code below to view table columns 
table_info = "PRAGMA table_info(boss)"
cursor.execute(table_info)
i = 0
for column in cursor.fetchall():
    print(f"{i}: " + column[1])
    i += 1
cursor.execute("SELECT DISTINCT bidding_window FROM boss")
bidding_windows = cursor.fetchall()
for bid in bidding_windows:
    print(bid)

def get_bid_results(course_code, window):
    db = "boss_data.db"
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    # uncomment the code below to view table columns 
    table_info = "PRAGMA table_info(boss)"
    cursor.execute(table_info)
    i = 0
    for column in cursor.fetchall():
       print(f"{i}: " + column[1])
       i += 1
    
    query = """
        SELECT * from boss 
        where course_code = f"{course_code}"
        and bidding_window like f"{window}"
        and median_bid > 0;
        """
    df = pd.read_sql_query(query, conn)
    conn.close()

    day_order = ['MON', 'TUE', 'WED', 'THU', 'FRI']
    df['day_idx'] = df['day'].apply(lambda d: day_order.index(d))
    df = df.sort_values(by=['day_idx', 'start_time'])
    # temp_df = df[['course_code','day','start_time']]
    # print(temp_df.head(20))
    df['start_time'] = df['start_time'].str.slice(0, 5)
    df['end_time'] = df['end_time'].str.slice(0, 5)

    return df
