#!/usr/bin/env python3
"""
Download Shiller data files from shillerdata.com
"""

import os
import sys
import urllib.request
import hashlib
from datetime import datetime
from bs4 import BeautifulSoup

def scrape_download_urls():
    """Scrape the download URLs from shillerdata.com"""
    print("Scraping download URLs from shillerdata.com...")

    with urllib.request.urlopen('https://shillerdata.com/') as response:
        html = response.read().decode('utf-8')

    soup = BeautifulSoup(html, 'html.parser')
    urls = {}

    # Find all download links
    for link in soup.find_all('a', href=True):
        href = link['href']
        # Look for .xls files in the href
        if 'ie_data.xls' in href:
            urls['ie_data.xls'] = 'https:' + href if href.startswith('//') else href
            print(f"✓ Found ie_data.xls URL")
        elif 'Fig3-1' in href and '.xls' in href:
            urls['Fig3-1.xls'] = 'https:' + href if href.startswith('//') else href
            print(f"✓ Found Fig3-1.xls URL")

    # Fail if we didn't find both URLs
    if 'ie_data.xls' not in urls:
        raise RuntimeError("Failed to scrape ie_data.xls download URL from shillerdata.com")

    if 'Fig3-1.xls' not in urls:
        raise RuntimeError("Failed to scrape Fig3-1.xls download URL from shillerdata.com")

    return urls

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

    # Scrape the latest download URLs
    data_files = scrape_download_urls()

    for filename, url in data_files.items():
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
    else:
        print("\nNo changes detected in data files")

    # Always return 0 (success) even if no changes
    return 0

if __name__ == "__main__":
    sys.exit(main())