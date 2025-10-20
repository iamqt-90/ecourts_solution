"""
Configuration settings for eCourts Scraper.
"""

import os
from typing import Dict, Any

# eCourts platform settings
ECOURTS_BASE_URL = "https://ecourts.gov.in"
ECOURTS_SEARCH_ENDPOINT = "/ecourts_home/static/manuals/cis/"

# Request settings
REQUEST_TIMEOUT = 30
MAX_RETRIES = 3
RETRY_DELAY = 1

# Output settings
DEFAULT_OUTPUT_FORMAT = "json"
OUTPUT_DIRECTORY = "output"

# Logging settings
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# API settings (for optional web interface)
API_HOST = "0.0.0.0"
API_PORT = 5000
API_DEBUG = os.getenv("API_DEBUG", "False").lower() == "true"

# Date formats
DATE_FORMAT = "%d-%m-%Y"
DATETIME_FORMAT = "%d-%m-%Y %H:%M:%S"

# File settings
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {'.pdf', '.txt', '.json'}

# Error messages
ERROR_MESSAGES: Dict[str, str] = {
    "invalid_cnr": "Invalid CNR format. Please check and try again.",
    "invalid_case_details": "Invalid case details. Please provide valid case type, number, and year.",
    "network_error": "Network error occurred. Please check your internet connection.",
    "case_not_found": "Case not found for the specified date.",
    "pdf_not_available": "PDF document is not available for this case.",
    "causelist_error": "Error downloading cause list. Please try again later."
}