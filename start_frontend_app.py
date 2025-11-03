#!/usr/bin/env python3
"""
Flutter Frontend Application Launcher
"""

import os
import sys
import subprocess
import time

def main():
    print("\n" + "="*50)
    print("  Flutter Frontend Application Launcher")
    print("="*50 + "\n")
    
    # Set Flutter path
    flutter_bin = r"D:\flutter\flutter\bin"
    flutter_exe = os.path.join(flutter_bin, "flutter.bat")
    
    # Check if Flutter exists
    if not os.path.exists(flutter_exe):
        print("ERROR: Flutter not found at", flutter_exe)
        return 1
    
    print("✓ Flutter found at:", flutter_exe)
    print()
    
    # Change to frontend directory
    frontend_dir = r"d:\JZ_Project3\frontend"
    os.chdir(frontend_dir)
    print("✓ Changed to frontend directory:", frontend_dir)
    print()
    
    # Step 1: Get dependencies
    print("Step 1: Getting dependencies...")
    print("-" * 50)
    result = subprocess.run([flutter_exe, "pub", "get"], cwd=frontend_dir)
    if result.returncode != 0:
        print("ERROR: Failed to get dependencies")
        return 1
    print()
    
    # Step 2: Check devices
    print("Step 2: Checking for devices...")
    print("-" * 50)
    result = subprocess.run([flutter_exe, "devices"], cwd=frontend_dir)
    print()
    
    # Step 3: Run application
    print("Step 3: Running application...")
    print("-" * 50)
    print("Tips:")
    print("  - Press 'r' to hot reload")
    print("  - Press 'R' to restart")
    print("  - Press 'q' to quit")
    print()
    
    result = subprocess.run([flutter_exe, "run"], cwd=frontend_dir)
    
    return result.returncode

if __name__ == "__main__":
    sys.exit(main())

