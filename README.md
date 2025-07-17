# 📥 Video Downloader Lite

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/flask-2.0.1+-green.svg)](https://flask.palletsprojects.com/)
[![Vue.js](https://img.shields.io/badge/vue.js-3.0+-4FC08D.svg?logo=vue.js)](https://vuejs.org/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Une application web légère et performante pour télécharger des vidéos depuis des milliers de sites (dont YouTube) au format MP4 ou en extraire l'audio en MP3.

## 🚀 Fonctionnalités

- Téléchargement de vidéos depuis de nombreuses plateformes
- Conversion en MP3 ou MP4
- Interface utilisateur moderne et réactive
- Aucune installation de Node.js requise
- Mise à jour automatique de yt-dlp

## 🛠️ Technologies utilisées

### Backend
- **Python Flask** : Serveur web léger et puissant
  - Gestion des routes API
  - Intégration transparente avec yt-dlp
  - Configuration CORS pour la sécurité

### Frontend
- **Vue.js 3** (CDN) : Framework JavaScript progressif
  - Réactivité et composants
  - Gestion d'état simple et efficace
  - Pas de build nécessaire

### Outils
- **Axios** (CDN) : Client HTTP pour les appels API
- **Bootswatch** (Bootstrap 5) : Thèmes CSS prêts à l'emploi

## ⚙️ Installation

1. **Prérequis** :
   - Python 3.8 ou supérieur
   - Git (pour cloner le dépôt)

2. **Configuration** :
   ```bash
   # Cloner le dépôt
   git clone https://github.com/Mending-Electronics/video-downloader-lite.git
   cd video-downloader-lite
   
   # Installer les dépendances
   script - setup.cmd
   
   # Mettre à jour yt-dlp
   script - force-update-yt-dlp.cmd
   ```

3. **Lancement** :
   ```bash
   script - run.cmd
   ```
   L'application sera accessible à l'adresse : `http://localhost:5000`

## 📁 Structure des dossiers

- `/downloads` : Dossier de destination des téléchargements
- `/templates` : Fichiers de template HTML
- `/static` : Fichiers statiques (CSS, JS, images, composants)








## Screenshots

![Screenshot0001](https://github.com/Mending-Electronics/video-downloader-lite/blob/main/.screenshots/screenshot0001.png?raw=true "Screenshot0001")

![Screenshot0002](https://github.com/Mending-Electronics/video-downloader-lite/blob/main/.screenshots/screenshot0002.png?raw=true "Screenshot0002")

![Screenshot0003](https://github.com/Mending-Electronics/video-downloader-lite/blob/main/.screenshots/screenshot0003.png?raw=true "Screenshot0003")

![Screenshot0004](https://github.com/Mending-Electronics/video-downloader-lite/blob/main/.screenshots/screenshot0004.png?raw=true "Screenshot0004")



## 🎯 Intégration Vue.js avec Flask

### Configuration des délimiteurs

Pour éviter les conflits entre la syntaxe de template Jinja2 (`{{ }}`) et Vue.js, modifiez les délimiteurs de Vue :

```javascript
const app = Vue.createApp({
  // ...
  delimiters: ['[[', ']]']
})
```

### Exemple de template hybride

```html
<div id="app">
  <!-- Syntaxe Jinja2 -->
  <h1>Bienvenue, {{ username }}!</h1>
  
  <!-- Syntaxe Vue.js -->
  <p>Compteur : [[ count ]]</p>
  <button @click="increment">+1</button>
  
  <!-- Liaisons d'attributs avec v-bind -->
  <div :class="{ active: isActive }">
    Contenu dynamique
  </div>
  
  <!-- v-model pour la liaison bidirectionnelle -->
  <input v-model="message" placeholder="Éditez-moi">
  
  <!-- v-for pour les listes -->
  <ul>
    <li v-for="item in items" :key="item.id">
      [[ item.text ]]
    </li>
  </ul>
  
  <!-- v-if pour le rendu conditionnel -->
  <div v-if="showMessage">
    Message important !
  </div>
  
  <!-- v-cloak pour éviter le flash de contenu non compilé -->
  <div v-cloak>
    [[ message ]]
  </div>
</div>

<style>
  [v-cloak] { display: none; }
</style>
```

### Hooks Vue.js utiles

- **created()** : Appelé après la création de l'instance
- **mounted()** : Appelé après l'insertion dans le DOM
- **updated()** : Appelé après une mise à jour du DOM
- **unmounted()** : Appelé après la destruction de l'instance

## 💡 Pourquoi cette stack ?

- **Développement rapide** : Pas de processus de build complexe
- **Léger** : Aucune installation de Node.js requise
- **Flexible** : Combinaison puissante de Flask et Vue.js
- **Facile à déployer** : Un simple serveur Python suffit

## 📝 Crédits

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - Outil de téléchargement de vidéos
- [Vue.js](https://vuejs.org/) - Framework JavaScript progressif
- [Flask](https://flask.palletsprojects.com/) - Micro-framework web Python
- [Bootswatch](https://bootswatch.com/) - Thèmes Bootstrap gratuits

## 📜 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

<p align="center">
  Développé avec ❤️ par Mending Electronics
</p>