#!/usr/bin/env python3
"""
Improved PDF parser for Ministry crop price data
Better handles the table structure from the sample you provided
"""
import re
import json
import csv
import pathlib
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Tuple
import pdfplumber

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
    confidence: str = "high"

# Month mappings
MONTHS = {
    'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6,
    'july': 7, 'august': 8, 'september': 9, 'october': 10, 'november': 11, 'december': 12,
    'januari': 1, 'februari': 2, 'machi': 3, 'aprili': 4, 'mei': 5, 'juni': 6,
    'julai': 7, 'agosti': 8, 'septemba': 9, 'oktoba': 10, 'novemba': 11, 'desemba': 12
}

# Commodity column patterns
COMMODITY_PATTERNS = [
    (r'maize|mahindi', 'maize'),
    (r'rice|mchele', 'rice'),
    (r'beans|maharage', 'beans'),
    (r'millet|uwele', 'bulrush_millet'),
    (r'sorghum|mtama', 'sorghum'),
    (r'finger.*millet|ulezi', 'finger_millet'),
    (r'wheat|ngano', 'wheat'),
    (r'potato|viazi.*mviringo', 'irish_potatoes')
]

def extract_date_from_filename(filename):
    """Extract date from filename"""
    pattern = r'(\d+)(?:st|nd|rd|th)?\s+([a-z]+),?\s*(\d{4})'
    match = re.search(pattern, filename.lower())
    if match:
        day, month_name, year = match.groups()
        month_num = MONTHS.get(month_name.lower())
        if month_num:
            return f"{year}-{month_num:02d}-{int(day):02d}"
    return "unknown"

def parse_price(price_str):
    """Convert price string to float"""
    if not price_str or str(price_str).upper() in ['NA', 'N/A', '-', '']:
        return None
    
    cleaned = re.sub(r'[,\s]', '', str(price_str))
    try:
        val = float(cleaned)
        return val if val > 0 else None
    except:
        return None

def parse_pdf_with_tables(pdf_path):
    """Parse PDF using table extraction"""
    records = []
    date = extract_date_from_filename(pdf_path.name)
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                # Try to extract tables
                tables = page.extract_tables()
                
                for table in tables or []:
                    if not table or len(table) < 2:
                        continue
                    
                    # Look for header row with commodities
                    header_row = None
                    for i, row in enumerate(table[:5]):  # Check first 5 rows
                        row_text = ' '.join([str(cell) for cell in row if cell]).lower()
                        if any(pattern[0] in row_text for pattern, _ in COMMODITY_PATTERNS):
                            header_row = i
                            break
                    
                    if header_row is None:
                        continue
                    
                    headers = table[header_row]
                    data_rows = table[header_row + 1:]
                    
                    # Map commodity columns
                    commodity_cols = {}
                    for col_idx, header in enumerate(headers):
                        if not header:
                            continue
                        header_lower = str(header).lower()
                        for pattern, commodity in COMMODITY_PATTERNS:
                            if re.search(pattern, header_lower):
                                # Look for min/max columns nearby
                                min_col = col_idx
                                max_col = col_idx + 1 if col_idx + 1 < len(headers) else None
                                
                                # Try to find actual min/max columns
                                for offset in range(1, 4):
                                    if col_idx + offset < len(headers):
                                        next_header = str(headers[col_idx + offset] or '').lower()
                                        if 'min' in next_header:
                                            min_col = col_idx + offset
                                        elif 'max' in next_header:
                                            max_col = col_idx + offset
                                
                                commodity_cols[commodity] = {'min': min_col, 'max': max_col}
                                break
                    
                    # Process data rows
                    for row in data_rows:
                        if not row or len(row) < 2:
                            continue
                        
                        # Extract region and market
                        region = str(row[0] or '').strip()
                        market = str(row[1] or '').strip() if len(row) > 1 else region
                        
                        if not region or region.lower() in ['region', 'mkoa']:
                            continue
                        
                        # Clean up location names
                        region = region.replace('saalam', 'Salaam').title()
                        market = market.replace('saalam', 'Salaam').title()
                        
                        # Extract prices for each commodity
                        for commodity, cols in commodity_cols.items():
                            min_col = cols.get('min')
                            max_col = cols.get('max')
                            
                            if min_col is not None and min_col < len(row):
                                min_price = parse_price(row[min_col])
                                if min_price:
                                    records.append(PriceRecord(
                                        date=date,
                                        region=region,
                                        market=market,
                                        commodity=commodity,
                                        price_type='wholesale',
                                        stat='min',
                                        price_per_kg=min_price / 100.0,  # Convert from per 100kg
                                        unit='kg',
                                        source_file=pdf_path.name
                                    ))
                            
                            if max_col is not None and max_col < len(row):
                                max_price = parse_price(row[max_col])
                                if max_price:
                                    records.append(PriceRecord(
                                        date=date,
                                        region=region,
                                        market=market,
                                        commodity=commodity,
                                        price_type='wholesale',
                                        stat='max',
                                        price_per_kg=max_price / 100.0,  # Convert from per 100kg
                                        unit='kg',
                                        source_file=pdf_path.name
                                    ))
    
    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")
    
    return records

def main():
    """Main function"""
    pdf_dir = pathlib.Path("crop price pdf")
    output_dir = pathlib.Path("parser_output")
    output_dir.mkdir(exist_ok=True)
    
    all_records = []
    summary = {}
    
    # Process all PDFs
    for pdf_path in pdf_dir.glob("*.pdf"):
        print(f"Processing {pdf_path.name}...")
        records = parse_pdf_with_tables(pdf_path)
        all_records.extend(records)
        summary[pdf_path.name] = len(records)
        print(f"  -> {len(records)} records extracted")
    
    # Remove duplicates and sort
    unique_records = []
    seen = set()
    for record in all_records:
        key = (record.date, record.region, record.market, record.commodity, record.stat)
        if key not in seen:
            seen.add(key)
            unique_records.append(record)
    
    print(f"\nAfter deduplication: {len(unique_records)} unique records")
    
    if unique_records:
        # Save as CSV
        csv_path = output_dir / "parsed_prices.csv"
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'date', 'region', 'market', 'commodity', 'price_type', 
                'stat', 'price_per_kg', 'unit', 'source_file', 'confidence'
            ])
            writer.writeheader()
            for record in sorted(unique_records, key=lambda x: (x.date, x.region, x.commodity)):
                writer.writerow(asdict(record))
        
        # Save summary
        summary_path = output_dir / "parsing_summary.json"
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump({
                'total_files': len(summary),
                'total_records': len(unique_records),
                'files': summary,
                'commodities': list(set(r.commodity for r in unique_records)),
                'regions': list(set(r.region for r in unique_records)),
                'date_range': {
                    'start': min(r.date for r in unique_records),
                    'end': max(r.date for r in unique_records)
                }
            }, f, indent=2)
        
        print(f"\nResults saved:")
        print(f"  CSV: {csv_path}")
        print(f"  Summary: {summary_path}")
        print(f"\nSample data:")
        for i, record in enumerate(unique_records[:5]):
            print(f"  {record.date} | {record.region} {record.market} | {record.commodity} {record.stat}: {record.price_per_kg:.2f} TZS/kg")
    
    else:
        print("No records extracted")

if __name__ == "__main__":
    main()
