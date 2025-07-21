#!/usr/bin/env python3

import pyodbc
import sys
import os
import traceback

def debug_odbc_environment():
    """Debug ODBC environment and drivers"""
    print("=== DEBUGGING ODBC ENVIRONMENT ===")
    
    # Python environment
    print(f"Python executable: {sys.executable}")
    print(f"Working directory: {os.getcwd()}")
    print(f"PYTHONPATH: {os.environ.get('PYTHONPATH', '<not set>')}")
    
    # Available drivers
    print(f"\n=== AVAILABLE DRIVERS ===")
    try:
        drivers = pyodbc.drivers()
        print(f"Found {len(drivers)} drivers:")
        for i, driver in enumerate(drivers):
            print(f"  {i+1}. {driver}")
    except Exception as e:
        print(f"Error getting drivers: {e}")
    
    # Test connections with different drivers
    server = "137.131.246.149"
    database = "dtbTransporte"
    uid = "consulta.pbi"
    pwd = "Br$Samor@2025#C"
    
    drivers_to_test = [
        "SQL Server",
        "ODBC Driver 17 for SQL Server",
        "ODBC Driver 18 for SQL Server",
        "ODBC Driver 13 for SQL Server"
    ]
    
    print(f"\n=== TESTING DIFFERENT DRIVERS ===")
    
    for driver in drivers_to_test:
        conn_str = f"DRIVER={{{driver}}};SERVER={server};DATABASE={database};UID={uid};PWD={pwd};TrustServerCertificate=yes;"
        print(f"\nTesting driver: {driver}")
        print(f"Connection string: {conn_str}")
        
        try:
            conn = pyodbc.connect(conn_str)
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            conn.close()
            print(f"  SUCCESS: {result[0]}")
        except Exception as e:
            print(f"  ERROR: {str(e)}")

if __name__ == "__main__":
    debug_odbc_environment()