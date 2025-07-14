from flask import Flask, render_template, request, send_file
import yt_dlp
import os
from pathlib import Path
from moviepy.editor import VideoFileClip
from loguru import logger

# Configuration de la journalisation
logger.add("logs/youtube_downloader.log", rotation="500 MB", retention="7 days")

app = Flask(__name__)

# Configuration du dossier de sortie
OUTPUT_DIR = Path('output')
OUTPUT_DIR.mkdir(exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    try:
        url = request.form.get('url')
        download_format = request.form.get('format')
        
        if not url:
            logger.error("URL YouTube non spécifiée")
            return render_template('index.html', message="URL YouTube requise", success=False)
        
        logger.info(f"Début du téléchargement pour l'URL: {url}")
        logger.info(f"Format sélectionné: {'vidéo' if download_format == 'video' else 'audio'}")
        
        # Configuration de yt-dlp
        ydl_opts = {
            'outtmpl': str(OUTPUT_DIR / '%(title)s.%(ext)s'),
            'format': 'best',  # Toujours télécharger la meilleure qualité vidéo
            'preferredquality': '192',
            'postprocessors': [],
            'progress_hooks': [lambda d: logger.info(f"Progression: {d.get('status', 'inconnu')}")]
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            output_path = ydl.prepare_filename(info)
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            output_path = ydl.prepare_filename(info)
            
            # Si c'est un fichier audio, extraire l'audio avec MoviePy
            if download_format == 'audio':
                try:
                    logger.info("Début de l'extraction de l'audio")
                    # Extraire l'audio et le sauvegarder en MP3
                    clip = VideoFileClip(output_path)
                    mp3_path = output_path.rsplit('.', 1)[0] + '.mp3'
                    
                    # Extraire l'audio avec des paramètres spécifiques
                    audio = clip.audio
                    audio.write_audiofile(mp3_path, fps=44100, bitrate='192k')
                    audio.close()
                    clip.close()
                    
                    # Supprimer le fichier vidéo original
                    os.remove(output_path)
                    output_path = mp3_path
                    logger.success(f"Extraction audio terminée avec succès: {mp3_path}")
                except Exception as e:
                    logger.error(f"Erreur lors de l'extraction de l'audio: {str(e)}")
                    return render_template('index.html', 
                                        message=f"Erreur lors de l'extraction de l'audio : {str(e)}", 
                                        success=False)
            
            logger.success(f"Téléchargement terminé avec succès: {output_path}")
            return render_template('index.html', 
                                message=f"Téléchargement terminé ! Le fichier est disponible ici : {output_path}", 
                                success=True)
    except Exception as e:
        logger.error(f"Erreur lors du téléchargement: {str(e)}")
        return render_template('index.html', message=f"Erreur lors du téléchargement : {str(e)}", success=False)

if __name__ == '__main__':
    app.run(debug=True)