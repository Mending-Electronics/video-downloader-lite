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

### Prérequis
- Python 3.11 ou supérieur
- Git (facultatif pour cloner le dépôt)

### Recupérer le projet

#### Méthode 1 : Recupérer le projet via Git
```bash
# Cloner le dépôt
git clone [https://github.com/Mending-Electronics/video-downloader-lite.git](https://github.com/Mending-Electronics/video-downloader-lite.git)
cd video-downloader-lite
```

#### Méthode 2 : Téléchargement direct
1. Téléchargez le projet au format [ZIP](https://github.com/Mending-Electronics/video-downloader-lite/archive/refs/heads/main.zip)
2. Extrayez l'archive



#### Création de l'environnement virtuel et installation des dépendances

Executer : `script - setup.cmd`
   
#### Mettre à jour `yt-dlp`

Executer : `script - force-update-yt-dlp.cmd`


#### Lancement de l'application

Executer : `script - run.cmd`
   
L'application sera accessible à l'adresse : `http://localhost:5000`

## 📁 Structure de l'application

- `/downloads` : Dossier de destination des téléchargements
- `/templates` : Fichiers de template HTML
- `/static` : Fichiers statiques (CSS, JS, images, composants)

- `app.py` : Fichier principal de l'application (Serveur)
- `app.vue` : Fichier principal de l'application (Frontend)
- `index.html` : Template HTML (Serveur / Frontend)


## Captures d'écran

![Screenshot0001](https://github.com/Mending-Electronics/video-downloader-lite/blob/main/.screenshots/screenshot0001.png?raw=true "Screenshot0001")

![Screenshot0002](https://github.com/Mending-Electronics/video-downloader-lite/blob/main/.screenshots/screenshot0002.png?raw=true "Screenshot0002")

![Screenshot0003](https://github.com/Mending-Electronics/video-downloader-lite/blob/main/.screenshots/screenshot0003.png?raw=true "Screenshot0003")

![Screenshot0004](https://github.com/Mending-Electronics/video-downloader-lite/blob/main/.screenshots/screenshot0004.png?raw=true "Screenshot0004")


---

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




## 🛠️ Directives Vue.js essentielles

Vue.js propose des directives puissantes pour manipuler le DOM de manière déclarative. Voici les plus couramment utilisées :

### 1. v-bind - Liaison d'attributs
Permet de lier dynamiquement des attributs HTML ou des propriétés de composant à des expressions JavaScript.

**Syntaxe complète :**
```html
<a v-bind:href="url">Lien</a>
```

**Syntaxe abrégée (recommandée) :**
```html
<a :href="url">Lien</a>
```

**Exemples :**
```html
<!-- Liaison de classe -->
<div :class="{ active: isActive, 'text-danger': hasError }"></div>

<!-- Liaison de style -->
<div :style="{ color: textColor, fontSize: size + 'px' }"></div>

<!-- Liaison de plusieurs attributs -->
<div v-bind="{ id: someProp, 'aria-label': label }"></div>
```

### 2. v-if / v-else / v-else-if - Rendu conditionnel
Permet d'afficher conditionnellement un élément.

```html
<div v-if="type === 'A'">
  Type A
</div>
<div v-else-if="type === 'B'">
  Type B
</div>
<div v-else>
  Autre type
</div>
```

### 3. v-for - Boucles
Permet d'itérer sur des tableaux ou des objets.

```html
<!-- Itération sur un tableau -->
<ul>
  <li v-for="(item, index) in items" :key="item.id">
    {{ index }} - {{ item.message }}
  </li>
</ul>

<!-- Itération sur un objet -->
<ul>
  <li v-for="(value, key, index) in object">
    {{ index }}. {{ key }}: {{ value }}
  </li>
</ul>
```

### 4. v-on - Gestion des événements
Permet d'écouter les événements du DOM.

**Syntaxe complète :**
```html
<button v-on:click="doSomething">Cliquez-moi</button>
```

**Syntaxe abrégée (recommandée) :**
```html
<button @click="doSomething">Cliquez-moi</button>
```

**Modificateurs :**
```html
<!-- L'événement submit ne rechargera pas la page -->
<form @submit.prevent="onSubmit"></form>

<!-- Le gestionnaire ne sera appelé qu'une seule fois -->
<button @click.once="doThis"></button>

<!-- Le comportement par défaut du clic droit sera empêché -->
<button @contextmenu.prevent="showContextMenu">Menu</button>
```

### 5. v-model - Liaison bidirectionnelle
Crée une liaison bidirectionnelle sur un élément de formulaire.

```html
<input v-model="message" placeholder="Éditez-moi">
<p>Message : {{ message }}</p>

<!-- Avec des modificateurs -->
<input v-model.lazy="msg"> <!-- Mise à jour après le changement -->
<input v-model.number="age" type="number"> <!-- Convertit en nombre -->
<input v-model.trim="msg"> <!-- Supprime les espaces inutiles -->
```

### 6. v-html - Injection de HTML
Affiche le contenu HTML brut (attention aux attaques XSS).

```html
<div v-html="rawHtml"></div>
```

### 7. v-show - Affichage conditionnel (CSS)
Similaire à v-if mais utilise `display: none` au lieu de supprimer l'élément.

```html
<h1 v-show="isVisible">Visible ou non</h1>
```

### 8. v-cloak - Masquage du contenu non compilé
Empêche l'affichage du contenu non compilé avant que Vue ne prenne le contrôle.

```html
<div v-cloak>
  {{ message }}
</div>

<style>
  [v-cloak] {
    display: none;
  }
</style>
```

### Astuce : Syntaxe des deux-points
En Vue.js, le préfixe `:` est un raccourci pour `v-bind:`. Il peut être utilisé pour tous les attributs HTML pour les rendre dynamiques :

```html
<!-- Ces deux lignes sont équivalentes -->
<img v-bind:src="imageSrc">
<img :src="imageSrc">

<!-- Cela fonctionne avec n'importe quel attribut -->
<button :disabled="isButtonDisabled">Valider</button>
<input :placeholder="inputPlaceholder">
<div :class="[isActive ? activeClass : '', errorClass]"></div>
```

Cette syntaxe concise est largement utilisée dans les applications Vue.js pour une meilleure lisibilité du code.


### Présentation des hooks du cycle de vie de Vue.js 3

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
   - Gestion des erreurs asynchrones

#### Exemple d'application *.vue complète utilisant les hooks

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

// Montage de l'application sur l'element HTML ayant pour ID "app"
app.mount('#app');
```



# 🎯 Intégration Vue.js avec Flask

### Cohabitation des syntaxes Jinja et Vue.js

Pour éviter les erreurs d'interprétation dans les templates dû a la syntaxe moustache (`{{ }}`) commune a Jinja2 et Vue.js, modifiez les délimiteurs de Vue :

```javascript
const app = Vue.createApp({ 
  // ...
  delimiters: ['[[', ']]']
})
```


### Exemple de template *.html hybride Jinja2 et Vue.js

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


<!-- Import de notre application Vue / Il faut spécifier le type="text/javascript" pour que le navigateur comprenne que c'est du JavaScript ES5 -->
<script src="{{ url_for('static', filename='components/app.vue') }}" type="text/javascript"></script>
```




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