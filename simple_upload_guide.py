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

print("\n📋 UPLOAD STEPS:")
print("1. Go to: http://localhost:8000/admin/crops/pdfupload/add/")
print("2. Click 'Choose File' and select the PDF")
print("3. Leave other fields as default")
print("4. Click 'Save'")
print("5. Go back to PDF list and select your upload")
print("6. Choose action: 'Parse selected PDF files' and click 'Go'")
print("7. Click on your PDF name to view details")
print("8. Click 'Preview' to see extracted data")
print("9. Click 'Import to Database' to save the data")
