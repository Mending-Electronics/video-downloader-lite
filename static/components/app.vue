// Création de l'application Vue
const { createApp, ref, onMounted, nextTick } = Vue;

const app = createApp({
    delimiters: ['[[', ']]'],
    setup() {
        // Réactifs
        const url = ref('');
        const isUrlValid = ref(false);
        const isLoading = ref(false);
        const downloadPlaylist = ref(false);
        const showFormatCard = ref(false);
        const showStatusCard = ref(false);
        const videoInfo = ref({
            title: 'Unknown',
            thumbnail: '',
            formats: []
        });
        const downloadProgress = ref({
            percent: 0,
            speed: '0 B/s',
            eta: '--:--',
            status: 'Preparing download...',
            terminal: []
        });
        const toast = ref({
            show: false,
            title: '',
            message: '',
            type: 'info'
        });

        // Références aux éléments DOM
        let toastInstance = null;

        // Initialisation
        onMounted(() => {
            // Initialiser le toast Bootstrap
            const toastEl = document.getElementById('toast');
            toastInstance = new bootstrap.Toast(toastEl);

            // Gestion du défilement fluide
            document.querySelectorAll('a[href^="#"]').forEach(anchor => {
                anchor.addEventListener('click', function(e) {
                    e.preventDefault();
                    const target = document.querySelector(this.getAttribute('href'));
                    if (target) {
                        target.scrollIntoView({ behavior: 'smooth' });
                    }
                });
            });
        });

        // Propriétés calculées
        const urlGroupClasses = Vue.computed(() => ({
            'has-validation': true,
            'was-validated': url.value.length > 0,
            'is-valid': isUrlValid.value && url.value.length > 0,
            'is-invalid': !isUrlValid.value && url.value.length > 0
        }));

        // Méthodes
        const getFormatType = (ext, quality) => {
            // Si le quality est déjà défini, on le retourne
            if (quality !== 'N/A') return quality;
            
            // Listes des extensions pour chaque type
            const videoExtensions = ['mp4', 'webm', 'avi', 'wmv'];
            const audioExtensions = ['mp3', 'weba', 'wma'];
            
            // Normaliser l'extension (en minuscules sans point)
            const normalizedExt = ext.toLowerCase().replace('.', '');
            
            // Déterminer le type en fonction de l'extension
            if (videoExtensions.includes(normalizedExt)) {
                return 'Video';
            } else if (audioExtensions.includes(normalizedExt)) {
                return 'Audio';
            }
            return 'N/A';
        };

        const validateUrl = (url) => {
            const urlRegex = /^(http|https):\/\//;
            return urlRegex.test(url);
        };

        const updateUrlValidation = () => {
            isUrlValid.value = validateUrl(url.value);
        };

        const showToast = (title, message, type = 'info') => {
            toast.value = { show: true, title, message, type };
            nextTick(() => {
                toastInstance.show();
            });
        };

        const addTerminalLine = (message) => {
            downloadProgress.value.terminal.push({
                id: Date.now(),
                message,
                type: message.toLowerCase().includes('[error]') ? 'error' : 
                      message.toLowerCase().includes('[warning]') ? 'warning' :
                      message.toLowerCase().includes('[debug]') ? 'debug' : 'info'
            });
            // Faire défiler vers le bas
            nextTick(() => {
                const terminal = document.getElementById('terminalOutput');
                if (terminal) {
                    terminal.scrollTop = terminal.scrollHeight;
                }
            });
        };

        const formatFileSize = (bytes) => {
            if (bytes === null || bytes === undefined) return 'N/A';
            if (bytes === 0) return '0 Bytes';
            const k = 1024;
            const sizes = ['Bytes', 'KB', 'MB', 'GB'];
            const i = Math.floor(Math.log(bytes) / Math.log(k));
            return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
        };

        const cleanTerminalOutput = (text) => {
            if (!text) return '';
            // Supprimer les codes ANSI
            return text.replace(/\x1b\[[0-9;]*[mK]/g, '')
                      .replace(/[^\x20-\x7E\n]/g, '')
                      .trim();
        };

        // Gestion du formulaire
        const cleanYoutubeUrl = (url) => {
            if (!url.includes('youtube.com') && !url.includes('youtu.be')) return url;
            
            try {
                const urlObj = new URL(url);
                if (!downloadPlaylist.value && urlObj.searchParams.has('list')) {
                    // Remove list parameter and everything after it
                    const videoId = urlObj.searchParams.get('v');
                    if (videoId) {
                        return `${urlObj.origin}${urlObj.pathname}?v=${videoId}`;
                    }
                }
                return url;
            } catch (e) {
                console.error('Error cleaning YouTube URL:', e);
                return url;
            }
        };

        const handleSubmit = async (e) => {
            e.preventDefault();
            if (!isUrlValid.value) {
                showToast('Error', 'Please enter a valid URL', 'danger');
                return;
            }
            
            const cleanedUrl = cleanYoutubeUrl(url.value);

            isLoading.value = true;
            showFormatCard.value = false;
            showStatusCard.value = false;
            videoInfo.value.formats = [];

            try {
                const response = await axios.get(`/get-formats?url=${encodeURIComponent(cleanedUrl)}`);
                if (response.data.status === 'success') {
                    videoInfo.value = {
                        title: response.data.title || 'Unknown',
                        thumbnail: response.data.thumbnail || '',
                        formats: (response.data.formats || [])
                            .filter(fmt => !fmt.format_id.startsWith('hls') && !fmt.format_id.startsWith('sb'))
                            .map(fmt => ({
                                ...fmt,
                                format_id: fmt.format_id === '0' ? 'mp4' : fmt.format_id,
                                quality: fmt.quality === 'Unknown' ? 'Video' : fmt.quality,
                                resolution: !fmt.resolution || fmt.resolution === 'Unknown' ? 'Best' : fmt.resolution
                            }))
                    };
                    
                    // Ajouter l'option MP3 en premier
                    videoInfo.value.formats.unshift({
                        format_id: 'mp3',
                        ext: 'mp3',
                        quality: 'Audio',
                        resolution: 'audio only',
                        filesize: null
                    });

                    showFormatCard.value = true;
                    
                    // Faire défiler vers la carte des formats
                    nextTick(() => {
                        const formatCard = document.getElementById('formatCard');
                        if (formatCard) {
                            formatCard.scrollIntoView({ behavior: 'smooth' });
                        }
                    });
                } else {
                    throw new Error(response.data.message || 'Failed to fetch formats');
                }
            } catch (error) {
                console.error('Error fetching formats:', error);
                showToast('Error', 'Failed to fetch video formats', 'danger');
            } finally {
                isLoading.value = false;
            }
        };

        // Télécharger un format spécifique
        const downloadFormat = async (formatId) => {
            try {
                showStatusCard.value = true;
                // Nettoyer l'URL si nécessaire
                const cleanedUrl = cleanYoutubeUrl(url.value);
                
                // Réinitialiser la progression
                downloadProgress.value = {
                    percent: 0,
                    speed: '0 B/s',
                    eta: '--:--',
                    status: 'Preparing download...',
                    terminal: []
                };

                // Faire défiler vers la carte de statut
                await nextTick();
                const statusCard = document.getElementById('statusCard');
                if (statusCard) {
                    statusCard.scrollIntoView({ behavior: 'smooth' });
                }

                // Ajouter la première ligne au terminal
                addTerminalLine('Starting download...');

                // Démarrer la connexion SSE pour le téléchargement
                const eventSource = new EventSource(`/download-format?url=${encodeURIComponent(cleanedUrl)}&format_id=${formatId}`);

                // Démarrer le polling pour la progression
                let progressInterval = setInterval(() => {
                    fetch(`/download-progress?url=${encodeURIComponent(cleanedUrl)}`)
                        .then(response => response.json())
                        .then(data => {

                            // console.log('Progress data:', data);

                            if (data.status === 'success') {
                                const progress = data.progress;
                                
                                // Gestion des différents types de messages
                                if (progress.type === 'mp3_conversion_start') {
                                    // Début de la conversion MP3
                                    downloadProgress.value.status = 'Converting to MP3...';
                                    addTerminalLine('🔄 Starting MP3 conversion...');
                                    return;
                                }
                                
                                if (progress.type === 'mp3_conversion_complete') {
                                    // Fin de la conversion MP3
                                    downloadProgress.value.status = 'MP3 conversion completed!';
                                    addTerminalLine('✅ MP3 conversion completed!');
                                    return;
                                }
                                
                                if (progress.type === 'progress') {
                                    const percentValue = progress.data.progress_percent || 0;
                                    
                                    // Mettre à jour la progression
                                    downloadProgress.value = {
                                        ...downloadProgress.value,
                                        percent: Math.min(100, Math.max(0, percentValue)),
                                        speed: cleanTerminalOutput(progress.data.speed || '0 B/s'),
                                        eta: cleanTerminalOutput(progress.data.eta || '--:--'),
                                        status: cleanTerminalOutput(progress.data.terminal_line || 'Downloading...')
                                    };

                                    // Mettre à jour la barre de progression
                                    nextTick(() => {
                                        const progressBar = document.querySelector('.progress-bar');
                                        if (progressBar) {
                                            progressBar.style.width = `${percentValue}%`;
                                            progressBar.setAttribute('aria-valuenow', percentValue);
                                            
                                            // Mettre à jour le texte du pourcentage
                                            const percentText = progressBar.querySelector('.progress-percent');
                                            if (percentText) {
                                                percentText.textContent = `${percentValue.toFixed(1)}%`;
                                            }
                                            
                                            // Mettre à jour les autres éléments
                                            const speedEl = document.getElementById('downloadSpeed');
                                            const etaEl = document.getElementById('etaText');
                                            const statusEl = document.getElementById('statusText');
                                            
                                            if (speedEl) speedEl.textContent = `Speed: ${downloadProgress.value.speed}`;
                                            if (etaEl) etaEl.textContent = `ETA: ${downloadProgress.value.eta}`;
                                            if (statusEl) statusEl.textContent = downloadProgress.value.status;
                                        }
                                    });
                                }
                            }
                        })
                        .catch(error => {
                            console.error('Error fetching progress:', error);
                            addTerminalLine(`Error fetching progress: ${error.message}`);
                        });
                }, 500); // Polling toutes les secondes

                eventSource.onmessage = (event) => {
                    const data = JSON.parse(event.data);
                    
                    // Vérifier si c'est un message de conversion MP3
                    if (data.type === 'mp3_conversion_start') {
                        downloadProgress.value.status = 'Converting to MP3...';
                        addTerminalLine('🔄 Starting MP3 conversion...');
                        return;
                    }
                    
                    if (data.type === 'mp3_conversion_complete') {
                        downloadProgress.value.status = 'MP3 conversion completed!';
                        addTerminalLine('✅ MP3 conversion completed!');
                        return;
                    }
                    
                    if (data.type === 'complete') {
                        // Mettre à jour la progression à 100%
                        downloadProgress.value = {
                            ...downloadProgress.value,
                            percent: 100,
                            speed: '0 B/s',
                            eta: '00:00',
                            status: `Download completed 👌: ${data.filename}`
                        };

                        // Mettre à jour la barre de progression
                        nextTick(() => {
                            const progressBar = document.querySelector('.progress-bar');
                            if (progressBar) {
                                progressBar.style.width = '100%';
                                progressBar.classList.remove('bg-primary');
                                progressBar.classList.add('bg-success');
                            }
                        });

                        // Afficher le toast et ajouter au terminal
                        showToast('Success', `Download completed 👌: ${data.filename}`, 'success');
                        addTerminalLine(`Download completed 👌: ${data.filename}`);

                        // Fermer les connexions
                        eventSource.close();
                        clearInterval(progressInterval);
                    } else if (data.type === 'error') {
                        const errorMsg = cleanTerminalOutput(data.message || 'Unknown error occurred');
                        
                        // Mettre à jour la barre de progression en rouge
                        nextTick(() => {
                            const progressBar = document.querySelector('.progress-bar');
                            if (progressBar) {
                                progressBar.classList.remove('bg-primary');
                                progressBar.classList.add('bg-danger');
                            }
                        });

                        // Afficher l'erreur
                        showToast('Error', `Download failed 👎: ${errorMsg}`, 'danger');
                        addTerminalLine(`Download failed 👎: ${errorMsg}`);

                        // Fermer les connexions
                        eventSource.close();
                        clearInterval(progressInterval);
                    }
                };

                eventSource.onerror = (error) => {
                    console.error('EventSource error:', error);
                    
                    // Mettre à jour la barre de progression en rouge
                    nextTick(() => {
                        const progressBar = document.querySelector('.progress-bar');
                        if (progressBar) {
                            progressBar.classList.remove('bg-primary');
                            progressBar.classList.add('bg-danger');
                        }
                    });

                    // Afficher l'erreur
                    showToast('Error', 'Connection error occurred', 'danger');
                    addTerminalLine('Connection error occurred');

                    // Fermer les connexions
                    eventSource.close();
                    clearInterval(progressInterval);
                };

            } catch (error) {
                console.error('Download error:', error);
                addTerminalLine(`Error: ${error.message}`);
                showToast('Error', 'Download failed', 'danger');
            }
        };

        // Réinitialiser le formulaire
        const resetForm = () => {
            url.value = '';
            isUrlValid.value = false;
            showFormatCard.value = false;
            showStatusCard.value = false;
            videoInfo.value = { title: 'Unknown', thumbnail: '', formats: [] };
            downloadProgress.value = { percent: 0, speed: '0 B/s', eta: '--:--', status: '', terminal: [] };
        };

        // Retourner les données et méthodes exposées au template
        return {
            // Données réactives
            url,
            isUrlValid,
            isLoading,
            showFormatCard,
            showStatusCard,
            videoInfo,
            downloadProgress,
            toast,
            downloadPlaylist,
            
            // Méthodes
            updateUrlValidation,
            validateUrl,
            handleSubmit,
            downloadFormat,
            resetForm,
            formatFileSize,
            cleanTerminalOutput,
            getFormatType,
            
            // Classes CSS conditionnelles
            urlInputClasses: {
                'is-valid': isUrlValid.value,
                'is-invalid': url.value && !isUrlValid.value
            },
            urlGroupClasses: {
                'has-success': isUrlValid.value,
                'has-danger': url.value && !isUrlValid.value
            },
            
            // Méthodes de cycle de vie
            mounted() {
                // Initialisation du toast Bootstrap
                const toastEl = document.getElementById('toast');
                if (toastEl) {
                    this.toastInstance = new bootstrap.Toast(toastEl);
                }
                
                // Gestion du défilement fluide
                document.querySelectorAll('a[href^="#"]').forEach(anchor => {
                    anchor.addEventListener('click', (e) => {
                        e.preventDefault();
                        const target = document.querySelector(this.getAttribute('href'));
                        if (target) {
                            target.scrollIntoView({ behavior: 'smooth' });
                        }
                    });
                });
            }
        };
    },
    
    // Méthodes de cycle de vie globales
    mounted() {
        console.log('Application Vue montée');
    }
});

// Monter l'application
app.mount('#app');

// Tous les gestionnaires d'événements sont maintenant gérés par Vue.js