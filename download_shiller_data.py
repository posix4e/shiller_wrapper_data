#!/usr/bin/env python3
"""
Download Shiller data files from shillerdata.com
"""

import os
import sys
import urllib.request
import hashlib
from datetime import datetime

DATA_FILES = {
    "Fig3-1.xls": "http://www.econ.yale.edu/~shiller/data/Fig3-1.xls",
    "ie_data.xls": "http://www.econ.yale.edu/~shiller/data/ie_data.xls"
}

def download_file(url, filename):
    """Download a file from URL to filename"""
    print(f"Downloading {filename} from {url}...")
    try:
        urllib.request.urlretrieve(url, filename)
        print(f"✓ Downloaded {filename}")
        return True
    except Exception as e:
        print(f"✗ Failed to download {filename}: {e}")
        return False

def get_file_hash(filename):
    """Calculate SHA256 hash of a file"""
    if not os.path.exists(filename):
        return None
    with open(filename, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()

def main():
    """Main function to download all data files"""
    changes = []

    for filename, url in DATA_FILES.items():
        old_hash = get_file_hash(filename)

        if download_file(url, filename):
            new_hash = get_file_hash(filename)

            if old_hash != new_hash:
                if old_hash is None:
                    changes.append(f"Added {filename}")
                else:
                    changes.append(f"Updated {filename}")
                print(f"  File changed: {filename}")
            else:
                print(f"  No changes to {filename}")

    if changes:
        print(f"\n{len(changes)} file(s) changed:")
        for change in changes:
            print(f"  - {change}")
        return 0
    else:
        print("\nNo changes detected in data files")
        return 1

if __name__ == "__main__":
    sys.exit(main())