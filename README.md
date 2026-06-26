# EcoPulse AI: End-to-End Macroeconomic Intelligence Pipeline

EcoPulse AI is a full-stack analytical engine designed to ingest, cache, and evaluate key macroeconomic datasets. The pipeline monitors federal monetary shifts, executing automated algorithms to dynamically classify market risk layers and asset class sentiment in real-time.

---

##  System Architecture & Data Flow

The system is engineered as an event-driven data pipeline split into separate execution contexts:

* **Ingestion Layer (`fetch_macro_data.py`)**: Connects directly to external economic registries via HTTP requests to harvest raw macroeconomic points.
* **Persistence Caching (`ecopulse.db`)**: Enforces relational data typing constraints (`PRIMARY KEY`) using SQL transactional properties to guarantee absolute data integrity and prevent duplicate records.
* **Application Server (`main.py`)**: A high-performance **FastAPI REST API** wrapper running on an asynchronous loop to calculate delta variances across temporal intervals.
* **Presentation Engine (Asynchronous UI)**: A modern, non-blocking vanilla JavaScript terminal dashboard that asynchronously renders dynamic mutations based on incoming policy vectors.

---

##  Key Technical Features

* **Asynchronous Networking**: Built around a high-performance ASGI application layer (FastAPI & Uvicorn) to ensure scalable request handling.
* **Idempotent Storage Pipelines**: Database transactions avoid sequence mutation risks by utilizing strict local transactional schema rules (`INSERT OR IGNORE`) instead of basic global flat-file storage arrays.
* **Bespoke Responsive Layout System**: Designed with a clean financial data layout hierarchy using native responsive element rules, completely independent of external aesthetic framing heavy loads.

---

##  Local Installation & Deployment Routine

### Prerequisites
Ensure your environment running local runtimes is set up with:
* Python 3.10+
* Git configuration variables active

### Installation

1. Clone this repository locally:
```bash
git clone [https://github.com/lloyduk/ecopulse-macro-pipeline.git](https://github.com/lloyduk/ecopulse-macro-pipeline.git)
cd ecopulse-macro-pipeline

pip install fastapi uvicorn requests
python fetch_macro_data.py
python -m uvicorn main:app --reload
[http://127.0.0.1:8000](http://127.0.0.1:8000)
```bash
