# Template de Site Web Python avec CMS Intégré

Un template moderne de site web en Python avec un système de gestion de contenu (CMS) complet, permettant aux administrateurs de gérer facilement le contenu, les pages, les médias et l'apparence du site.

## Fonctionnalités

### 🎨 Gestion de l'Apparence
- **Personnalisation des couleurs** : Modifiez facilement les couleurs primaires, secondaires, d'accent, de fond et de texte
- **Gestion du logo** : Téléchargez et définissez votre logo personnalisé
- **Favicon** : Ajoutez votre propre favicon
- **Pied de page personnalisable** : Modifiez le texte du footer

### 📄 Gestion de Pages
- **Création de pages dynamiques** : Créez autant de pages que nécessaire
- **Éditeur HTML** : Éditez le contenu avec du HTML pour un contrôle total
- **URLs personnalisées (slugs)** : Définissez des URLs conviviales pour chaque page
- **Publication/Brouillon** : Contrôlez la visibilité de vos pages
- **Gestion du menu** : Choisissez quelles pages apparaissent dans le menu de navigation
- **Ordre du menu** : Définissez l'ordre d'affichage des pages dans le menu

### 🖼️ Médiathèque
- **Upload de médias** : Téléchargez des images (PNG, JPG, JPEG, GIF, WEBP, SVG)
- **Gestion centralisée** : Organisez tous vos médias au même endroit
- **Textes alternatifs** : Ajoutez des descriptions pour l'accessibilité
- **Copie rapide d'URL** : Copiez facilement l'URL de vos médias

### 👥 Gestion des Utilisateurs
- **Système d'authentification** : Connexion sécurisée
- **Rôles administrateur** : Contrôlez qui peut modifier le site
- **Gestion multi-utilisateurs** : Créez plusieurs comptes administrateurs

## Installation

### Prérequis
- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Étapes d'installation

1. **Cloner le repository**
   ```bash
   git clone <votre-repo-url>
   cd python_web_template
   ```

2. **Créer un environnement virtuel**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Sur Linux/Mac
   # ou
   venv\Scripts\activate  # Sur Windows
   ```

3. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurer les variables d'environnement**
   ```bash
   cp .env.example .env
   # Éditez .env et modifiez les valeurs selon vos besoins
   ```

5. **Initialiser la base de données**
   ```bash
   python init_db.py
   ```

   Cela créera :
   - Un utilisateur admin par défaut (username: `admin`, password: `admin123`)
   - Un thème par défaut
   - Des pages d'exemple

6. **Lancer l'application**
   ```bash
   python run.py
   ```

7. **Accéder au site**
   Ouvrez votre navigateur et allez sur `http://localhost:5000`

## Utilisation

### Première connexion

1. Allez sur `http://localhost:5000/auth/login`
2. Connectez-vous avec :
   - **Nom d'utilisateur** : `admin`
   - **Mot de passe** : `admin123`
3. **IMPORTANT** : Changez le mot de passe par défaut immédiatement !

### Accéder au panneau d'administration

Une fois connecté en tant qu'administrateur, cliquez sur "Admin" dans le menu de navigation ou allez sur `http://localhost:5000/admin`

### Gérer les pages

1. Dans le panneau admin, cliquez sur "Pages"
2. Cliquez sur "Nouvelle page" pour créer une page
3. Remplissez les informations :
   - **Titre** : Le titre de votre page
   - **Slug** : L'URL de la page (généré automatiquement depuis le titre)
   - **Contenu** : Le contenu HTML de votre page
   - **Publié** : Cochez pour rendre la page visible
   - **Afficher dans le menu** : Cochez pour ajouter la page au menu de navigation
   - **Ordre dans le menu** : Numéro pour définir la position (0 = premier)

### Gérer les médias

1. Cliquez sur "Médias" dans le panneau admin
2. Cliquez sur "Télécharger un fichier"
3. Sélectionnez votre image et ajoutez un texte alternatif
4. Une fois téléchargé, vous pouvez copier l'URL du média pour l'utiliser dans vos pages

