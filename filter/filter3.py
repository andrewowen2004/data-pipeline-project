import sqlite3
import pandas as pd

# Step 1: Connect to the SQLite database
conn = sqlite3.connect('../data/transactions.db')

# Step 2: Load SQL query from external file
with open('../sql/sort3.sql', 'r') as file:
    query = file.read()

# Step 3: Execute the query
df = pd.read_sql_query(query, conn)

# Step 4: Export results to a CSV file
df.to_csv('../output/query_results-3.csv', index=False)

# Step 5: Close the connection
conn.close()

print("Export complete: 'output/query_results-3.csv'")