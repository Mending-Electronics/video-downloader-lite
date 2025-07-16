from flask import Flask, render_template, request, send_file, Response, jsonify
import yt_dlp
import os
import json
from pathlib import Path
import threading
import time
import re

app = Flask(__name__)

# Ensure the downloads directory exists
DOWNLOAD_DIR = Path("downloads")
DOWNLOAD_DIR.mkdir(exist_ok=True)

class DownloadProgress:
    def __init__(self):
        self.progress = {}
        self.lock = threading.Lock()

    def update(self, url, data):
        with self.lock:
            if url not in self.progress:
                self.progress[url] = []
            self.progress[url].append(data)

    def get_progress(self, url):
        with self.lock:
            return self.progress.get(url, [])

progress_tracker = DownloadProgress()

class ProgressHook:
    def __init__(self, url):
        self.url = url
        self.callback = None
        self.last_update = time.time()

    def hook(self, d):
        if d['status'] == 'downloading':
            status = d.get('_percent_str', '0%').strip()
            speed = d.get('_speed_str', '0 B/s')
            eta = d.get('_eta_str', '--:--')
            
            # Clean terminal output by removing ANSI escape codes
            terminal_line = f"[download] {status} at {speed} ETA {eta}"
            terminal_line = re.sub(r'\x1b\[([0-9]{1,2}(;[0-9]{1,2})?)?[m|K]', '', terminal_line)
            
            # Clean percentage value
            clean_percent = re.sub(r'\x1b\[([0-9]{1,2}(;[0-9]{1,2})?)?[m|K]', '', status)
            clean_percent = clean_percent.replace('%', '').strip()
            
            progress_data = {
                'type': 'progress',
                'data': {
                    'percent': status,
                    'speed': speed,
                    'eta': eta,
                    'terminal_line': terminal_line,
                    'progress_percent': float(clean_percent) if clean_percent else 0
                }
            }
            
            if self.callback:
                self.callback(progress_data)
            
            # Update progress tracker
            progress_tracker.update(self.url, progress_data)
            
            # Limit updates to once per second
            current_time = time.time()
            if current_time - self.last_update < 1:
                return
            self.last_update = current_time

        elif d['status'] == 'finished':
            progress_tracker.update(self.url, {
                'type': 'complete',
                'data': {
                    'message': 'Download completed'
                }
            })
        
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-formats')
def get_formats():
    url = request.args.get('url')
    if not url:
        return jsonify({'status': 'error', 'message': 'No URL provided'}), 400

    try:
        ydl_opts = {
            'extract_flat': True,
            'quiet': True
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            formats = []
            for fmt in info.get('formats', []):
                if fmt.get('format_id'):
                    formats.append({
                        'format_id': fmt['format_id'],
                        'format': fmt.get('format_note', 'Unknown'),
                        'resolution': fmt.get('resolution', 'Unknown'),
                        'ext': fmt.get('ext', 'Unknown'),
                        'filesize': fmt.get('filesize')
                    })
            
            return jsonify({
                'status': 'success',
                'title': info.get('title', 'Unknown'),
                'formats': formats,
                'thumbnail': info.get('thumbnail', '')
            })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/download-progress')
def download_progress():
    url = request.args.get('url')
    if not url:
        return jsonify({'status': 'error', 'message': 'No URL provided'}), 400

    progress = progress_tracker.get_progress(url)
    if progress:
        return jsonify({
            'status': 'success',
            'progress': progress[-1]  # Return the latest progress update
        })
    else:
        return jsonify({'status': 'not_found'}), 404

@app.route('/download-format')
def download_format():
    url = request.args.get('url')
    format_id = request.args.get('format_id')
    if not url or not format_id:
        return jsonify({'status': 'error', 'message': 'URL or format ID not provided'}), 400

    class YTDLLogger:
        def __init__(self, url):
            self.url = url

        def debug(self, msg):
            if msg.startswith('[debug]'):
                pass
            else:
                print(msg)

        def info(self, msg):
            print(msg)

        def warning(self, msg):
            print(f"WARNING: {msg}")

        def error(self, msg):
            print(f"ERROR: {msg}")

    def generate():
        progress = ProgressHook(url)
        
        def progress_callback(data):
            return f"data: {json.dumps(data)}\n\n"
        
        progress.callback = progress_callback

        # For MP3, we'll download the best video format first
        if format_id == 'mp3':
            ydl_opts = {
                'format': 'best',  # Get the best quality video
                'outtmpl': str(DOWNLOAD_DIR / '%(title)s.%(ext)s'),
                'progress_hooks': [progress.hook],
                'quiet': False,
                'no_warnings': False,
                'noprogress': True,
                'logger': YTDLLogger(url)
            }
        else:
            ydl_opts = {
                'format': format_id,
                'outtmpl': str(DOWNLOAD_DIR / '%(title)s_%(format_id)s.%(ext)s'),
                'progress_hooks': [progress.hook],
                'quiet': False,
                'no_warnings': False,
                'noprogress': True,
                'logger': YTDLLogger(url)
            }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                
                # If the format is 'mp3', convert the downloaded video to MP3
                if format_id == 'mp3':
                    # Send download completed message
                    yield f"data: {json.dumps({
                        'type': 'log',
                        'message': 'Download completed',
                        'terminal_line': '✅ Download Completed',
                        'status': 'Starting MP3 conversion...'
                    })}\n\n"
                    
                    # Small delay to ensure message is sent
                    time.sleep(0.1)
                    
                    # Send MP3 conversion starting message (SSE)
                    yield f"data: {json.dumps({
                        'type': 'mp3_conversion_start',
                        'message': 'Starting MP3 conversion',
                        'terminal_line': '🔄 Starting MP3 Conversion...',
                        'status': 'Converting to MP3...'
                    })}\n\n"
                    
                    # We don't update the progress tracker here to avoid duplicate messages
                    # The SSE message is already sent above and will be handled by the frontend
                    
                    try:
                        from moviepy.editor import VideoFileClip
                        
                        # Create the MP3 filename
                        mp3_filename = os.path.splitext(filename)[0] + '.mp3'
                        
                        # Notify client that we're starting the conversion
                        yield f"data: {json.dumps({
                            'type': 'log',
                            'message': 'Converting to MP3...',
                            'terminal_line': '📊 Converting video to MP3 format...',
                            'status': 'Converting to MP3...'
                        })}\n\n"
                        
                        # Convert video to MP3
                        clip = VideoFileClip(filename)
                        audio = clip.audio
                        
                        # Send progress update
                        yield f"data: {json.dumps({
                            'type': 'log',
                            'message': 'Extracting audio...',
                            'terminal_line': '🔊 Extracting audio from video...',
                            'status': 'Extracting audio...'
                        })}\n\n"
                        
                        # Write audio file with progress updates
                        audio.write_audiofile(
                            mp3_filename,
                            fps=44100,
                            bitrate='192k',
                            logger=None,  # Disable moviepy's progress output
                            verbose=False
                        )
                        
                        # Clean up
                        audio.close()
                        clip.close()
                        
                        # Remove the original video file
                        os.remove(filename)
                        
                        # Update the filename to point to the MP3
                        filename = mp3_filename
                        
                        # Send MP3 conversion complete message (SSE)
                        yield f"data: {json.dumps({
                            'type': 'mp3_conversion_complete',
                            'message': 'MP3 conversion completed',
                            'terminal_line': '✅ MP3 conversion completed!',
                            'status': 'MP3 conversion completed!'
                        })}\n\n"
                        
                        # We don't update the progress tracker here to avoid duplicate messages
                        # The SSE message is already sent above and will be handled by the frontend
                        
                    except Exception as e:
                        error_msg = f"Error converting to MP3: {str(e)}"
                        yield f"data: {json.dumps({
                            'type': 'error',
                            'message': error_msg,
                            'terminal_line': error_msg
                        })}\n\n"
                        # Clean up any partially created files
                        if os.path.exists(filename):
                            try:
                                os.remove(filename)
                            except:
                                pass
                        return
                
                yield f"data: {json.dumps({
                    'type': 'complete',
                    'filename': os.path.basename(filename)
                })}\n\n"
                
        except Exception as e:
            error_msg = str(e)
            print(f"Error in download: {error_msg}")
            yield f"data: {json.dumps({
                'type': 'error',
                'message': error_msg
            })}\n\n"
        finally:
            yield "data: [DONE]\n\n"
    
    return Response(
        generate(),
        mimetype='text/event-stream'
    )

