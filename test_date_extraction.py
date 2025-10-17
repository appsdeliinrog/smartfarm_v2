#!/usr/bin/env python3
"""
Test script to verify date extraction fix
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fixed_parser import extract_date_from_filename

# Test cases
test_cases = [
    "sw-1758182447-Wholesale price 10TH SEPTEMBER, 2025.pdf",  # Failing case
    "sw-1752844676-Wholesale price 28th April, 2025.pdf",      # Working case
    "sw-1234567890-Wholesale price 1st January, 2025.pdf",     # Edge case
    "sw-1234567890-Wholesale price 31ST DECEMBER, 2025.pdf",   # Uppercase edge case
]

print("=== Testing Date Extraction Fix ===")
for filename in test_cases:
    extracted_date = extract_date_from_filename(filename)
    status = "✅ SUCCESS" if extracted_date else "❌ FAILED"
    print(f"{status}: {filename}")
    print(f"    Extracted: {extracted_date}")
    print()
