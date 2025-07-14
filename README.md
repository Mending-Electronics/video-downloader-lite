# YouTube Downloader

A web application for downloading YouTube videos.

## Updating yt-dlp

The application uses yt-dlp for downloading YouTube content. To ensure you have the latest version of yt-dlp, use the `force-yt-dlp-update.cmd` script:

1. Open a terminal in the project directory
2. Run: `force-yt-dlp-update.cmd`

This script will:
- Activate the virtual environment
- Display the current yt-dlp version
- Uninstall the current version
- Install the latest version
- Display the new version number

## Requirements

- Python 3.8 or higher
- Virtual environment (automatically created by the script)