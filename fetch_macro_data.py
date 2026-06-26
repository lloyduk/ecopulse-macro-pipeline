import requests
import sqlite3 # Import the SQL database library

# 1. Configuration
API_KEY = "0DZTAI5E9ZNXHT1R" 
FUNCTION = "FEDERAL_FUNDS_RATE"
URL = f"https://www.alphavantage.co/query?function={FUNCTION}&apikey={API_KEY}"

print("Step 1: Connecting to Alpha Vantage pipeline...")

try:
    response = requests.get(URL)
    data = response.json()
    
    if "data" in data:
        recent_data = data["data"][:5]
        print("Step 1 Success: Data fetched over the network.")
        
        print("\nStep 2: Initializing SQLite Database...")
        # Open a connection to the database file (creates it if it doesn't exist)
        conn = sqlite3.connect("ecopulse.db")
        cursor = conn.cursor()
        
        # Create a structured SQL table to store the economic records
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS interest_rates (
                announcement_date TEXT PRIMARY KEY,
                rate_value REAL
            )
        ''')
        
        print("Step 3: Ingesting records into SQL database layout...")
        inserted_counter = 0
        
        for record in recent_data:
            date = record["date"]
            value = float(record["value"]) # Convert text format to a float number
            
            # INSERT OR IGNORE avoids duplicates if I run the script multiple times
            cursor.execute('''
                INSERT OR IGNORE INTO interest_rates (announcement_date, rate_value)
                VALUES (?, ?)
            ''', (date, value))
            
            # Check if a row was actually inserted
            if cursor.rowcount > 0:
                inserted_counter += 1
                
        # Commit (save) changes permanently to the database file
        conn.commit()
        conn.close()
        
        print(f"SUCCESS! Added {inserted_counter} brand new economic records to 'ecopulse.db'.")
        
    else:
        print("\n API Error. Response received:", data)

except Exception as e:
    print(f"\n Pipeline failed. Error: {e}")