#!/usr/bin/env python3
"""
Simple regex test for date extraction
"""
import re

def test_extract_date_from_filename(filename):
    """Extract date from PDF filename - test version"""
    # Pattern for dates like "30th May, 2025", "9th July,2025", "10TH SEPTEMBER, 2025"
    date_pattern = r'(\d{1,2})(?:st|nd|rd|th|ST|ND|RD|TH)?\s+([A-Za-z]+),?\s*(\d{4})'
    
    match = re.search(date_pattern, filename, re.IGNORECASE)
    if match:
        day = int(match.group(1))
        month_name = match.group(2).upper()
        year = int(match.group(3))
        
        # Month name mapping (English)
        english_months = {
            'JANUARY': 1, 'FEBRUARY': 2, 'MARCH': 3, 'APRIL': 4, 'MAY': 5, 'JUNE': 6,
            'JULY': 7, 'AUGUST': 8, 'SEPTEMBER': 9, 'OCTOBER': 10, 'NOVEMBER': 11, 'DECEMBER': 12
        }
        
        month = english_months.get(month_name)
        if month:
            return f"{year}-{month:02d}-{day:02d}"
    
    return None

# Test cases
test_cases = [
    "sw-1758182447-Wholesale price 10TH SEPTEMBER, 2025.pdf",  # Failing case
    "sw-1752844676-Wholesale price 28th April, 2025.pdf",      # Working case
    "sw-1234567890-Wholesale price 1st January, 2025.pdf",     # Edge case
    "sw-1234567890-Wholesale price 31ST DECEMBER, 2025.pdf",   # Uppercase edge case
]

print("=== Testing Date Extraction Fix ===")
for filename in test_cases:
    extracted_date = test_extract_date_from_filename(filename)
    status = "✅ SUCCESS" if extracted_date else "❌ FAILED"
    print(f"{status}: {filename}")
    print(f"    Extracted: {extracted_date}")
    print()
