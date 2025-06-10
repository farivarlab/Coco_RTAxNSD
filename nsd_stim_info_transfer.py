import pyodbc
import pandas as pd

# This script transfer the nas_stim_info_merged table to Azure Data Studio SQL Server database for data preprocessing (dropping unnecessary columns, etc.).
server = 'localhost'  # e.g., 'localhost' or 'yourserver.database.windows.net'
database = ''
username = ''
password = ''
driver = '{ODBC Driver 17 for SQL Server}'

conn = pyodbc.connect(
    f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}"
)
cursor = conn.cursor()

csv_path = "nsd_stim_info_merged.csv"  # Update this with the correct path
df = pd.read_csv(csv_path)
df = df.drop(columns=["cocoSplit", "cocoId", "cropBox", "loss"], axis=1)
table_name = "nsd_stim_info"

num_conditions = len(df.columns)
pure_cols  = [col for col in df.columns]
print(pure_cols)
cols = ['node_index INT', 'nsdId INT', 'flagged BIT', 
'BOLD5000 BIT', 'shared1000 BIT', 'subject1 BIT', 'subject2 BIT', 'subject3 BIT', 'subject4 BIT', 'subject5 BIT', 
'subject6 BIT', 'subject7 BIT', 'subject8 BIT', 'subject1_rep0 INT', 'subject1_rep1 INT', 'subject1_rep2 INT', 
'subject2_rep0 INT', 'subject2_rep1 INT', 'subject2_rep2 INT', 'subject3_rep0 INT', 'subject3_rep1 INT', 
'subject3_rep2 INT', 'subject4_rep0 INT', 'subject4_rep1 INT', 'subject4_rep2 INT', 'subject5_rep0 INT', 
'subject5_rep1 INT', 'subject5_rep2 INT', 'subject6_rep0 INT', 'subject6_rep1 INT', 'subject6_rep2 INT', 
'subject7_rep0 INT', 'subject7_rep1 INT', 'subject7_rep2 INT', 'subject8_rep0 INT', 'subject8_rep1 INT', 
'subject8_rep2 INT']

cols_sql = ",\n    ".join(cols)

create_table_sql = f"""
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '{table_name}')
BEGIN
    CREATE TABLE {table_name} (
        {cols_sql}
    );
END;
"""
print(create_table_sql)
# Execute the SQL query
cursor.execute(create_table_sql)
conn.commit()

print(f"Table '{table_name}' created successfully!")

insert_sql = f"INSERT INTO {table_name} (" + ", ".join(pure_cols) + ") VALUES (" + ", ".join(["?" for _ in range(1, num_conditions + 1)]) + ")"
for index, row in df.iterrows():
    cursor.execute(insert_sql, tuple(row))

# Commit the changes to the database
conn.commit()

print(f"Table '{table_name}' created and data inserted successfully!")

# Close connection
cursor.close()
conn.close()