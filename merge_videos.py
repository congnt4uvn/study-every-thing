"""
Video Merger Script
Merges all video files in a folder into a single video file.
pip install moviepy
"""

import os
from pathlib import Path

from moviepy import VideoFileClip, concatenate_videoclips

def merge_videos(folder_path, output_file="merged_video.mp4", video_extensions=None):
    """
    Merge all video files in a folder.
    
    Args:
        folder_path: Path to folder containing video files
        output_file: Name of output merged video file
        video_extensions: List of video extensions to look for (default: common formats)
    
    Returns:
        Path to merged video file or None if error
    """
    
    if video_extensions is None:
        video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm']
    
    folder_path = Path(folder_path)
    
    # Check if folder exists
    if not folder_path.exists():
        print(f"Error: Folder '{folder_path}' does not exist!")
        return None
    
    # Get all video files, sorted by name
    video_files = sorted([
        f for f in folder_path.iterdir() 
        if f.is_file() and f.suffix.lower() in video_extensions
    ])
    
    if not video_files:
        print(f"No video files found in '{folder_path}'")
        return None
    
    print(f"Found {len(video_files)} video files:")
    for i, video in enumerate(video_files, 1):
        print(f"  {i}. {video.name}")
    
    # Load all video clips
    print("\nLoading video clips...")
    clips = []
    for i, video_file in enumerate(video_files, 1):
        try:
            print(f"  Loading: {video_file.name}", end=" ... ")
            clip = VideoFileClip(str(video_file))
            clips.append(clip)
            print(f"OK ({clip.duration:.1f}s)")
        except Exception as e:
            print(f"ERROR: {str(e)}")
    
    if not clips:
        print("Error: Could not load any video clips!")
        return None
    
    # Merge clips
    print(f"\nMerging {len(clips)} videos...")
    try:
        final_clip = concatenate_videoclips(clips)
        output_path = folder_path / output_file
        
        print(f"Writing output: {output_file}")
        final_clip.write_videofile(
            str(output_path),
            logger=None,  # Suppress verbose output
            threads=4,    # Use multiple threads for faster processing  
        )
        
        # Close clips
        final_clip.close()
        for clip in clips:
            clip.close()
        
        print(f"\n✓ Successfully merged! Output: {output_path}")
        print(f"  Total duration: {final_clip.duration:.1f} seconds ({final_clip.duration/60:.1f} minutes)")
        
        return str(output_path)
    
    except Exception as e:
        print(f"Error during merging: {str(e)}")
        return None


def main():
    """Main entry point"""
    import sys
    
    if len(sys.argv) > 1:
        folder_path = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else "merged_video.mp4"
    else:
        # Interactive mode
        print("=" * 50)
        print("VIDEO MERGER SCRIPT")
        print("=" * 50)
        folder_path = r"C:\Users\ADMIN\Downloads\New folder"
        output_file = r"C:\Users\ADMIN\Downloads\New folder\merged_video.mp4"
    
    merge_videos(folder_path, output_file)


if __name__ == "__main__":
    main()
