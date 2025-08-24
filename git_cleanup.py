#!/usr/bin/env python3
"""
Git Management Utility for WhatsApp Voice Agent V2
Helps identify and clean up large files that should be excluded from git
Prevents repository bloat and push timeouts
"""

import os
import glob
import shutil
import subprocess
from pathlib import Path

def format_size(size_bytes):
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    return f"{size_bytes:.1f} {size_names[i]}"

def get_git_tracked_files():
    """Get list of files currently tracked by git"""
    try:
        result = subprocess.run(['git', 'ls-files'], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip().split('\n') if result.stdout.strip() else []
        return []
    except Exception:
        return []

def check_large_tracked_files(min_size_mb=1):
    """Check for large files currently tracked by git"""
    tracked_files = get_git_tracked_files()
    large_tracked = []
    min_size_bytes = min_size_mb * 1024 * 1024
    
    for file_path in tracked_files:
        if os.path.exists(file_path):
            try:
                file_size = os.path.getsize(file_path)
                if file_size > min_size_bytes:
                    large_tracked.append({
                        'path': file_path,
                        'size': file_size,
                        'size_str': format_size(file_size)
                    })
            except (OSError, IOError):
                continue
    
    return sorted(large_tracked, key=lambda x: x['size'], reverse=True)

def find_large_files(directory=".", min_size_mb=1):
    """Find files larger than specified size"""
    large_files = []
    min_size_bytes = min_size_mb * 1024 * 1024
    
    for root, dirs, files in os.walk(directory):
        # Skip .git directory
        if '.git' in dirs:
            dirs.remove('.git')
        
        for file in files:
            file_path = os.path.join(root, file)
            try:
                file_size = os.path.getsize(file_path)
                if file_size > min_size_bytes:
                    large_files.append({
                        'path': file_path,
                        'size': file_size,
                        'size_str': format_size(file_size)
                    })
            except (OSError, IOError):
                continue
    
    return sorted(large_files, key=lambda x: x['size'], reverse=True)

def find_ignored_files():
    """Find files that should be ignored according to .gitignore patterns"""
    ignored_patterns = [
        # Audio files
        "**/*.wav", "**/*.mp3", "**/*.webm", "**/*.ogg", "**/*.m4a",
        # Temp files
        "**/temp_audio/*", "**/tmp*", "**/temp*",
        # Python cache
        "**/__pycache__/**", "**/*.pyc",
        # Virtual environment
        "**/venv/**", "**/env/**",
        # Logs
        "**/*.log", "**/logs/**",
        # Models (if any)
        "**/*.pt", "**/*.pth", "**/*.bin"
    ]
    
    ignored_files = []
    for pattern in ignored_patterns:
        files = glob.glob(pattern, recursive=True)
        ignored_files.extend(files)
    
    return ignored_files

def clean_temp_files():
    """Clean up temporary files that should not be in git"""
    cleaned = []
    
    # Clean temp audio files
    temp_audio_dir = "backend/temp_audio"
    if os.path.exists(temp_audio_dir):
        for file in os.listdir(temp_audio_dir):
            if file.endswith(('.wav', '.webm', '.ogg', '.mp3')):
                file_path = os.path.join(temp_audio_dir, file)
                try:
                    os.remove(file_path)
                    cleaned.append(file_path)
                except OSError:
                    pass
    
    # Clean Python cache
    for root, dirs, files in os.walk("."):
        if '__pycache__' in dirs:
            cache_dir = os.path.join(root, '__pycache__')
            try:
                shutil.rmtree(cache_dir)
                cleaned.append(cache_dir)
            except OSError:
                pass
        
        # Remove .pyc files
        for file in files:
            if file.endswith('.pyc'):
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    cleaned.append(file_path)
                except OSError:
                    pass
    
    return cleaned

def check_git_status():
    """Check current git status"""
    if os.path.exists('.git'):
        print("✅ Git repository found")
        return True
    else:
        print("❌ No git repository found. Run 'git init' first.")
        return False

def main():
    """Main function"""
    print("🔍 Git Management Utility for WhatsApp Voice Agent V2")
    print("=" * 60)
    
    # Check git status
    if not check_git_status():
        return
    
    # Check for large files currently tracked by git (CRITICAL CHECK)
    print("\n⚠️ Checking for large files currently tracked by git...")
    large_tracked = check_large_tracked_files(min_size_mb=1)
    
    if large_tracked:
        print(f"\n🚨 CRITICAL: Found {len(large_tracked)} large files being tracked by git!")
        print("These files are causing push timeouts and should be removed:")
        total_size = 0
        for file_info in large_tracked:
            print(f"   {file_info['size_str']:>8} - {file_info['path']}")
            total_size += file_info['size']
        
        print(f"\n📈 Total size being tracked: {format_size(total_size)}")
        print("\n🛠️ To fix this, run:")
        for file_info in large_tracked:
            print(f"   git rm --cached '{file_info['path']}'")
        print("   git commit -m 'Remove large files from tracking'")
        
        return
    else:
        print("✅ No large files currently tracked by git")
    
    # Find large files
    print("\n📊 Searching for large files (>1MB)...")
    large_files = find_large_files(min_size_mb=1)
    
    if large_files:
        print(f"\n📋 Found {len(large_files)} large files:")
        for file_info in large_files[:10]:  # Show top 10
            print(f"   {file_info['size_str']:>8} - {file_info['path']}")
        
        if len(large_files) > 10:
            print(f"   ... and {len(large_files) - 10} more files")
    else:
        print("✅ No large files found")
    
    # Find ignored files that exist
    print("\n🔍 Checking for files that should be ignored...")
    ignored_files = find_ignored_files()
    
    if ignored_files:
        print(f"\n⚠️ Found {len(ignored_files)} files that should be ignored:")
        for file in ignored_files[:15]:  # Show first 15
            if os.path.exists(file):
                size = format_size(os.path.getsize(file))
                print(f"   {size:>8} - {file}")
        
        if len(ignored_files) > 15:
            print(f"   ... and {len(ignored_files) - 15} more files")
    
    # Ask if user wants to clean
    print("\n🧹 Clean up temporary files?")
    print("   This will remove:")
    print("   - Temporary audio files (*.wav, *.webm in temp_audio/)")
    print("   - Python cache (__pycache__/, *.pyc)")
    print("   - Log files")
    
    response = input("\nProceed with cleanup? (y/N): ").lower().strip()
    
    if response == 'y' or response == 'yes':
        print("\n🧹 Cleaning up...")
        cleaned = clean_temp_files()
        
        if cleaned:
            print(f"✅ Cleaned {len(cleaned)} files/directories:")
            for item in cleaned[:10]:
                print(f"   - {item}")
            if len(cleaned) > 10:
                print(f"   ... and {len(cleaned) - 10} more items")
        else:
            print("✅ No files to clean")
    else:
        print("⏸️ Cleanup skipped")
    
    # Git recommendations
    print("\n📝 Git Recommendations:")
    print("   1. Add all files to git: git add .")
    print("   2. Commit changes: git commit -m 'Add project files'")
    print("   3. The .gitignore will prevent large files from being added")
    print("   4. Run this script periodically to clean temp files")
    
    print("\n✅ Git management complete!")

if __name__ == "__main__":
    main()