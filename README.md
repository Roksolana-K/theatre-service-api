# Theatre Service API
>The Theatre Service API is a Django REST 
Framework-based project that allows users 
to manage and explore a theater system. 
Authenticated users can book tickets for 
performances, while administrators have 
full control over all data.


# Features
- JWT Authentication (via SimpleJWT)
- Interactive API Docs (Swagger / Redoc)
- User registration & login
- Manage actors, genres, plays, theatres
- Book tickets for performances
- View upcoming performance schedules
- Filtering by actor, genre, theatre, title
- Docker / docker-compose support

# Quick Start with Docker
> Make sure Docker and docker-compose are installed on your machine.
```shell
# Clone the repository
git clone https://github.com/Roksolana-K/theatre-service-api

# Move into the project directory
cd theatre-service-api

# Build the Docker containers
docker-compose build

# Start the containers
docker-compose up
```

#  Access the App
Once running, visit:
```shell
http://127.0.0.1:8000/
```
>## Permissions:
> - Anonymous users - can view public information
> - Registered users - can make tickets reservations
> - Admin users - have full CRUD access to all models via the admin panel or API

>## Authentication:
> ```shell
> /api/user/register/
> ```
> Create Superuser:
> ```shell
> docker exec -it theatre-backend sh
> python manage.py createsuperuser
> ```

