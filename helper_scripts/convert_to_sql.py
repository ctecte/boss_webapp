import sqlite3 as sql
import pandas as pd

conn = sql.connect('boss_data.db')
cursor = conn.cursor()

file = '_merged_filtered.xlsx'
excel_files = [
    f'2021-22_T2{file}',
    f'2022-23_T1{file}',
    f'2022-23_T2{file}',
    f'2023-24_T1{file}',
    f'2023-24_T2{file}',
    f'2024-25_T1{file}',
    f'2024-25_T2{file}',
    f'2025-26_T1{file}'
]

for excel in excel_files:
    print(excel)
    # Adjust the path here as required! ----------------------------------------------------
    df = pd.read_excel(f'merged_data_filtered/{excel}')
    print("read excel")

    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
    
    print("converting to sql")
    df.to_sql("boss", conn, if_exists="append", index=False)
    print("done")

conn.commit()
conn.close()
print("Combined excels into boss_data.db")
