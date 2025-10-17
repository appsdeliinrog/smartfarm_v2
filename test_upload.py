"""
Quick test script to upload a PDF and demonstrate the admin interface
"""
import os
import django
import sys

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from crops.models import PDFUpload, PriceSource
from crops.services import PDFParsingService
from django.core.files.base import ContentFile
import shutil

def test_pdf_upload():
    """Test PDF upload functionality"""
    try:
        # Find a PDF file in the crop price pdf directory
        pdf_dir = r"c:\Users\fsociety\Documents\agri-open\crop price pdf"
        pdf_files = [f for f in os.listdir(pdf_dir) if f.endswith('.pdf')]
        
        if not pdf_files:
            print("No PDF files found in crop price pdf directory")
            return
        
        # Use the first PDF file
        test_pdf = pdf_files[0]
        pdf_path = os.path.join(pdf_dir, test_pdf)
        
        print(f"📄 Testing with PDF: {test_pdf}")
        
        # Get or create a price source
        source, created = PriceSource.objects.get_or_create(
            name="Ministry of Agriculture",
            defaults={
                'source_type': 'pdf',
                'is_active': True,
                'contact_info': 'Official price bulletins from Ministry of Agriculture'
            }
        )
        
        # Create PDFUpload instance
        with open(pdf_path, 'rb') as f:
            pdf_content = f.read()
        
        upload = PDFUpload.objects.create(
            file_name=test_pdf,
            file_size=len(pdf_content),
            uploaded_by='admin',
            import_mode='skip',
            source=source,
            notes=f'Test upload of {test_pdf}'
        )
        
        # Save the file content
        upload.file_path.save(test_pdf, ContentFile(pdf_content), save=True)
        
        print(f"✅ PDF uploaded successfully: ID {upload.id}")
        print(f"📊 File size: {upload.file_size:,} bytes")
        print(f"🔄 Status: {upload.get_status_display()}")
        print(f"💾 File path: {upload.file_path.name}")
        
        # Try to parse the PDF
        print("\n🔍 Attempting to parse PDF...")
        service = PDFParsingService()
        
        try:
            records_parsed, errors = service.parse_pdf(upload)
            print(f"✅ Parsing completed!")
            print(f"📈 Records parsed: {records_parsed}")
            if errors:
                print(f"⚠️ Errors: {len(errors)}")
                for error in errors[:3]:  # Show first 3 errors
                    print(f"   - {error}")
            
            # Refresh from database
            upload.refresh_from_db()
            print(f"🔄 New status: {upload.get_status_display()}")
            print(f"📊 Records in database: {upload.parsed_records.count()}")
            
        except Exception as e:
            print(f"❌ Parsing failed: {str(e)}")
        
        print(f"\n🌐 View in admin: http://127.0.0.1:8001/admin/crops/pdfupload/{upload.id}/change/")
        print(f"📋 All uploads: http://127.0.0.1:8001/admin/crops/pdfupload/")
        
        return upload
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return None

if __name__ == '__main__':
    test_pdf_upload()
