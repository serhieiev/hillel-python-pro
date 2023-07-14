import os
import sqlite3

from typing import List, Set, Union
from decimal import Decimal


# Function to execute a SQL query and return the result
def execute_query(query_sql: str, fetch_all: bool = False) -> Union[List, tuple, None]:
    db_pass = os.path.join(os.getcwd(), 'chinook.db')
    connection = sqlite3.connect(db_pass)
    cur = connection.cursor()
    if fetch_all:
        result = cur.execute(query_sql).fetchall()
    else:
        result = cur.execute(query_sql).fetchone()
    connection.close()
    return result

# Function to calculate the total profit of the invoice_items table
def calculate_profit():
    # Define the SQL query
    query_sql = f'''
    SELECT SUM(UnitPrice * Quantity) AS TotalProfit
    FROM invoice_items
    '''

    result = execute_query(query_sql)
    return Decimal(result[0]).quantize(Decimal('0.00')) if result else None

# Function to find repeated first names and their number in the customers table
def find_repeated_firstnames():
    # Define the SQL query
    query_sql = f'''
    SELECT FirstName, COUNT(*) as Count
    FROM customers
    GROUP BY FirstName
    HAVING COUNT(*) > 1
    '''

    result =  execute_query(query_sql, fetch_all = True)
    return result

print(calculate_profit())

results = find_repeated_firstnames()
for result in results:
    print(f"'{result[0]}', {result[1]}")