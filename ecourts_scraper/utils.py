"""
Utility functions for eCourts Scraper.
"""

import json
import os
from datetime import datetime
from typing import Dict, Any


def format_date(date: datetime) -> str:
    """Format date for eCourts API."""
    return date.strftime("%d-%m-%Y")


def save_results(data: Dict[str, Any], filename: str, format_type: str = 'json') -> str:
    """Save results to file in specified format."""
    
    # Create output directory if it doesn't exist
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    if format_type == 'json':
        filepath = os.path.join(output_dir, f"{filename}.json")
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    else:  # text format
        filepath = os.path.join(output_dir, f"{filename}.txt")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(format_text_output(data))
    
    return filepath


def format_text_output(data: Dict[str, Any]) -> str:
    """Format data as readable text."""
    lines = []
    lines.append("eCourts Scraper Results")
    lines.append("=" * 25)
    lines.append("")
    
    for key, value in data.items():
        if isinstance(value, dict):
            lines.append(f"{key.upper()}:")
            for sub_key, sub_value in value.items():
                lines.append(f"  {sub_key}: {sub_value}")
        elif isinstance(value, list):
            lines.append(f"{key.upper()}:")
            for i, item in enumerate(value, 1):
                if isinstance(item, dict):
                    lines.append(f"  {i}. {item}")
                else:
                    lines.append(f"  {i}. {item}")
        else:
            lines.append(f"{key}: {value}")
    
    return "\n".join(lines)


def validate_cnr(cnr: str) -> bool:
    """Validate CNR format."""
    # Allow demo CNR for testing
    if cnr and cnr.upper() == 'DEMO123':
        return True
    
    # Basic CNR validation - adjust based on actual format requirements
    if not cnr or len(cnr) < 10:
        return False
    return True


def validate_case_details(case_type: str, case_number: str, case_year: str) -> bool:
    """Validate case details format."""
    if not all([case_type, case_number, case_year]):
        return False
    
    try:
        year = int(case_year)
        if year < 1950 or year > datetime.now().year:
            return False
    except ValueError:
        return False
    
    return True