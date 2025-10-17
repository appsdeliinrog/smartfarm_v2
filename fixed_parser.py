#!/usr/bin/env python3
"""
Fixed PDF parser for Ministry crop price data
"""
import os
import glob
import pdfplumber
import json
import csv
import re
from pathlib import Path
from datetime import datetime

# Swahili month mapping
SWAHILI_MONTHS = {
    'JANUARI': 1, 'FEBRUARI': 2, 'MACHI': 3, 'APRILI': 4, 'MEI': 5, 'JUNI': 6,
    'JULAI': 7, 'AGOSTI': 8, 'SEPTEMBA': 9, 'OKTOBA': 10, 'NOVEMBA': 11, 'DESEMBA': 12
}

# Commodity mapping (based on header order in PDFs)
COMMODITIES = [
    'Maize (Mahindi)',
    'Rice (Mchele)', 
    'Sorghum (Mtama)',
    'Bulrush Millet (Uwele)',
    'Finger Millet (Ulezi)',
    'Wheat Grain (Ngano)',
    'Beans (Maharage)',
    'Irish Potatoes (Viazi Mviringo)'
]

def clean_price(price_str):
    """Clean price string and convert to float"""
    if price_str is None or price_str == '':
        return None
    
    # Handle numeric input (already a float/int)
    if isinstance(price_str, (int, float)):
        return float(price_str) if price_str > 0 else None
    
    # Handle string input
    price_str = str(price_str)
    if price_str.upper() == 'NA' or price_str.strip() == '':
        return None
    
    # Remove spaces and commas, handle OCR artifacts
    cleaned = price_str.replace(' ', '').replace(',', '').replace("'", '').strip()
    
    try:
        return float(cleaned)
    except:
        return None

def extract_date_from_filename(filename):
    """Extract date from PDF filename"""
    # Pattern for dates like "30th May, 2025", "9th July,2025", "10TH SEPTEMBER, 2025"
    # Make the ordinal suffix case-insensitive and optional
    date_pattern = r'(\d{1,2})(?:st|nd|rd|th|ST|ND|RD|TH)?\s+([A-Za-z]+),?\s*(\d{4})'
    
    match = re.search(date_pattern, filename, re.IGNORECASE)
    if match:
        day = int(match.group(1))
        month_name = match.group(2).upper()  # Convert to uppercase for consistent lookup
        year = int(match.group(3))
        
        # Month name mapping (English)
        english_months = {
            'JANUARY': 1, 'FEBRUARY': 2, 'MARCH': 3, 'APRIL': 4, 'MAY': 5, 'JUNE': 6,
            'JULY': 7, 'AUGUST': 8, 'SEPTEMBER': 9, 'OCTOBER': 10, 'NOVEMBER': 11, 'DECEMBER': 12
        }
        
        month = english_months.get(month_name) or SWAHILI_MONTHS.get(month_name)
        if month:
            return f"{year}-{month:02d}-{day:02d}"
    
    return None

def extract_date_from_text(text):
    """Extract date from PDF header text"""
    # Pattern for dates like "18 JULAI, 2025" or "30JULAI, 2025"
    date_pattern = r'(\d{1,2})\s*([A-Z]+),?\s*(\d{4})'
    
    match = re.search(date_pattern, text.upper())
    if match:
        day = int(match.group(1))
        month_name = match.group(2)
        year = int(match.group(3))
        
        month = SWAHILI_MONTHS.get(month_name)
        if month:
            return f"{year}-{month:02d}-{day:02d}"
    
    return None