@app.route('/download-stream')
def download_stream():
    url = request.args.get('url')
    if not url:
        return jsonify({'status': 'error', 'message': 'No URL provided'}), 400
    
    class YTDLLogger:
        def debug(self, msg):
            if msg.startswith('[debug]'):  # Skip debug messages
                pass
            else:
                print(msg)  # Print other messages to console

        def info(self, msg):
            print(msg)

        def warning(self, msg):
            print(f"WARNING: {msg}")

        def error(self, msg):
            print(f"ERROR: {msg}")

    def generate():
        progress = ProgressHook(url)
        
        def progress_callback(data):
            return f"data: {json.dumps(data)}\n\n"
        
        progress.callback = progress_callback

        ydl_opts = {
            'format': 'best',
            'outtmpl': str(DOWNLOAD_DIR / '%(title)s.%(ext)s'),
            'progress_hooks': [progress.hook],
            'quiet': False,
            'no_warnings': False,
            'noprogress': True,  # Disable yt-dlp's progress bar
            'logger': YTDLLogger()  # Use our custom logger class
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                
                # Send completion message
                yield f"data: {json.dumps({
                    'type': 'complete',
                    'filename': os.path.basename(filename)
                })}\n\n"
                
        except Exception as e:
            error_msg = str(e)
            print(f"Error in download: {error_msg}")  # Log the error
            yield f"data: {json.dumps({
                'type': 'error',
                'message': error_msg
            })}\n\n"
        finally:
            yield "data: [DONE]\n\n"
    
    return Response(
        generate(),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'X-Accel-Buffering': 'no'
        }
    )

@app.route('/download/<filename>')
def download_file(filename):
    try:
        return send_file(
            DOWNLOAD_DIR / filename,
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f"Download failed: {str(e)}"
        }), 404

if __name__ == '__main__':
    app.run(debug=True, threaded=True)