# 📥 Video Downloader Lite

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/flask-2.0.1+-green.svg)](https://flask.palletsprojects.com/)
[![Vue.js](https://img.shields.io/badge/vue.js-3.0+-4FC08D.svg?logo=vue.js)](https://vuejs.org/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

> Une application web légère et performante pour télécharger des vidéos depuis des milliers de sites (dont YouTube) au format MP4 ou MP3.

## 🚀 Fonctionnalités

- Téléchargement de vidéos depuis de nombreuses plateformes
- Conversion automatique en MP3 si ce format est choisi
- Interface utilisateur moderne et réactive
- Mise à jour semi-automatique de yt-dlp


## 🛠️ Technologies utilisées

### Backend
- **Python Flask** : Serveur web léger et puissant
  - Gestion des routes API
  - Intégration de la methode de telechargement des videos via `yt-dlp`
  - Configuration CORS pour la sécurité

### Frontend
- **Vue.js 3** (CDN) : Framework JavaScript ES5 progressif
  - Réactivité et composants
  - Gestion du DOM simple et efficace
  - Pas de build nécessaire (Aucune installation de Node.js requise)

- **Axios** (CDN) : Client HTTP pour les appels API

- **Bootswatch** (Bootstrap 5) : Thèmes CSS prêts à l'emploi

## ⚙️ Installation

1. **Prérequis** :
   - Python 3.11 ou supérieur
   - Git (pour cloner le dépôt)

2. **Configuration** :
   ```bash
   # Cloner le dépôt
   git clone https://github.com/Mending-Electronics/video-downloader-lite.git
   cd video-downloader-lite
  ```

  ou Telecharger le projet au format `*.zip` depuis le bouton `Code` en haut de la page

   # Création de l'environnement virtuel et installation des dépendances
   Executer : `script - setup.cmd`
   
   # Mettre à jour `yt-dlp`
   Executer : `script - force-update-yt-dlp.cmd`


3. **Lancement** :
   Executer : `script - run.cmd`
   
   L'application sera accessible à l'adresse : `http://localhost:5000`

## 📁 Structure de l'application

- `/downloads` : Dossier de destination des téléchargements
- `/templates` : Fichiers de template HTML
- `/static` : Fichiers statiques (CSS, JS, images, composants)

- app.py : Fichier principal de l'application (Serveur)
- app.vue : Fichier principal de l'application (Frontend)
- index.html : Template HTML (Serveur / Frontend)


## Captures d'écran

![Screenshot0001](https://github.com/Mending-Electronics/video-downloader-lite/blob/main/.screenshots/screenshot0001.png?raw=true "Screenshot0001")

![Screenshot0002](https://github.com/Mending-Electronics/video-downloader-lite/blob/main/.screenshots/screenshot0002.png?raw=true "Screenshot0002")

![Screenshot0003](https://github.com/Mending-Electronics/video-downloader-lite/blob/main/.screenshots/screenshot0003.png?raw=true "Screenshot0003")

![Screenshot0004](https://github.com/Mending-Electronics/video-downloader-lite/blob/main/.screenshots/screenshot0004.png?raw=true "Screenshot0004")


---


# 🎯 Intégration Vue.js avec Flask

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
  <!-- 1. Syntaxe de base -->
  
  <!-- Affichage d'une variable Jinja2 (côté serveur) -->
  <h1>Bienvenue, {{ username }}!</h1>
  
  <!-- Affichage d'une variable Vue.js (côté client) -->
  <p>Compteur : [[ count ]]</p>
  <button @click="increment">+1</button>
  
  <!-- 2. Exemple d'imbrication : Boucle Jinja2 avec du contenu Vue.js -->
  {% for category in categories %}
    <div class="category">
      <!-- Utilisation de la variable de boucle Jinja2 dans un attribut Vue -->
      <h2 :class="['category-title', '{{ category.slug }}']">
        {{ category.name }}
      </h2>
      
      <!-- Boucle Vue.js à l'intérieur d'une boucle Jinja2 -->
      <ul>
        <li v-for="item in items" v-if="item.category === '{{ category.id }}'" :key="item.id">
          [[ item.name ]] - {{ category.name }}
        </li>
      </ul>
    </div>
  {% endfor %}
  
  <!-- 3. Exemple de condition Jinja2 avec contenu Vue.js -->
  {% if user.is_authenticated %}
    <div class="user-panel">
      <!-- Le contenu Vue.js ne sera rendu que si l'utilisateur est authentifié -->
      <p>Bonjour {{ user.username }}, vous avez <strong>[[ unreadCount ]]</strong> messages non lus.</p>
      
      <!-- v-show avec une condition Jinja2 -->
      <div v-show="hasNotifications" class="notifications">
        {% if user.has_notifications %}
          <p>Nouvelles notifications : [[ notificationCount ]]</p>
        {% else %}
          <p>Aucune nouvelle notification</p>
        {% endif %}
      </div>
    </div>
  {% else %}
    <p>Veuillez vous connecter pour voir votre contenu personnalisé.</p>
  {% endif %}
  
  <!-- 4. Utilisation de v-model avec des valeurs initiales Jinja2 -->
  <input 
    v-model="searchQuery" 
    :placeholder="'Rechercher dans {{ total_items }} éléments...'"
    @input="performSearch">
  
  <!-- 5. v-cloak pour éviter le flash de contenu non compilé -->
  <div v-cloak>
    [[ message ]]
  </div>
</div>

<style>
  /* 
    [v-cloak] est utilisé pour masquer les balises contenant des expressions Vue.js
    jusqu'à ce que l'application soit complètement compilée.
    Cela évite d'afficher brièvement le code source (comme {{ message }}) 
    avant que Vue.js ne prenne le contrôle du rendu.
  */
  [v-cloak] { 
    display: none; 
  }
  .category {
    margin-bottom: 20px;
    padding: 10px;
    border: 1px solid #eee;
  }
  .category-title {
    color: #2c3e50;
  }
</style>
```

### Tous les hooks du cycle de vie de Vue.js 3

#### Hooks de création et d'initialisation
- **beforeCreate()** : Appelé immédiatement après l'initialisation de l'instance
- **created()** : Appelé après la création de l'instance (données réactives disponibles)
- **beforeMount()** : Appelé avant le montage du composant dans le DOM
- **mounted()** : Appelé après le montage du composant dans le DOM

#### Hooks de mise à jour
- **beforeUpdate()** : Appelé avant qu'une modification du DOM réactif ne soit appliquée
- **updated()** : Appelé après une mise à jour du DOM réactif

#### Hooks de destruction
- **beforeUnmount()** : Appelé avant la destruction du composant (remplace `beforeDestroy` de Vue 2)
- **unmounted()** : Appelé après la destruction du composant (remplace `destroyed` de Vue 2)

#### Hooks de gestion des erreurs
- **errorCaptured()** : Appelé lorsqu'une erreur est capturée depuis un composant enfant
- **renderTracked()** : Appelé lorsqu'une dépendance de rendu est suivie (débogage)
- **renderTriggered()** : Appelé lorsqu'une dépendance de rendu déclenche un nouveau rendu (débogage)
- **onRenderTracked()** (Composition API) : Équivalent à renderTracked
- **onRenderTriggered()** (Composition API) : Équivalent à renderTriggered

#### Exemple complet d'utilisation des hooks

```javascript
const app = Vue.createApp({
  data() {
    return {
      message: 'Bonjour Vue!',
      count: 0,
      userData: null,
      error: null
    };
  },
  
  // Hooks de création
  beforeCreate() {
    console.log('beforeCreate: Pas encore de données réactives');
  },
  
  created() {
    console.log('created: Données réactives disponibles');
    this.fetchUserData();
  },
  
  beforeMount() {
    console.log('beforeMount: Avant le rendu du DOM');
  },
  
  mounted() {
    console.log('mounted: Composant monté dans le DOM');
    // Accès aux éléments du DOM
    this.$refs.myButton.focus();
  },
  
  // Hooks de mise à jour
  beforeUpdate() {
    console.log('beforeUpdate: Avant la mise à jour du DOM');
  },
  
  updated() {
    console.log('updated: DOM mis à jour');
  },
  
  // Hooks de destruction
  beforeUnmount() {
    console.log('beforeUnmount: Avant la destruction du composant');
    // Nettoyage des écouteurs d'événements, des timers, etc.
    window.removeEventListener('resize', this.handleResize);
  },
  
  unmounted() {
    console.log('unmounted: Composant détruit');
  },
  
  // Gestion des erreurs
  errorCaptured(err, vm, info) {
    console.error('Erreur capturée:', err, info);
    this.error = `Une erreur est survenue: ${err.message}`;
    // Empêche la propagation de l'erreur
    return false;
  },
  
  methods: {
    increment() {
      this.count++;
    },
    
    async fetchUserData() {
      try {
        const response = await fetch('/api/user');
        this.userData = await response.json();
      } catch (err) {
        this.error = 'Échec du chargement des données utilisateur';
        console.error(err);
      }
    },
    
    handleResize() {
      console.log('Fenêtre redimensionnée');
    }
  },
  
  // Définition des délimiteurs personnalisés pour éviter les conflits avec Jinja2
  delimiters: ['[[', ']]']
});

app.mount('#app');
```

### Meilleures pratiques pour l'utilisation des hooks

1. **created()** : 
   - Chargement initial des données
   - Configuration des écouteurs d'événements globaux
   
2. **mounted()** :
   - Accès aux éléments du DOM
   - Initialisation des bibliothèques tierces nécessitant le DOM
   
3. **beforeUnmount()** :
   - Nettoyage des écouteurs d'événements
   - Annulation des requêtes en cours
   - Nettoyage des timers et des abonnements
   
4. **errorCaptured()** :
   - Journalisation des erreurs
   - Affichage des messages d'erreur conviviaux
   - Gération des erreurs asynchrones

## 💡 Pourquoi cette stack ?

- **Développement rapide** : Pas de processus de build complexe
- **Léger** : Aucune installation de Node.js requise
- **Flexible** : Combinaison puissante de Flask et Vue.js
- **Facile à déployer** : Un simple serveur Python suffit
- **Architecture moderne** : Séparation claire entre le frontend (Vue.js) et le backend (Flask) qui communique via une API RESTful
- **Évolutif** : Le découplage permet de faire évoluer indépendamment chaque partie de l'application
- **Courbe d'apprentissage douce** : Vue.js et Flask sont réputés pour leur accessibilité tout en restant puissants
- **Adaptabilité** : Idéal pour des projets de toutes tailles, du prototype rapide à l'application complète
- **Écosystème complet** : Accès aux riches écosystèmes Python et JavaScript
- **Performance optimisée** : 
  - *Côté serveur* : Flask est extrêmement léger et rapide, et la logique métier est allégée car le rendu est principalement géré côté client
  - *Côté client* : Vue.js offre des performances optimales grâce à son DOM virtuel et à son système de rendu réactif
  - *Architecture efficace* : La majeure partie du traitement est effectuée dans le navigateur, réduisant ainsi la charge sur le serveur
- **Chargement rapide via CDN** :
  - Les bibliothèques (Vue.js, Axios, Bootstrap) sont chargées depuis des CDN mondiaux
  - Distribution géographique des serveurs CDN pour des temps de chargement réduits
  - Mise en cache navigateur optimisée pour les ressources fréquemment utilisées
  - Sécurité renforcée avec les dernières versions stables des bibliothèques
- **Maintenabilité** : Architecture propre qui facilite la maintenance et l'ajout de nouvelles fonctionnalités

Cette stack est parfaitement adaptée aussi bien pour des projets personnels que professionnels. Sa simplicité d'accès en fait un excellent choix pour les débutants, tandis que ses capacités étendues permettent de développer des applications complexes et performantes, comparables à ce que l'on pourrait faire avec des combinaisons plus lourdes comme Django/React, mais avec une configuration initiale bien plus légère et une courbe d'apprentissage plus douce.

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