### Personnaliser l'apparence

1. Cliquez sur "Apparence" dans le panneau admin
2. Modifiez le nom du site et les couleurs
3. Cliquez sur "Choisir un logo" ou "Choisir un favicon" pour sélectionner un média
4. Enregistrez vos modifications

## Structure du projet

```
python_web_template/
├── app/
│   ├── __init__.py          # Initialisation de l'application Flask
│   ├── models.py            # Modèles de base de données
│   ├── forms.py             # Formulaires WTForms
│   ├── routes/              # Routes de l'application
│   │   ├── main.py          # Routes publiques
│   │   ├── auth.py          # Authentification
│   │   └── admin.py         # Routes d'administration
│   ├── templates/           # Templates Jinja2
│   │   ├── layouts/         # Templates de base
│   │   ├── pages/           # Templates des pages publiques
│   │   ├── admin/           # Templates du panneau admin
│   │   └── auth/            # Templates d'authentification
│   └── static/              # Fichiers statiques
│       ├── css/             # Styles CSS personnalisés
│       ├── js/              # Scripts JavaScript
│       └── uploads/         # Médias téléchargés
├── config.py                # Configuration de l'application
├── requirements.txt         # Dépendances Python
├── run.py                   # Point d'entrée de l'application
├── init_db.py               # Script d'initialisation de la base de données
└── README.md                # Ce fichier
```

## Modèles de données

### User (Utilisateur)
- `username` : Nom d'utilisateur unique
- `email` : Adresse email unique
- `password_hash` : Mot de passe hashé
- `is_admin` : Booléen pour les droits administrateur

### Page
- `title` : Titre de la page
- `slug` : URL de la page
- `content` : Contenu HTML
- `is_published` : Statut de publication
- `show_in_menu` : Affichage dans le menu
- `menu_order` : Ordre d'affichage

### Media
- `filename` : Nom du fichier
- `original_filename` : Nom d'origine
- `file_path` : Chemin du fichier
- `file_type` : Type de média
- `alt_text` : Texte alternatif

### Theme
- `site_name` : Nom du site
- `primary_color` : Couleur primaire
- `secondary_color` : Couleur secondaire
- `accent_color` : Couleur d'accent
- `background_color` : Couleur de fond
- `text_color` : Couleur du texte
- `logo_id` : Référence au logo
- `favicon_id` : Référence au favicon
- `footer_text` : Texte du pied de page

## Technologies utilisées

- **Flask** : Framework web Python
- **Flask-SQLAlchemy** : ORM pour la gestion de la base de données
- **Flask-Login** : Gestion de l'authentification
- **Flask-WTF** : Gestion des formulaires
- **Bootstrap 5** : Framework CSS pour le design
- **Bootstrap Icons** : Icônes
- **SQLite** : Base de données (par défaut)

## Configuration

### Variables d'environnement (.env)

```env
SECRET_KEY=votre-clé-secrète-ici
DATABASE_URL=sqlite:///cms.db
FLASK_ENV=development
UPLOAD_FOLDER=app/static/uploads
MAX_CONTENT_LENGTH=16777216  # 16MB en octets
```

### Sécurité

⚠️ **IMPORTANT pour la production** :
- Changez le `SECRET_KEY` par une valeur aléatoire et sécurisée
- Changez le mot de passe admin par défaut
- Utilisez HTTPS
- Configurez un serveur de production (Gunicorn, uWSGI)
- Utilisez une base de données de production (PostgreSQL, MySQL)
- Configurez les sauvegardes régulières de la base de données

## Développement futur

Fonctionnalités potentielles à ajouter :
- Éditeur WYSIWYG pour le contenu
- Système de catégories pour les pages
- Blog avec articles et commentaires
- Galerie d'images
- Formulaire de contact
- SEO (métadonnées, sitemap)
- Multi-langues
- Système de cache
- API REST

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## Support

Pour toute question ou problème, ouvrez une issue sur le repository GitHub.

---

**Fait avec ❤️ en Python et Flask**
