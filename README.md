
# Honeypot Attack Monitoring System

## Overview
A beginner-friendly cybersecurity project that simulates a
honeypot login portal, records login attempts, stores events
in SQLite, and displays statistics using Streamlit.

## Features
- Simulated login portal
- Login-attempt logging
- SQLite database storage
- Dashboard with charts and statistics
- Recent event table
- CSV export from the dashboard

## Technologies
- Python
- SQLite
- Streamlit
- Pandas
- Plotly

## Project Files
- `honeypot.py` - Receives simulated login attempts
- `database.py` - Initializes and accesses the SQLite database
- `dashboard.py` - Displays monitoring statistics

## Setup

Install the required packages:

```bash
python -m pip install streamlit pandas plotly
```

Start the honeypot in one terminal:

```bash
python honeypot.py
```

Start the dashboard in another terminal:

```bash
python -m streamlit run dashboard.py
```

Open the local dashboard URL shown in the terminal.

## Safety Notice
This project is intended for educational use in a local lab.
It records simulated login attempts and does not prove that
a real attack occurred.
