#!/usr/bin/env python3
"""
🔧 DEPENDENCY CONFLICTS SOLVER

This script checks for and resolves common dependency conflicts
in the WhatsApp Voice Agent with CoquiTTS integration.

Run this script to:
1. Detect conflicts between tokenizers, transformers, and TTS
2. Suggest fixes for version incompatibilities
3. Verify if the environment is ready for TTS functionality
"""

import sys
import subprocess
import pkg_resources
import importlib.util
import os

def check_package_version(package_name, target_version):
    """Check if a package is installed and matches version"""
    try:
        spec = importlib.util.find_spec(package_name)
        if spec is None:
            print(f"❌ Package '{package_name}' is not installed")
            return False

        try:
            version = pkg_resources.get_distribution(package_name).version
            if target_version in version:
                print(f"✅ {package_name} {version} (correct)")
                return True
            else:
                print(f"⚠️  {package_name} {version} (expected {target_version})")
                return False
        except pkg_resources.DistributionNotFound:
            print(f"❌ Cannot get version for {package_name}")
            return False

    except ImportError:
        print(f"❌ Import error for {package_name}")
        return False

def check_conflicts():
    """Check for known dependency conflicts"""
    print("🔍 Checking for dependency conflicts...")
    print()

    conflicts = []

    # Check tokenizers version
    if not check_package_version('tokenizers', '0.13.3'):
        conflicts.append({
            'package': 'tokenizers',
            'current': 'unknown',
            'required': '0.13.3',
            'reason': 'faster-whisper compatibility'
        })

    # Check transformers version
    if not check_package_version('transformers', '4.31.0'):
        conflicts.append({
            'package': 'transformers',
            'current': 'unknown',
            'required': '4.31.0',
            'reason': 'CoquiTTS compatibility'
        })

    # Check faster-whisper
    if not check_package_version('faster_whisper', '1.0.1'):
        conflicts.append({
            'package': 'faster_whisper',
            'current': 'unknown',
            'required': '1.0.1',
            'reason': 'STT functionality'
        })

    # Check TTS
    if not check_package_version('TTS', '0.22.0'):
        conflicts.append({
            'package': 'TTS',
            'current': 'unknown',
            'required': '0.22.0',
            'reason': 'Voice synthesis'
        })

    return conflicts

def generate_fix_commands(conflicts):
    """Generate commands to fix conflicts"""
    if not conflicts:
        return []

    commands = [
        "REM Fix dependency conflicts:",
        "echo Installing dependencies in correct order...",
        ""
    ]

    # Uninstall problematic packages first
    for conflict in conflicts:
        pkg = conflict['package']
        if pkg in ['tokenizers', 'transformers']:
            commands.append(f"pip uninstall -y {pkg}")

    # Install in correct order
    commands.extend([
        "",
        "REM Install in correct order:",
        "pip install tokenizers==0.13.3",
        "pip install transformers==4.31.0",
        "pip install faster-whisper==1.0.1",
        "pip install \"TTS==0.22.0\"",
        ""
    ])

    return commands

def create_fix_script(conflicts):
    """Create a fix script for the user"""
    if not conflicts:
        print("✅ No conflicts found! Environment looks good.")
        return True

    print("⚠️  Found dependency conflicts!")
    print(f"   {len(conflicts)} issues need to be resolved")
    print()

    commands = generate_fix_commands(conflicts)
    script_path = "fix_conflicts.bat"

    print("📝 Creating fix script...")

    try:
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(commands))
        print(f"✅ Created: {script_path}")

        print()
        print("🔧 RECOMMENDED FIX:"        print("1. Close your application")
        print("2. Run: fix_conflicts.bat")
        print("3. Restart your application")
        print()
        print("Or run these commands manually:"
        for cmd in commands[3:]:  # Skip the REM comments
            if cmd and not cmd.startswith('REM') and not cmd.startswith('echo'):
                print(f"   - {cmd}")

    except Exception as e:
        print(f"❌ Error creating fix script: {e}")
        print()
        print("🔧 Manual fix commands:")
        for cmd in commands:
            if not cmd.startswith('REM') and not cmd.startswith('echo'):
                print(f"   {cmd}")

    return False

def main():
    """Main function"""
    print("🚀 WhatsApp Voice Agent - Dependency Checker")
    print("=" * 60)
    print()

    # Check for conflicts
    conflicts = check_conflicts()

    # Report summary
    print()
    if conflicts:
        print("❌ ISSUES FOUND:"        for conflict in conflicts:
            print(f"   • {conflict['package']}: {conflict['reason']}")
        print()
        create_fix_script(conflicts)
    else:
        print("✅ Environment looks good!"        print("   All dependencies appear to be correctly configured.")
        print()
        print("🎉 You should be able to use the TTS VoxClone feature.")
        print("   Start the application and check the '🔊 CoquiTTS VoxClone' tab.")

    print()
    print("📚 TROUBLESHOOTING:")
    if conflicts:
        print("• Always install packages in this order: tokenizers → transformers → TTS")
        print("• Use the exact versions specified to avoid conflicts")
        print("• If still having issues, uninstall and reinstall Python environment")
    else:
        print("• If TTS still doesn't work, check logs for detailed error messages")
        print("• Verify your reference audio files are clean WAV files")

    print()
    print("=" * 60)

if __name__ == "__main__":
    main()