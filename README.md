# totalechaos

### Environment file for Docker

    DEBUG=0
    SECRET_KEY=changeme
    DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
    
    SQL_ENGINE=django.db.backends.postgresql
    SQL_DATABASE=[same as POSTGRES_DB]
    SQL_USER=[same as POSTGRES_USER]
    SQL_PASSWORD=[same as POSTGRES_PASSWORD]
    SQL_HOST=db
    SQL_PORT=5432
    
    POSTGRES_USER=[same as SQL_USER]
    POSTGRES_PASSWORD=[same as SQL_PASSWORD]
    POSTGRES_DB=[same as SQL_DATABASE]
    
    TZ=Europe/Amsterdam
