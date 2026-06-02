#!/usr/bin/env python3


# ffmpeg -version


"""
Video Downloader for YouTube and Facebook
Downloads videos in BEST available HD quality (1080p, 1440p, 2K, 4K)
"""

import yt_dlp
import os
import sys
from pathlib import Path


def download_video(url, output_path="downloads", use_cookies=False):
    """
    Download video from YouTube or Facebook in BEST HD quality
    
    Args:
        url (str): Video URL from YouTube or Facebook
        output_path (str): Directory to save videos
        use_cookies (bool): Use browser cookies file if available
    """
    
    # Create output directory if it doesn't exist
    Path(output_path).mkdir(parents=True, exist_ok=True)
    
    # Configure yt-dlp options for BEST quality (4K/2K/1440p/1080p)
    # Try different formats - some don't require FFmpeg
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',  # Fallback formats
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'quiet': False,
        'no_warnings': False,
    }
    
    # Use cookies file if it exists
    cookies_file = os.path.join(output_path, 'cookies.txt')
    if use_cookies and os.path.exists(cookies_file):
        ydl_opts['cookiefile'] = cookies_file
        print(f"🔐 Using cookies from: {cookies_file}")
    
    try:
        print(f"🎥 Downloading video from: {url}")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            print(f"✅ Downloaded successfully: {filename}")
            return True
    
    except Exception as e:
        error_msg = str(e)
        if "Sign in to confirm" in error_msg or "bot" in error_msg.lower():
            print(f"⚠️  YouTube Authentication Required")
            print("   This video needs you to be logged in.")
            print("\n💡 Quick fixes:")
            print("   1. Open the URL in Chrome first to verify you can watch it")
            print("   2. Try a different (public) video")
            print("   3. Or download audio only: ")
            print("      yt-dlp -f bestaudio --extract-audio <url>")
        elif "nsig" in error_msg or "js player" in error_msg.lower():
            print(f"⚠️  YouTube Protection Active")
            print("   Update yt-dlp: pip install --upgrade yt-dlp")
        else:
            print(f"❌ Error: {error_msg[:100]}")
        return False


# ============================================
# HARDCODED URLs - Modify these to download
# ============================================
OUTPUT_FOLDER = "downloads"  # Change this to your desired folder


def main(urls=None, output_folder=None, use_cookies=False):
    """
    Main function to download videos
    
    Args:
        urls (list): List of video URLs to download
        output_folder (str): Output directory for videos
        use_cookies (bool): Use cookies file if available (default: False)
    """
    
    if output_folder is None:
        output_folder = OUTPUT_FOLDER
    
    # Get URLs from command-line arguments if not provided
    if urls is None:
        urls = sys.argv[1:]
    
    print("=" * 60)
    print("  🎬 Video Downloader (YouTube & Facebook) - BEST HD Quality")
    print("=" * 60)
    print()
    
    if not urls:
        print("❌ No URLs provided!")
        print("\n📖 Usage:")
        print(f"   python {sys.argv[0]} <url1> <url2> ...")
        print("\n💡 Examples:")
        print("   python video_downloader.py https://www.youtube.com/watch?v=...")
        print("   python video_downloader.py https://youtu.be/... https://facebook.com/...")
        return
    
    print(f"📥 Found {len(urls)} URL(s) to download")
    print(f"🎬 Downloading in BEST available quality (4K/2K/1440p/1080p)\n")
    
    for index, url in enumerate(urls, 1):
        print(f"[{index}/{len(urls)}] Processing: {url}")
        download_video(url, output_folder, use_cookies=use_cookies)
        print()


if __name__ == "__main__":
    str = """
https://www.youtube.com/watch?v=AUH2nnk7MiU
    """
    urls = str.split("\n")  # Split by newline
    urls = [url.strip() for url in urls if url.strip()]  # Remove empty lines and whitespace
    main(urls, output_folder=r"C:\Users\ADMIN\Downloads")
