"""
ChromeDriver Downloader for Chrome 149.0.7827.197
This script downloads the matching ChromeDriver version for your Chrome browser.
"""


import requests
import zipfile
import os
from pathlib import Path




def download_chromedriver():
    # Chrome version 149.0.7827.197
    chrome_version = "149.0.7827.197"
    major_version = chrome_version.split('.')[0]
   
    print(f"Downloading ChromeDriver for Chrome version {chrome_version}...")
   
    # Chrome for Testing JSON endpoint (for Chrome 115+)
    base_url = "https://googlechromelabs.github.io/chrome-for-testing"
   
    try:
        # Get available versions
        print("Fetching available ChromeDriver versions...")
        response = requests.get(f"{base_url}/known-good-versions-with-downloads.json")
        response.raise_for_status()
        data = response.json()
       
        # Find the exact version or closest match
        target_version = None
        for version_info in data.get('versions', []):
            if version_info['version'] == chrome_version:
                target_version = version_info
                break
            elif version_info['version'].startswith(f"{major_version}."):
                target_version = version_info  # Keep updating to get the latest in major version
       
        if not target_version:
            print(f"Exact version {chrome_version} not found. Trying latest stable for version {major_version}...")
            # Try latest stable endpoint
            response = requests.get(f"{base_url}/last-known-good-versions-with-downloads.json")
            data = response.json()
           
            # Look for the channel with matching major version
            for channel, channel_data in data.get('channels', {}).items():
                if channel_data['version'].startswith(f"{major_version}."):
                    target_version = channel_data
                    break
       
        if not target_version:
            print(f"ERROR: Could not find ChromeDriver for Chrome {major_version}")
            print(f"\nAlternative: Download manually from:")
            print(f"https://googlechromelabs.github.io/chrome-for-testing/")
            return False
       
        # Find Windows 64-bit chromedriver download URL
        download_url = None
        downloads = target_version.get('downloads', {})
       
        for driver_info in downloads.get('chromedriver', []):
            if driver_info.get('platform') == 'win64':
                download_url = driver_info.get('url')
                break
       
        if not download_url:
            print("ERROR: Could not find Windows 64-bit ChromeDriver download URL")
            return False
       
        print(f"Found ChromeDriver version: {target_version['version']}")
        print(f"Download URL: {download_url}")
       
        # Download the zip file
        print("\nDownloading ChromeDriver...")
        zip_path = Path("chromedriver-win64.zip")
       
        response = requests.get(download_url, stream=True)
        response.raise_for_status()
       
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0
       
        with open(zip_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                downloaded += len(chunk)
                if total_size:
                    percent = (downloaded / total_size) * 100
                    print(f"\rProgress: {percent:.1f}%", end='')
       
        print("\n\nExtracting ChromeDriver...")
       
        # Extract the zip file
        extract_dir = Path("chromedriver-win64")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
       
        # Clean up zip file
        zip_path.unlink()
       
        # Find the chromedriver.exe path
        chromedriver_exe = None
        for root, dirs, files in os.walk(extract_dir):
            if 'chromedriver.exe' in files:
                chromedriver_exe = Path(root) / 'chromedriver.exe'
                break
       
        if chromedriver_exe and chromedriver_exe.exists():
            print(f"\n✓ SUCCESS!")
            print(f"ChromeDriver downloaded to: {chromedriver_exe.absolute()}")
            print(f"\nYour a.py script is already configured to use this path:")
            print(f'CHROMEDRIVER_PATH = Path("chromedriver-win64") / "chromedriver-win64" / "chromedriver.exe"')
            return True
        else:
            print(f"\n✓ ChromeDriver extracted to: {extract_dir}")
            print("Please locate chromedriver.exe in the extracted folder")
            return True
           
    except requests.exceptions.RequestException as e:
        print(f"ERROR: Network error occurred: {e}")
        print(f"\nManual download option:")
        print(f"1. Visit: https://googlechromelabs.github.io/chrome-for-testing/")
        print(f"2. Find your Chrome version {chrome_version}")
        print(f"3. Download the win64 ChromeDriver ZIP")
        print(f"4. Extract to 'chromedriver-win64' folder")
        return False
    except Exception as e:
        print(f"ERROR: {e}")
        return False




if __name__ == "__main__":
    print("=" * 60)
    print("ChromeDriver Downloader for Chrome 149.0.7827.197")
    print("=" * 60)
    print()
   
    success = download_chromedriver()
   
    if success:
        print("\n" + "=" * 60)
        print("Next steps:")
        print("1. Verify chromedriver.exe is in the correct location")
        print("2. Run your a.py script")
        print("=" * 60)
    else:
        print("\nDownload failed. Please try manual download.")
   
    input("\nPress Enter to exit...")
