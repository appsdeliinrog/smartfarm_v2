#!/usr/bin/env python3
"""
Simple PDF parser for Ministry crop price data
Uses basic text extraction and pattern matching - more reliable than complex table extraction
"""
import re
import json
import csv
import glob
import pathlib
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Tuple

import pdfplumber

# Commodity mappings
COMMODITIES = {
    'mahindi': 'maize',
    'mchele': 'rice', 
    'maharage': 'beans',
    'uwele': 'bulrush_millet',
    'mtama': 'sorghum',
    'ulezi': 'finger_millet',
    'ngano': 'wheat',
    'viazi mviringo': 'irish_potatoes'
}

# Month mappings
MONTHS = {
    'january': 1, 'februari': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6,
    'july': 7, 'august': 8, 'september': 9, 'october': 10, 'november': 11, 'december': 12,
    'januari': 1, 'februari': 2, 'machi': 3, 'aprili': 4, 'mei': 5, 'juni': 6,
    'julai': 7, 'agosti': 8, 'septemba': 9, 'oktoba': 10, 'novemba': 11, 'desemba': 12
}

@dataclass
class PriceRecord:
    date: str
    region: str
    market: str
    commodity: str
    price_type: str
    stat: str  # min or max
    price_per_kg: float
    unit: str
    source_file: str

def clean_text(text):
    """Clean and normalize text"""
    if not text:
        return ""
    return re.sub(r'\s+', ' ', str(text).strip().lower())

def extract_date_from_filename(filename):
    """Extract date from filename like 'Wholesale price 6th August, 2025.pdf'"""
    # Try pattern: number + month + year
    pattern = r'(\d+)(?:st|nd|rd|th)?\s+([a-z]+),?\s*(\d{4})'
    match = re.search(pattern, filename.lower())
    if match:
        day, month_name, year = match.groups()
        month_num = MONTHS.get(month_name.lower())
        if month_num:
            return f"{year}-{month_num:02d}-{int(day):02d}"
    return None

def parse_price(price_str):
    """Convert price string to float, handling commas and 'NA'"""
    if not price_str or str(price_str).upper() in ['NA', 'N/A', '-', '']:
        return None
    
    # Remove commas and spaces
    cleaned = re.sub(r'[,\s]', '', str(price_str))
    try:
        return float(cleaned)
    except:
        return None

def extract_text_from_pdf(pdf_path):
    """Extract all text from PDF"""
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
    return text

def parse_pdf_simple(pdf_path):
    """Parse PDF using simple text extraction and regex patterns"""
    records = []
    
    # Get date from filename
    date = extract_date_from_filename(pdf_path.name)
    if not date:
        print(f"Could not extract date from {pdf_path.name}")
        return records
    
    # Extract text
    text = extract_text_from_pdf(pdf_path)
    if not text:
        print(f"No text extracted from {pdf_path.name}")
        return records
    
    # Look for data patterns
    lines = text.split('\n')
    
    # Find lines that look like data rows (region + numbers)
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Skip header lines
        if any(word in line.lower() for word in ['region', 'mkoa', 'district', 'market', 'min price', 'max price']):
            continue
            
        # Look for lines with region names and numbers
        # Pattern: Region Market Number Number Number...
        parts = line.split()
        if len(parts) < 3:
            continue
            
        # First part should be region/location
        region = parts[0]
        market = parts[1] if len(parts) > 1 else region
        
        # Rest should be numbers (prices)
        numbers = []
        for part in parts[2:]:
            price = parse_price(part)
            if price is not None:
                numbers.append(price)
        
        if len(numbers) >= 2:  # Need at least min/max for one commodity
            # Simple assumption: pairs of numbers are min/max for commodities
            # This is a simplified approach - in real implementation we'd need
            # to match column headers to know which commodity each pair represents
            
            commodity_index = 0
            commodity_names = list(COMMODITIES.keys())
            
            for i in range(0, len(numbers), 2):
                if i + 1 < len(numbers) and commodity_index < len(commodity_names):
                    commodity = commodity_names[commodity_index]
                    min_price = numbers[i] / 100  # Convert from per 100kg to per kg
                    max_price = numbers[i + 1] / 100
                    
                    # Add min record
                    records.append(PriceRecord(
                        date=date,
                        region=region,
                        market=market,
                        commodity=COMMODITIES[commodity],
                        price_type='wholesale',
                        stat='min',
                        price_per_kg=min_price,
                        unit='kg',
                        source_file=pdf_path.name
                    ))
                    
                    # Add max record
                    records.append(PriceRecord(
                        date=date,
                        region=region,
                        market=market,
                        commodity=COMMODITIES[commodity],
                        price_type='wholesale',
                        stat='max',
                        price_per_kg=max_price,
                        unit='kg',
                        source_file=pdf_path.name
                    ))
                    
                    commodity_index += 1
    
    return records

def main():
    """Main parsing function"""
    pdf_dir = pathlib.Path("crop price pdf")
    output_dir = pathlib.Path("parser_output")
    output_dir.mkdir(exist_ok=True)
    
    all_records = []
    
    # Process all PDFs
    for pdf_path in pdf_dir.glob("*.pdf"):
        print(f"Processing {pdf_path.name}...")
        records = parse_pdf_simple(pdf_path)
        all_records.extend(records)
        print(f"  -> {len(records)} records extracted")
    
    # Save results
    if all_records:
        # Save as CSV
        csv_path = output_dir / "crop_prices.csv"
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'date', 'region', 'market', 'commodity', 'price_type', 
                'stat', 'price_per_kg', 'unit', 'source_file'
            ])
            writer.writeheader()
            for record in all_records:
                writer.writerow(asdict(record))
        
        # Save as JSON
        json_path = output_dir / "crop_prices.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump([asdict(r) for r in all_records], f, indent=2, ensure_ascii=False)
        
        print(f"\nResults saved:")
        print(f"  CSV: {csv_path}")
        print(f"  JSON: {json_path}")
        print(f"  Total records: {len(all_records)}")
    else:
        print("No records extracted from any PDF")

if __name__ == "__main__":
    main()
