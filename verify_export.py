"""
Verify the exported ZIP contains all necessary files
"""
import zipfile
import os
from pathlib import Path

def verify_export():
    """Verify the latest export ZIP"""
    
    # Find the latest export ZIP
    export_dir = Path(r'c:\Users\fsociety\Documents')
    zip_files = list(export_dir.glob('agri-open-export-*.zip'))
    
    if not zip_files:
        print("❌ No export ZIP files found!")
        return
    
    latest_zip = max(zip_files, key=os.path.getctime)
    print(f"🔍 Verifying: {latest_zip.name}")
    
    essential_files = [
        'manage.py',
        'requirements.txt',
        'requirements_production.txt',
        'db.sqlite3',
        'README_EXPORT.md',
        'backend/settings.py',
        'backend/urls.py',
        'crops/models.py',
        'crops/views.py',
        'crops/services.py',
        'crops/commodity_matching.py',
        'frontend/package.json',
        'frontend/src/App.jsx',
        'frontend/src/components/Dashboard.jsx',
        'frontend/src/components/FilterBar.jsx',
        'frontend/src/components/PriceGrid.jsx',
        'fixed_parser.py',
    ]
    
    essential_dirs = [
        'backend/',
        'crops/',
        'frontend/',
        'frontend/src/',
        'frontend/src/components/',
        'frontend/src/pages/',
        'frontend/src/hooks/',
        'frontend/src/utils/',
    ]
    
    with zipfile.ZipFile(latest_zip, 'r') as zf:
        file_list = zf.namelist()
        
        print(f"\n📦 ZIP Contents Summary:")
        print(f"Total files: {len(file_list)}")
        
        # Check essential files
        missing_files = []
        for file in essential_files:
            if file not in file_list:
                missing_files.append(file)
            else:
                print(f"✅ {file}")
        
        # Check essential directories
        missing_dirs = []
        for dir_name in essential_dirs:
            if not any(f.startswith(dir_name) for f in file_list):
                missing_dirs.append(dir_name)
            else:
                print(f"✅ {dir_name}")
        
        # Check database
        if 'db.sqlite3' in file_list:
            db_info = zf.getinfo('db.sqlite3')
            db_size_mb = db_info.file_size / (1024 * 1024)
            print(f"✅ Database included: {db_size_mb:.2f} MB")
        else:
            print("❌ Database missing!")
        
        # Show file type distribution
        file_types = {}
        for file in file_list:
            ext = Path(file).suffix.lower()
            if ext:
                file_types[ext] = file_types.get(ext, 0) + 1
        
        print(f"\n📊 File Type Distribution:")
        for ext, count in sorted(file_types.items()):
            print(f"  {ext}: {count} files")
        
        if missing_files:
            print(f"\n❌ Missing essential files:")
            for file in missing_files:
                print(f"  - {file}")
        
        if missing_dirs:
            print(f"\n❌ Missing essential directories:")
            for dir_name in missing_dirs:
                print(f"  - {dir_name}")
        
        if not missing_files and not missing_dirs:
            print(f"\n✅ Export verification successful!")
            print(f"📦 {latest_zip.name} contains all essential files")
            
            # Calculate total size
            total_size = sum(zf.getinfo(f).file_size for f in file_list)
            total_size_mb = total_size / (1024 * 1024)
            print(f"📊 Total extracted size: {total_size_mb:.2f} MB")
        else:
            print(f"\n⚠️  Export has missing components!")

if __name__ == "__main__":
    verify_export()
