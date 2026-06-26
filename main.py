from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import sqlite3
import os

app = FastAPI()

@app.get("/api/analysis")
def get_analysis():
    # 1. Dynamically find the folder where main.py is running right now
    current_folder = os.path.dirname(os.path.abspath(__file__))
    
    # 2. Join it with your database name automatically
    db_path = "ecopulse.db"
    
    print(f"\n🔍 AI ENGINE CHECK: Looking for database at: {db_path}")
    print(f"📂 DOES FILE EXIST? {os.path.exists(db_path)}")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT announcement_date, rate_value FROM interest_rates ORDER BY announcement_date DESC LIMIT 2")
        records = cursor.fetchall()
        conn.close()
        
        if len(records) < 2:
            print("⚠️ DB Found, but not enough entries inside.")
            return {"status": "error", "message": "Insufficient records"}
            
        current_date, current_rate = records[0]
        previous_date, previous_rate = records[1]
        rate_change = round(current_rate - previous_rate, 4)
        
        if rate_change > 0:
            sentiment, risk = "HAWKISH (Contractionary)", "HIGH RISK FOR TECH STOCKS"
            insight = f"Rates increased by {abs(rate_change)}%. Capital cost is rising."
        elif rate_change < 0:
            sentiment, risk = "DOVISH (Expansionary)", "LOW RISK / GROWTH ORIENTED"
            insight = f"Rates decreased by {abs(rate_change)}%. Lower borrowing friction boosts tech sectors."
        else:
            sentiment, risk = "NEUTRAL / STABLE", "MODERATE / PREDICTABLE"
            insight = "Rates unchanged. Market volatility expected to normalize."
            
        print("✅ SUCCESS: Successfully fetched data from database layout!")
        return {
            "current_date": current_date,
            "current_rate": current_rate,
            "rate_change": f"{rate_change:+}%",
            "sentiment": sentiment,
            "risk": risk,
            "insight": insight
        }
        
    except Exception as e:
        # This will intercept the exact internal crash reason and scream it in the terminal log
        print(f"❌ CRITICAL BACKEND EXCEPTION: {str(e)}")
        return {"status": "error", "message": str(e)}

