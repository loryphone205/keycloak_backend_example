# Keycloak Backend Token Validation Example
This project has the objective to utilize the package `python-keycloak` and `django` to validate JWT Tokens from Keycloak. 
Keycloak version mismatch doesn't matter as long as it's a small release.
---
# What's needed:
- JDK 24 or newer
- PostgreSQL 17 or newer

## What to do: 
### Keycloak Setup
- [Download](https://github.com/keycloak/keycloak/releases/download/26.3.3/keycloak-26.3.3.zip) Keycloak Standalone Server, Extract it. (version 26.3.2)
- Create a Database named `keycloak` with password `mysecret` (remember to grant all privileges on `keycloak`)
- Edit the file `path/to/keycloak-26.3.2/conf/keycloak.conf` to match your database settings:
    ```
    db=postgres
    db-url=jdbc:postgresql://localhost:5432/keycloak
    db-username=keycloak
    db-password=mypassword
    hostname=localhost
    ```
- Set the following evironment variables:
    ```
    set KEYCLOAK_ADMIN=admin
    set KEYCLOAK_ADMIN_PASSWORD=admin
    ```
- Navigate to `path/to/keycloak-26.3.2/bin/` and open a Terminal. Execute: `kc.bat start-dev`
- Navigate to `http://localhost:8080`
- When prompted, login with username `admin ` and password `admin `
- Click on Top-Left Hamburger Menu >`Manage Realms` >`Create Realm`:
- Realm name will be `realm-prova` (check that `realm-prova` is the `Current realm`)
- Under`Manage `, go to `Clients ` > `Create Client`:
    ```
    Client ID: react-app
    Client Type: OpenID Connect
    Client Authentication: Off
    Authentication Flow: Standard Flow
    Web Origins: http://localhost:3000
    Valid Redirect URIs: http://localhost:3000/*
    ```
- Under`Manage `, go to `Users ` > `Add user`:
    ```
    Username: testuser
    ```
- You should be on the testuser tab. Click on `Credentials ` and create a new password

### Backend Setup
- Pull this repo
- Install packages found in the `requirements.txt`
- Start the server with `python manage.py runserver` and eventually run migrations with `python manage.py migrate`
---
# Testing

The functionalities can be tested with either postman, curl, or any other tool suited for http calls. 
Please use the Frotend Example for a little demo. It can be found [here](https://github.com/loryphone205/keycloak_frontend_example).
