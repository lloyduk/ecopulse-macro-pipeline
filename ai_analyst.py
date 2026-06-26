import sqlite3

def run_ai_analysis():
    print(" Initializing EcoPulse AI Analyst Engine...")
    
    # 1. Connect to the existing SQL database
    conn = sqlite3.connect("ecopulse.db")
    cursor = conn.cursor()
    
    # 2. Fetch the 2 most recent interest rate entries to calculate the change (delta)
    cursor.execute("SELECT announcement_date, rate_value FROM interest_rates ORDER BY announcement_date DESC LIMIT 2")
    records = cursor.fetchall()
    conn.close()
    
    if len(records) < 2:
        print(" Insufficient historical data in database to calculate economic trends yet.")
        return

    # Extract the dates and values from the database rows
    current_date, current_rate = records[0]
    previous_date, previous_rate = records[1]
    
    # 3. Core Math: Calculate the economic shift direction
    rate_change = round(current_rate - previous_rate, 4)
    
    print("\n Statistical Readout:")
    print(f"   • Current Rate ({current_date}): {current_rate}%")
    print(f"   • Previous Rate ({previous_date}): {previous_rate}%")
    print(f"   • Shift Delta: {rate_change:+}%")
    
    print("\n AI Risk Assessment Report:")
    print("-" * 65)
    
    # 4. Rule-based AI Categorization Layer
    if rate_change > 0:
        sentiment = "HAWKISH (Contractionary)"
        risk_level = "HIGH RISK FOR ACCELERATED TECH STOCKS"
        insight = f"The Federal Reserve increased interest rates by {abs(rate_change)}%. This structural monetary tightening increases the cost of corporate capital, placing downward pressure on high-growth technology equity valuations."
    elif rate_change < 0:
        sentiment = "DOVISH (Expansionary)"
        risk_level = "LOW RISK / GROWTH ORIENTED"
        insight = f"The Federal Reserve decreased interest rates by {abs(rate_change)}%. This capital easing lowers borrowing friction, structurally accelerating corporate net margins and boosting liquidity inside tech-sector equity markets."
    else:
        sentiment = "NEUTRAL / STABLE"
        risk_level = "MODERATE / PREDICTABLE"
        insight = "Interest rates remain unchanged. Market volatility is expected to normalize as macro conditions match current baseline institutional pricing schemas."

    # Print out the structured AI profile output
    print(f"ECONOMIC SENTIMENT : {sentiment}")
    print(f"MACRO RISK PROFILE : {risk_level}")
    print(f"DECISION INSIGHT   : {insight}")
    print("-" * 65)

if __name__ == "__main__":
    run_ai_analysis()