def parse_pdf(pdf_path):
    """Parse a single PDF file"""
    records = []
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            # Extract date from first page text
            first_page_text = pdf.pages[0].extract_text() or ""
            report_date = extract_date_from_text(first_page_text)
            
            # If date extraction from content fails, try filename
            if not report_date:
                filename = os.path.basename(pdf_path)
                report_date = extract_date_from_filename(filename)
                print(f"  -> Using date from filename: {report_date}")
            else:
                print(f"  -> Using date from PDF content: {report_date}")
            
            # Extract table from first page
            tables = pdf.pages[0].extract_tables()
            
            if not tables:
                print(f"  -> No tables found in {pdf_path}")
                return []
            
            table = tables[0]  # Use first table
            
            if len(table) < 2:
                print(f"  -> Table too small in {pdf_path}")
                return []
            
            # Process each data row (skip header if present)
            for row in table:
                if not row or len(row) < 3:
                    continue
                    
                # Skip header rows
                if any(x and ('Region' in str(x) or 'Mkoa' in str(x) or 'Min Price' in str(x)) for x in row[:3]):
                    continue
                
                region = str(row[0]).strip() if row[0] else ""
                market = str(row[1]).strip() if row[1] else ""
                
                # Skip empty rows
                if not region and not market:
                    continue
                
                # Process commodity prices (8 commodities, 2 columns each = 16 price columns)
                # Starting from column 2, each commodity has Min Price, Max Price
                price_cols = row[2:18]  # Columns 2-17 contain the price data
                
                for i, commodity in enumerate(COMMODITIES):
                    if i * 2 + 1 < len(price_cols):  # Ensure we have both min and max columns
                        min_price = clean_price(price_cols[i * 2])
                        max_price = clean_price(price_cols[i * 2 + 1])
                        
                        # Create records for min and max prices
                        if min_price is not None:
                            records.append({
                                'date': report_date,
                                'region': region,
                                'market': market,
                                'commodity': commodity,
                                'price_type': 'wholesale',
                                'stat': 'min',
                                'price_per_100kg': min_price,
                                'price_per_kg': round(min_price / 100, 2),
                                'currency': 'TZS',
                                'source_file': os.path.basename(pdf_path)
                            })
                        
                        if max_price is not None:
                            records.append({
                                'date': report_date,
                                'region': region,
                                'market': market,
                                'commodity': commodity,
                                'price_type': 'wholesale',
                                'stat': 'max',
                                'price_per_100kg': max_price,
                                'price_per_kg': round(max_price / 100, 2),
                                'currency': 'TZS',
                                'source_file': os.path.basename(pdf_path)
                            })
    
    except Exception as e:
        print(f"  -> Error processing {pdf_path}: {e}")
        return []
    
    return records

def main():
    # Find all PDF files
    pdf_files = glob.glob("crop price pdf/*.pdf")
    
    if not pdf_files:
        print("No PDF files found in 'crop price pdf/' directory")
        return
    
    print(f"Found {len(pdf_files)} PDF files")
    
    all_records = []
    
    for pdf_path in pdf_files:
        print(f"Processing {os.path.basename(pdf_path)}...")
        records = parse_pdf(pdf_path)
        print(f"  -> {len(records)} records extracted")
        all_records.extend(records)
    
    # Remove duplicates based on key fields
    seen = set()
    unique_records = []
    
    for record in all_records:
        key = (record['date'], record['region'], record['market'], 
               record['commodity'], record['stat'])
        if key not in seen:
            seen.add(key)
            unique_records.append(record)
    
    print(f"\nAfter deduplication: {len(unique_records)} unique records")
    
    if unique_records:
        # Create output directory
        os.makedirs("parser_output", exist_ok=True)
        
        # Save as JSON
        with open("parser_output/crop_prices.json", "w", encoding="utf-8") as f:
            json.dump(unique_records, f, indent=2, ensure_ascii=False)
        
        # Save as CSV
        with open("parser_output/crop_prices.csv", "w", newline="", encoding="utf-8") as f:
            fieldnames = ['date', 'region', 'market', 'commodity', 'price_type', 'stat', 
                         'price_per_100kg', 'price_per_kg', 'currency', 'source_file']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(unique_records)
        
        print(f"Results saved to:")
        print(f"  - parser_output/crop_prices.json")
        print(f"  - parser_output/crop_prices.csv")
        
        # Show sample data
        print(f"\nSample records:")
        for i, record in enumerate(unique_records[:5]):
            print(f"  {i+1}. {record['date']} | {record['region']} | {record['market']} | {record['commodity']} | {record['stat']}: {record['price_per_kg']} TZS/kg")
        
        # Show statistics
        dates = set(r['date'] for r in unique_records if r['date'])
        regions = set(r['region'] for r in unique_records)
        commodities = set(r['commodity'] for r in unique_records)
        
        print(f"\nStatistics:")
        print(f"  - Dates covered: {len(dates)} ({sorted(dates)})")
        print(f"  - Regions: {len(regions)}")
        print(f"  - Commodities: {len(commodities)}")
        
    else:
        print("No records extracted")

if __name__ == "__main__":
    main()
