"""
Export the agri-open project as a ZIP file
Excludes unnecessary files like node_modules, .git, __pycache__, etc.
"""
import os
import zipfile
import shutil
from pathlib import Path
from datetime import datetime

def should_exclude(file_path, exclude_patterns):
    """Check if a file/folder should be excluded"""
    path_str = str(file_path).replace('\\', '/')
    
    for pattern in exclude_patterns:
        if pattern in path_str:
            return True
    return False

def create_project_zip():
    """Create a ZIP file of the project"""
    
    project_root = Path(r'c:\Users\fsociety\Documents\agri-open')
    
    # Files and folders to exclude
    exclude_patterns = [
        'node_modules/',
        '.git/',
        '__pycache__/',
        '.venv/',
        '/.venv',
        '.env',
        '.DS_Store',
        'Thumbs.db',
        '*.pyc',
        '*.pyo',
        '*.pyd',
        '.pytest_cache/',
        '.coverage',
        'coverage.xml',
        '*.log',
        '.idea/',
        '.vscode/',
        'dist/',
        'build/',
        '.next/',
        '.nuxt/',
        # 'db.sqlite3',  # Include database file in export
        'media/',
        'staticfiles/',
        '*.tmp',
        '*.temp',
    ]
    
    # Create timestamp for the ZIP filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = f"agri-open-export-{timestamp}.zip"
    zip_path = project_root.parent / zip_filename
    
    print(f"🚀 Creating ZIP export: {zip_filename}")
    print(f"📁 Source directory: {project_root}")
    print(f"💾 Output location: {zip_path}")
    
    files_added = 0
    files_excluded = 0
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(project_root):
            # Filter out excluded directories
            dirs[:] = [d for d in dirs if not should_exclude(Path(root) / d, exclude_patterns)]
            
            for file in files:
                file_path = Path(root) / file
                
                if should_exclude(file_path, exclude_patterns):
                    files_excluded += 1
                    continue
                
                # Calculate relative path for the ZIP
                relative_path = file_path.relative_to(project_root)
                
                # Add file to ZIP
                zipf.write(file_path, relative_path)
                files_added += 1
                
                if files_added % 50 == 0:
                    print(f"   Added {files_added} files...")
    
    # Get ZIP file size
    zip_size = zip_path.stat().st_size
    zip_size_mb = zip_size / (1024 * 1024)
    
    print(f"\n✅ ZIP Export Complete!")
    print(f"📦 File: {zip_filename}")
    print(f"📊 Size: {zip_size_mb:.2f} MB")
    print(f"📄 Files included: {files_added}")
    print(f"🚫 Files excluded: {files_excluded}")
    print(f"📍 Location: {zip_path}")
    
    # Create a summary file
    summary_file = project_root.parent / f"export-summary-{timestamp}.txt"
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(f"Agri-Open Project Export Summary\n")
        f.write(f"{'='*40}\n\n")
        f.write(f"Export Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"ZIP File: {zip_filename}\n")
        f.write(f"Size: {zip_size_mb:.2f} MB\n")
        f.write(f"Files Included: {files_added}\n")
        f.write(f"Files Excluded: {files_excluded}\n\n")
        f.write(f"Project Structure:\n")
        f.write(f"- Backend: Django REST API\n")
        f.write(f"- Frontend: React + Vite\n")
        f.write(f"- Database: SQLite (included with data)\n")
        f.write(f"- PDF Processing: Python scripts\n")
        f.write(f"- Smart Commodity Matching: AI-powered normalization\n\n")
        f.write(f"Setup Instructions:\n")
        f.write(f"1. Extract ZIP file\n")
        f.write(f"2. Backend: pip install -r requirements.txt\n")
        f.write(f"3. Frontend: cd frontend && npm install\n")
        f.write(f"4. Database is included - no migration needed\n")
        f.write(f"5. Start backend: python manage.py runserver\n")
        f.write(f"6. Start frontend: cd frontend && npm run dev\n\n")
        f.write(f"Included Data:\n")
        f.write(f"- 6500+ price observations\n")
        f.write(f"- 9 commodity types with smart matching\n")
        f.write(f"- Historical data from Jan-Aug 2025\n")
        f.write(f"- All markets and regions\n")
    
    print(f"📋 Summary created: export-summary-{timestamp}.txt")
    
    return zip_path, summary_file

if __name__ == "__main__":
    try:
        zip_path, summary_path = create_project_zip()
        print(f"\n🎉 Export successful!")
        print(f"You can now share or backup: {zip_path}")
    except Exception as e:
        print(f"❌ Export failed: {e}")
        import traceback
        traceback.print_exc()
