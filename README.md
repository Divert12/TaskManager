# TaskManager - Gestionnaire collaboratif de tâches

## Description
TasManager est une application web collaborative de gestion de tâches permettant à plusieurs utilisateurs de créer, organiser, attribuer et suivre des tâches, avec gestion d'équipes, visibilité privée/publique, et une interface moderne animée.

## Fonctionnalités principales
- Gestion des tâches (création, modification, suppression)
- Attribution à des utilisateurs et des équipes
- Tâches privées et publiques
- Gestion des équipes (création, liste, détails)
- Tableau de bord utilisateur
- Animations et interactions modernes
- Interface responsive

## Principales URLs de l’application
→ / : Page d’accueil
→ /login/ : Connexion
→ /signup/ : Inscription
→ /tasks/liste_taches/ : Liste des tâches
→ /tasks/ajouter_tache/ : Ajouter une tâche
→ /tasks/modifier_tache/<id>/ : Modifier une tâche
→ /tasks/supprimer_tache/<id>/ : Supprimer une tâche
→ /tasks/liste_equipes/ : Liste des équipes
→ /tasks/creer_equipe/ : Créer une équipe
→ /tasks/equipe_detail/<id>/ : Détail d’une équipe
→ /tasks/profil/ : Dashboard
1


## Installation

### Prérequis
- Python 3.8+

### Étapes

```bash
git clone <https://github.com/Divert12/TaskManager.git>
cd TaskManager
python -m venv venv
source venv/bin/activate
pip install django
pip install django-widget-tweaks
python manage.py runserver
```

## Utilisation

- Accédez à `http://localhost:8000/`
- Inscrivez-vous ou connectez-vous
- Créez des tâches, des équipes, attribuez des membres, etc.

## Structure du projet

- `tasks/models.py` : Modèles de données (Tâche, Équipe, Utilisateur)
- `tasks/views.py` : Vues principales (CRUD, dashboard, etc.)
- `tasks/forms.py` : Formulaires Django
- `tasks/templates/` : Templates HTML
- `tasks/static/` : Fichiers CSS/JS

## Personnalisation

- Les styles sont dans `tasks/static/tasks/css/style.css`
- Les templates principaux sont dans `tasks/templates/tasks/`


## Contribution

1. Forkez le projet
2. Créez une branche (`git checkout -b feature/ma-feature`)
3. Commitez vos changements (`git commit -am 'Ajout de ma feature'`)
4. Poussez la branche (`git push origin feature/ma-feature`)
5. Ouvrez une Pull Request

## Auteur

- Boudjelel Mahdi
