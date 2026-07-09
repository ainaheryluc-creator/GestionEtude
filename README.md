# Gestion des Etudes

Application de gestion academique avec trois interfaces : publique, etudiant, chef de departement.

## Tech Stack

- **Backend :** Flask 3.0, Flask-Login
- **Base de donnees :** MongoDB (PyMongo)
- **Frontend :** Bootstrap 5, theme dark personnalise

## Installation

1. **Cloner le projet**
   ```bash
   git clone <url>
   cd GestionEtude
   ```

2. **Creer un environnement virtuel**
   ```bash
   python -m venv venv
   venv\Scripts\activate   # Windows
   source venv/bin/activate  # Linux/Mac
   ```

3. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurer l'environnement**
   ```bash
   cp .env.example .env
   ```
   Editez `.env` avec vos parametres MongoDB.

5. **Initialiser la base de donnees**
   ```bash
   python init_db.py
   ```
   Cela cree les comptes chefs, etudiants, cours, inscriptions, notes et annonces.

6. **Lancer l'application**
   ```bash
   python main.py
   ```
   Acceder a http://localhost:5000

## Comptes par defaut

### Chefs de departement
| Email | Mot de passe | Departement |
|-------|-------------|-------------|
| chef.info@gestionetude.com | admin123 | Informatique |
| chef.gestion@gestionetude.com | admin123 | Gestion |
| chef.geniecivil@gestionetude.com | admin123 | Genie Civil |
| chef.communication@gestionetude.com | admin123 | Communication |

### Etudiants
Tous les etudiants ont le mot de passe : `etudiant123`

## Interfaces

- **Publique :** Page d'accueil, annonces publiques, connexion
- **Etudiant :** Tableau de bord, notes par semestre/UE, cours, annonces du departement
- **Chef :** Dashboard, CRUD etudiants/cours/inscriptions/notes/annonces, saisie de notes par semestre, classement des moyennes

## Production

```bash
python wsgi.py
```

Ou avec waitress :
```bash
waitress-serve --host=0.0.0.0 --port=5000 app:app
```
