@echo off

:: Activate virtual environment
call .venv\Scripts\activate

echo Checking current yt-dlp version...
python -m yt_dlp --version

echo Uninstalling current yt-dlp...
pip uninstall -y yt-dlp

echo Installing latest yt-dlp...
pip install --upgrade yt-dlp

echo Installed yt-dlp version:
python -m yt_dlp --version

echo Update complete!

echo yt-dlp has been updated to the latest version
pause
