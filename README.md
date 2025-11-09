# Concrete Datasource Backend (Django REST API)

## Objectif

Ce projet a pour but de créer une **API REST** avec Django REST Framework permettant :
- L'inscription (`register`) d’un nouvel utilisateur.
- L’authentification (`login`) et la génération de jeton (`Token Authentication`).
- La création d’une **demande d’application**.
- La confirmation d’une application.

Ce projet constitue une base solide pour tout backend d’application Django RESTful utilisant Docker et SQLite.

---
## Prérequis

Avant de lancer le projet, assurez-vous d’avoir installé sur votre machine :
- **Python 3.11+**
- **Docker** et **Docker Compose**
- **Git**

---

## Fonctionnalités principales

| Endpoint | Méthode | Description |
|-----------|----------|-------------|
| `/api/register/` | `POST` | Inscription d’un utilisateur |
| `/api/login/` | `POST` | Connexion d’un utilisateur |
| `/api/create-application/` | `POST` | Création d’une demande d’application |
| `/api/confirm-application/<id>/` | `PATCH` | Confirmation d’une application |

---

## Étapes de lancement

### 1️- Cloner le dépôt

```
git clone https://github.com/soniarimamy/concrete_datasource_backend.git
```
### 2️ - Se déplacer dans le projet
```
cd concrete_datasource_backend
```

###  3️- Lancer l’application avec Docker
```
docker-compose up --build -d
```

L’API sera accessible à l’adresse :
http://127.0.0.1:8003

### 4 - Test des fonctionnalités via curl
#### 1. Enregistrer un utilisateur
```
curl -X POST http://127.0.0.1:8003/api/register/ \
-H "Content-Type: application/json" \
-d '{
  "email":"rakoto@example.com",
  "username":"rakoto",
  "password1":"abc123",
  "password2":"abc123"
}'
```

####  2. Se connecter
```
curl -X POST http://127.0.0.1:8003/api/login/ \
-H "Content-Type: application/json" \
-d '{"email":"test@example.com","password":"abc123"}'
```

Vous obtiendrez un jeton d’authentification du type :
"token": "f026b93430a70a1b97421331c5b2c8a2cc5df458"

#### 3. Créer une demande d’application
```
curl -X POST http://127.0.0.1:8003/api/create-application/ \
-H "Content-Type: application/json" \
-H "Authorization: Token f026b93430a70a1b97421331c5b2c8a2cc5df458" \
-d '{"first_name":"Rochel","last_name":"Soniarimamy"}'
```

#### 4. Confirmer la demande
```
curl -X PATCH http://127.0.0.1:8003/api/confirm-application/1/ \
-H "Content-Type: application/json" \
-H "Authorization: Token f026b93430a70a1b97421331c5b2c8a2cc5df458" \
-d '{"confirmed": true}'
```

###  5 - Docker Hub

L’image Docker officielle du projet est disponible sur Docker Hub :
```
docker pull rochel05/concrete_datasource_backend:latest
```

Vous pouvez l’utiliser directement pour déployer le projet sans builder l’image localement.

## Architecture du projet
```
concrete_datasource_backend/
├── concrete_datasource_backend/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
├── concrete_datasource_api/
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   ├── models.py
├── Dockerfile
├── docker-compose.yml
└── manage.py
```

## Licence

Ce projet est distribué sous la licence MIT.
Vous êtes libre de l’utiliser, le modifier et le redistribuer à condition de mentionner l’auteur original.

## Auteur
```
Nom : Rochel Soniarimamy
Email : rochel.soniarimamy@gmail.com
Docker Hub : rochel05
GitHub : https://github.com/soniarimamy/
```

## Contact
Pour toute question, suggestion ou contribution, veuillez me contacter par:
```
Email: rochel.soniarimamy@gmail.com
Telephone: +261349251646
```
