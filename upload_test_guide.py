"""
PDF Upload Test Guide
====================

This script demonstrates how to upload a PDF through the Django admin.

Sample PDF Location:
C:\Users\fsociety\Documents\agri-open\crop price pdf\sw-1752847591-Wholesale price 30th May, 2025.pdf

Admin URL:
http://localhost:8000/admin/crops/pdfupload/add/

Steps:
1. Login to admin (admin/admin123)
2. Go to PDF uploads → Add PDF upload
3. Fill form:
   - File name: "Wholesale price 30th May 2025" (optional)
   - File path: Browse and select the PDF file
   - Status: "Uploaded" (default)
   - Import mode: "Skip Existing" (default)
4. Click Save
5. Select the uploaded PDF and run "Parse selected PDF files" action
6. Click on the PDF name and then "Preview" to see extracted data
7. Click "Import to Database" to save the data

Expected Result:
- PDF uploaded successfully
- Records parsed and displayed in preview
- Data imported to database
"""

import os

# Check if sample PDF exists
sample_pdf = "C:/Users/fsociety/Documents/agri-open/crop price pdf/sw-1752847591-Wholesale price 30th May, 2025.pdf"

if os.path.exists(sample_pdf):
    print("✅ Sample PDF found!")
    print(f"📁 File: {sample_pdf}")
    print(f"📊 Size: {os.path.getsize(sample_pdf)} bytes")
    print("\nYou can use this file for testing the upload.")
else:
    print("❌ Sample PDF not found!")
    print("Check if the file exists in the 'crop price pdf' folder.")

print("\n" + "="*50)
print("🌐 Admin URLs:")
print("Login: http://localhost:8000/admin/")
print("Upload: http://localhost:8000/admin/crops/pdfupload/add/")
print("List: http://localhost:8000/admin/crops/pdfupload/")
print("="*50)
