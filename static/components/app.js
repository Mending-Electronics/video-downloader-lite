const app = Vue.createApp({
    data() {
        return {
            consoleMessages: [],
            downloadInterval: null,
            url: ''
        }
    },
    mounted() {
        // Initialize URL input validation
        const urlInput = document.getElementById('url')
        urlInput.addEventListener('input', () => {
            this.validateUrl()
        })

        // Ajouter l'écouteur d'événement au formulaire
        const form = document.querySelector('form')
        if (form) {
            form.addEventListener('submit', this.startDownload)
        }
    },
    methods: {
        validateUrl() {
            const urlInput = document.getElementById('url')
            if (!urlInput) return
            
            // Remove both classes first
            urlInput.classList.remove('is-valid', 'is-invalid')
            
            // Only validate if there's input
            if (this.url) {
                const regex = /^https:\/\//
                if (regex.test(this.url)) {
                    urlInput.classList.add('is-valid')
                } else {
                    urlInput.classList.add('is-invalid')
                }
            }
        },
        async startDownload(event) {
            event.preventDefault()
            const formData = new FormData(event.target)
            
            // Désactiver le bouton pendant le téléchargement
            const submitButton = event.target.querySelector('button[type="submit"]')
            submitButton.disabled = true
            
            // Initialiser la console
            this.consoleMessages = []

            // Créer une requête fetch avec un contrôleur abort
            const controller = new AbortController()
            const signal = controller.signal

            // Débuter la requête de téléchargement
            const downloadResponse = await fetch('/download', {
                method: 'POST',
                body: formData,
                signal: signal
            })

            // Démarrer la surveillance des messages de console
            this.downloadInterval = setInterval(async () => {
                try {
                    const response = await axios.get('/download/logs')
                    if (response.data && response.data.logs) {
                        // Ajouter les nouveaux messages
                        const newMessages = response.data.logs.filter(msg => !this.consoleMessages.includes(msg))
                        // Ajouter les nouveaux messages avec un formatage approprié
                        newMessages.forEach(msg => {
                            if (msg.startsWith('[')) {
                                // Messages yt-dlp avec couleur grise
                                this.consoleMessages.push(`<span style="color: #888;">${msg}</span>`)  
                            } else if (msg.includes('Progression:')) {
                                // Messages de progression avec couleur bleue
                                this.consoleMessages.push(`<span style="color: #007bff;">${msg}</span>`)  
                            } else if (msg.includes('erreur')) {
                                // Erreurs avec couleur rouge
                                this.consoleMessages.push(`<span style="color: #dc3545;">${msg}</span>`)  
                            } else {
                                // Messages normaux
                                this.consoleMessages.push(msg)
                            }
                        })
                        
                        // Mettre à jour l'affichage
                        this.$nextTick(() => {
                            const consoleOutput = document.querySelector('#consoleOutput pre')
                            if (consoleOutput) {
                                // Convertir les messages en HTML
                                const htmlContent = this.consoleMessages.join('<br>')
                                consoleOutput.innerHTML = htmlContent.replace(/\n/g, '<br>')
                                // Scroller automatiquement vers le bas
                                consoleOutput.parentElement.scrollTop = consoleOutput.parentElement.scrollHeight
                            }
                        })
                    }
                } catch (error) {
                    console.error('Erreur lors de la récupération des logs:', error)
                }
            }, 500) // Mise à jour plus fréquente pour une meilleure réactivité

            // Attendre la réponse complète
            const result = await downloadResponse.json()
            
            // Arrêter la surveillance
            clearInterval(this.downloadInterval)
            
            // Réactiver le bouton
            submitButton.disabled = false
            
            // Cacher la barre de progression
            this.showProgress = false
            
            // Rediriger vers la page de résultat
            window.location.href = '/result?success=' + result.success + '&message=' + encodeURIComponent(result.message)
        }
    },
    mounted() {
        // Ajouter l'écouteur d'événement au formulaire
        const form = document.querySelector('form')
        if (form) {
            form.addEventListener('submit', this.startDownload)
        }
    },
    unmounted() {
        // Nettoyer l'intervalle si l'application est démontée
        if (this.downloadInterval) {
            clearInterval(this.downloadInterval)
        }
    }
})

// Mount the Vue app
document.addEventListener('DOMContentLoaded', () => {
    app.mount('#app')
})

// Add Bootstrap Icons to the input field
const urlInput = document.getElementById('url')
if (urlInput) {
    urlInput.insertAdjacentHTML('afterend', `
        <div class="invalid-feedback">
            L'URL doit commencer par "https://"
        </div>
        <div class="valid-feedback">
            URL valide
        </div>
    `)
}