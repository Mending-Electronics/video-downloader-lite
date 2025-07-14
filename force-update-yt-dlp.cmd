@echo off

:: Activation de l'environnement virtuel
call .venv\Scripts\activate

echo Checking current yt-dlp version...
python -m yt_dlp --version

echo Uninstalling current yt-dlp...
pip uninstall -y yt-dlp

echo Installing latest yt-dlp version from PyPI (including dev0 and pre-releases)...
pip install --upgrade --pre yt-dlp

echo Installed yt-dlp version:
python -m yt_dlp --version

echo Update complete!
pause
