#!/usr/bin/env python3
"""
Test script for RSS generator
Checks if everything is working correctly
"""

import os
import sys

def check_requirements():
    """Check if all requirements are met"""
    print("🔍 Checking requirements...\n")
    
    checks = {
        "✓ Python 3.x": sys.version_info >= (3, 6),
        "✓ generate_rss.py exists": os.path.exists('generate_rss.py'),
        "✓ requirements.txt exists": os.path.exists('requirements.txt'),
    }
    
    all_ok = True
    for check, passed in checks.items():
        status = "✅" if passed else "❌"
        print(f"{status} {check}")
        if not passed:
            all_ok = False
    
    print()
    
    # Check environment variable
    api_key = os.environ.get('GEMINI_API_KEY')
    if api_key:
        print(f"✅ GEMINI_API_KEY is set ({api_key[:10]}...)")
    else:
        print("⚠️  GEMINI_API_KEY not set (needed for actual generation)")
        print("   For testing, you can set it: export GEMINI_API_KEY='your-key'")
    
    print()
    
    # Check dependencies
    try:
        import google.generativeai
        print("✅ google-generativeai package installed")
    except ImportError:
        print("❌ google-generativeai not installed")
        print("   Run: pip install google-generativeai --break-system-packages")
        all_ok = False
    
    print()
    
    if all_ok:
        print("🎉 All checks passed! Ready to generate RSS feed.")
        print("\nTo test generation:")
        print("  1. Set GEMINI_API_KEY environment variable")
        print("  2. Run: python generate_rss.py")
    else:
        print("❌ Some checks failed. Please fix the issues above.")
    
    return all_ok

def check_rss_file():
    """Check if RSS file exists and is valid"""
    print("\n📄 Checking RSS file...\n")
    
    if not os.path.exists('feed.xml'):
        print("ℹ️  feed.xml not found (will be created on first run)")
        return False
    
    try:
        import xml.etree.ElementTree as ET
        tree = ET.parse('feed.xml')
        root = tree.getroot()
        
        if root.tag == 'rss':
            channel = root.find('channel')
            items = channel.findall('item') if channel else []
            print(f"✅ Valid RSS feed with {len(items)} items")
            
            if items:
                latest = items[0]
                title = latest.find('title')
                print(f"   Latest: {title.text if title is not None else 'N/A'}")
            
            return True
        else:
            print("❌ Invalid RSS format")
            return False
    
    except Exception as e:
        print(f"❌ Error reading RSS file: {e}")
        return False

def main():
    """Main test function"""
    print("=" * 60)
    print("Daily English Learning RSS - System Check")
    print("=" * 60)
    print()
    
    requirements_ok = check_requirements()
    rss_ok = check_rss_file()
    
    print("\n" + "=" * 60)
    
    if requirements_ok:
        print("✨ System is ready!")
        print("\nNext steps:")
        print("1. Push to GitHub")
        print("2. Set GEMINI_API_KEY in GitHub Secrets")
        print("3. Enable GitHub Pages")
        print("4. Run GitHub Actions workflow")
    else:
        print("⚠️  Please fix the issues above first")
    
    print("=" * 60)

if __name__ == '__main__':
    main()
