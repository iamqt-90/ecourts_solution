#!/usr/bin/env python3
"""
Run the optional web API server.
"""

from ecourts_scraper.api import app
from config import API_HOST, API_PORT, API_DEBUG

if __name__ == '__main__':
    print(f"Starting eCourts Scraper API server on {API_HOST}:{API_PORT}")
    app.run(debug=API_DEBUG, host=API_HOST, port=API_PORT)