@app.get("/", response_class=HTMLResponse)
def dashboard():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>EcoPulse Intelligence Terminal</title>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
                background-color: #0c0e12;
                color: #e2e8f0;
                margin: 0;
                padding: 60px 20px;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                letter-spacing: -0.2px;
            }

            .terminal {
                background-color: #141822;
                border: 1px solid #232d3f;
                border-radius: 12px;
                padding: 40px;
                width: 100%;
                max-width: 760px;
                box-shadow: 0 30px 60px rgba(0, 0, 0, 0.4);
                transition: all 0.6s cubic-bezier(0.16, 1, 0.3, 1);
            }

            .terminal-header {
                display: flex;
                justify-content: space-between;
                align-items: baseline;
                border-bottom: 1px solid #232d3f;
                padding-bottom: 24px;
                margin-bottom: 32px;
            }

            .terminal-title {
                margin: 0;
                font-size: 16px;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 1.5px;
                color: #94a3b8;
                display: flex;
                align-items: center;
                gap: 8px;
            }

            .pulse-indicator {
                width: 6px;
                height: 6px;
                background-color: #38bdf8;
                border-radius: 50%;
                opacity: 0.8;
            }

            .system-status {
                font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
                font-size: 11px;
                color: #64748b;
                letter-spacing: 0.5px;
            }

            /* Asymmetrical Layout Blocks (Very Non-AI) */
            .main-display {
                display: grid;
                grid-template-columns: 1.2fr 1.8fr;
                gap: 32px;
                margin-bottom: 32px;
            }

            .primary-metric {
                display: flex;
                flex-direction: column;
                justify-content: center;
                border-right: 1px solid #232d3f;
                padding-right: 16px;
            }

            .metric-huge {
                font-size: 56px;
                font-weight: 700;
                line-height: 1;
                color: #ffffff;
                letter-spacing: -2px;
                margin: 8px 0;
            }

            .meta-pane {
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                gap: 16px;
            }

            .meta-row {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding-bottom: 8px;
                border-bottom: 1px dashed #1e293b;
            }

            .label {
                font-size: 13px;
                color: #64748b;
                font-weight: 500;
            }

            .value {
                font-size: 15px;
                font-weight: 600;
                color: #f1f5f9;
            }

            .insight-card {
                background: #0d111a;
                border: 1px solid #1e293b;
                border-radius: 8px;
                padding: 20px;
                margin-bottom: 32px;
            }

            .insight-text {
                margin: 0;
                font-size: 14px;
                line-height: 1.6;
                color: #94a3b8;
            }

            /* Bespoke Action Button */
            .action-btn {
                background-color: #f8fafc;
                color: #0f172a;
                border: none;
                padding: 16px 24px;
                font-size: 14px;
                font-weight: 600;
                border-radius: 8px;
                cursor: pointer;
                width: 100%;
                transition: all 0.2s ease;
                letter-spacing: 0.2px;
            }

            .action-btn:hover {
                background-color: #ffffff;
                transform: translateY(-1px);
                box-shadow: 0 4px 20px rgba(255, 255, 255, 0.1);
            }

            .action-btn:active {
                transform: translateY(0);
            }

            .placeholder-state {
                text-align: center;
                padding: 40px 0;
                color: #475569;
                font-size: 14px;
            }
        </style>
    </head>
    <body>

        <div class="terminal" id="terminal-wrapper">
            <div class="terminal-header">
                <h2 class="terminal-title"><span class="pulse-indicator" id="pulse"></span> EcoPulse Base</h2>
                <div class="system-status" id="status-text">SYS_IDLE // AWAITING_EXECUTION</div>
            </div>

            <div id="loading-view" class="placeholder-state">
                Click below to process the macroeconomic dataset query.
            </div>

            <div id="dashboard-view" style="display: none;">
                <div class="main-display">
                    <div class="primary-metric">
                        <span class="label">Fed Funds Rate</span>
                        <div class="metric-huge" id="ui-rate">0.00%</div>
                        <span class="label" id="ui-date">----(--)--</span>
                    </div>
                    
                    <div class="meta-pane">
                        <div class="meta-row">
                            <span class="label">MoM Velocity</span>
                            <span class="value" id="ui-delta" style="font-family: monospace;">0.00%</span>
                        </div>
                        <div class="meta-row">
                            <span class="label">Policy Classification</span>
                            <span class="value" id="ui-sentiment">—</span>
                        </div>
                        <div class="meta-row">
                            <span class="label">Risk Profile Mapping</span>
                            <span class="value" id="ui-risk">—</span>
                        </div>
                    </div>
                </div>

                <div class="insight-card">
                    <p class="insight-text" id="ui-insight">
                        System telemetry analysis column will compile upon data stream integration.
                    </p>
                </div>
            </div>

            <button class="action-btn" onclick="executePipeline()">Run Pipeline Analysis</button>
        </div>

        <script>
            async function executePipeline() {
                const loader = document.getElementById('loading-view');
                const view = document.getElementById('dashboard-view');
                const status = document.getElementById('status-text');
                const pulse = document.getElementById('pulse');
                const wrapper = document.getElementById('terminal-wrapper');

                loader.style.display = 'block';
                loader.innerText = "Querying local warehouse architecture...";
                status.innerText = "STATUS // EXECUTING_QUERIES";
                status.style.color = "#eab308";

                try {
                    const response = await fetch('/api/analysis');
                    const data = await response.json();

                    if (data.status === "error") {
                        loader.innerText = "ERR // DATABASE_TABLE_MISMATCH: " + data.message;
                        status.innerText = "STATUS // CRASH_LOG_POSTED";
                        status.style.color = "#f87171";
                        return;
                    }

                    loader.style.display = 'none';
                    view.style.display = 'block';
                    status.innerText = "STATUS // STREAM_ACTIVE";
                    status.style.color = "#64748b";

                    // Map fields
                    document.getElementById('ui-rate').innerText = data.current_rate + "%";
                    document.getElementById('ui-date').innerText = data.current_date;
                    document.getElementById('ui-delta').innerText = data.rate_change;
                    document.getElementById('ui-sentiment').innerText = data.sentiment;
                    document.getElementById('ui-risk').innerText = data.risk;
                    document.getElementById('ui-insight').innerText = data.insight;

                    // Sophisticated Human Design Touch: Dynamic color accents that fit real environments
                    if (data.sentiment.includes("DOVISH")) {
                        pulse.style.backgroundColor = "#4ade80";
                        document.getElementById('ui-delta').style.color = "#4ade80";
                        document.getElementById('ui-sentiment').style.color = "#4ade80";
                        wrapper.style.borderColor = "rgba(74, 222, 128, 0.15)";
                    } else if (data.sentiment.includes("HAWKISH")) {
                        pulse.style.backgroundColor = "#f87171";
                        document.getElementById('ui-delta').style.color = "#f87171";
                        document.getElementById('ui-sentiment').style.color = "#f87171";
                        wrapper.style.borderColor = "rgba(248, 113, 113, 0.15)";
                    }

                } catch (err) {
                    loader.innerText = "ERR // CONNECTION_FAILED";
                    status.innerText = "STATUS // LINK_OFFLINE";
                    status.style.color = "#f87171";
                }
            }
        </script>
    </body>
    </html>
    """