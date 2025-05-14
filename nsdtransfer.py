import pyodbc
import pandas as pd

# This script transfer the beta values table to Azure Data Studio SQL Server database for data preprocessing.
# Database connection details
server = "127.0.0.1"  # e.g., 'localhost' or 'yourserver.database.windows.net'
database = "nsd"
username = "sa"
password = "Laoniubusi123,"
driver = '{ODBC Driver 17 for SQL Server}'

# Connect to SQL Server
conn = pyodbc.connect(
    f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}"
)
cursor = conn.cursor()

# Load the CSV file into a pandas DataFrame
csv_path = "beta_matrix_new_roi02.csv"
df = pd.read_csv(csv_path)

# Generate the CREATE TABLE SQL statement dynamically
table_name = "BetaMatrix_HCP_MMP1_02"
num_conditions = len(df.columns) - 2  # Number of condition columns

columns_sql = ",\n    ".join([f"Condition_{i} FLOAT" for i in range(1, num_conditions + 1)])

create_table_sql = f"""
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '{table_name}')
BEGIN
    CREATE TABLE {table_name} (
        ROI VARCHAR(50),
        Node_Index INT,
        {columns_sql}
    );
END;
"""

print(create_table_sql)

# Execute the SQL query
cursor.execute(create_table_sql)
conn.commit()

print(f"Table '{table_name}' created successfully!")

insert_sql = f"INSERT INTO {table_name} (ROI, Node_Index, " + ", ".join([f"Condition_{i}" for i in range(1, num_conditions + 1)]) + ") VALUES (?, ?, " + ", ".join(["?" for _ in range(1, num_conditions + 1)]) + ")"
for index, row in df.iterrows():
    cursor.execute(insert_sql, tuple(row))

# Commit the changes to the database
conn.commit()

print(f"Table '{table_name}' created and data inserted successfully!")

# Close connection
cursor.close()
conn.close()
