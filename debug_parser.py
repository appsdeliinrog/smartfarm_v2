#!/usr/bin/env python3
"""
Debug PDF parser - examines PDFs to understand their structure
"""
import os
import glob
import pdfplumber
import json
from pathlib import Path

def debug_pdf(pdf_path):
    print(f"\n=== DEBUGGING: {pdf_path} ===")
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            print(f"Total pages: {len(pdf.pages)}")
            
            for i, page in enumerate(pdf.pages):
                print(f"\n--- Page {i+1} ---")
                
                # Extract raw text
                text = page.extract_text()
                if text:
                    print("Raw text (first 500 chars):")
                    print(repr(text[:500]))
                else:
                    print("No text extracted")
                
                # Try to extract tables
                tables = page.extract_tables()
                if tables:
                    print(f"Found {len(tables)} tables")
                    for j, table in enumerate(tables):
                        print(f"Table {j+1}: {len(table)} rows, {len(table[0]) if table else 0} cols")
                        if table:
                            print("First few rows:")
                            for row_idx, row in enumerate(table[:3]):
                                print(f"  Row {row_idx}: {row}")
                else:
                    print("No tables found")
                
                # Check for characters/objects
                chars = page.chars
                print(f"Characters found: {len(chars)}")
                
                # Check page size and layout
                print(f"Page size: {page.width} x {page.height}")
                
                # Only debug first page to avoid too much output
                if i == 0:
                    break
                    
    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")

def main():
    pdf_files = glob.glob("crop price pdf/*.pdf")
    
    if not pdf_files:
        print("No PDF files found in 'crop price pdf/' directory")
        return
    
    print(f"Found {len(pdf_files)} PDF files")
    
    # Debug first few PDFs
    for pdf_path in pdf_files[:3]:  # Only debug first 3 to avoid overwhelming output
        debug_pdf(pdf_path)
        print("\n" + "="*50)

if __name__ == "__main__":
    main()
