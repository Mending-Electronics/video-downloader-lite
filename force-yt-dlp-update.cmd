@echo off
:: Activate virtual environment
call .venv\Scripts\activate

:: Uninstall existing yt-dlp
pip uninstall -y yt-dlp

:: Install latest yt-dlp
pip install yt-dlp

echo yt-dlp has been updated to the latest version
pause
