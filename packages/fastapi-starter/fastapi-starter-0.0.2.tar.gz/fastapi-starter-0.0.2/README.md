# FastAPI Starter Application

This application serves as a starter for FastAPI applications which interact with a relational database and provide user authentication.

## Specification

In order to extend this starter for an application, perform the following actions:

1.  Install the starter application with `pip install fastapi-starter`.
2.  Define the following environment variables:
    -   APPLICATION_NAME
    -   APPLICATION_DESCRIPTION
    -   DB_HOST
    -   DB_NAME
    -   DB_PASSWORD
    -   DB_USER
    -   DEBUG
    -   MAILGUN_API_KEY
    -   MAILGUN_DOMAIN_NAME
    -   MAILGUN_SENDER_EMAIL
    -   MAILGUN_SENDER_NAME
    -   SECRET_KEY (generate using `openssl rand -hex 32`)
3.  Define database models which inherit from `fastapi_starter.models.Base`.
4.  Define schemas which utilise the following mixins from `fastapi_starter.schemas` where appropriate:
    -   `HasOwner`
    -   `InDatabase`
    -   `Updatable`
5.  Define and include `FastAPI.APIRouter`s to the `fastapi_starter.app` application.
6.  Create database tables with:

    ```python
    from fastapi_starter.database import engine
    from fastapi_starter.models import Base


    Base.metadata.create_all(bind=engine)
    ```

## Components

-   The [PyMySQL](https://pymysql.readthedocs.io/en/latest/) driver is used with [SQLAlchemy](https://www.sqlalchemy.org/) to provide a declarative interface between the FastAPI controllers and a MySQL database instance.
-   The [FastAPI Another JWT Auth](https://glitchcorp.github.io/fastapi-another-jwt-auth/) plugin is used to provide JWT authentication to the FastAPI application.

```

```
