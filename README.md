# Fast Auth Tools (for FastAPI)

> Adds OAuth2 authentication to a FastAPI app with a single function

## Install

```shell
pip install fast-auth-tools
```

## Create User DB

```shell
fast-auth-user
```

## Example

```python
from fastapi import FastAPI, Depends

from fast_auth import fast_auth, logged_in_user, User


app = FastAPI()

fast_auth(app)  # adds /login and /refresh_token endpoints as well as setting CORS origins

# Example authenticated routes:
@app.get("/secure/get/", dependencies=[Depends(logged_in_user)])
async def must_be_logged_in():
    return {}

@app.post("/secure/post/")
async def get_user_object(user: User = Depends(logged_in_user)):
    print(f"password hash: {user.password}")
    return {
        "data": f"{user.username} is already logged in"
    }
```

## Settings

| name                     | default                                     | description                                                                           |
|--------------------------|---------------------------------------------|---------------------------------------------------------------------------------------|
| cors_origins             | \["*"\]                                     | allowed CORS origins                                                                  |
| secret_key               | "SoMeThInG\_-sUp3Rs3kREt!!"                 | the key used to encrypt JWT                                                           |
| algorithm                | "HS256"                                     | the algorithm used to encrypt JWT                                                     |
| access_token_expire_days | 5                                           | the maximum number of days JWT will be valid                                          |
| user_db_path             | ".../site_packages/fast_auth/users.sqlite3" | the path to the sqlite database that holds username/encrypted password information    |
| login_url                | "login"                                     | path to POST endpoint accepting username/password form data                           |
| token_refresh_url        | "refresh_token"                             | path to GET endpoint that takes a valid JWT and returns a new JWT with maximum expiry |

## Loading Settings from a File

You can load initial settings from a YAML file by setting the `SETTINGS_PATH` environment variable to the path of your settings file. If the file is not found, or any of the settings are not included in the file, default settings will be used.

Example `auth.yaml`:

```yaml
cors_origins:
  - "myapp.com"
  - "my-test-server.com"
secret_key: "your_secret_key"
algorithm: "HS256"
access_token_expire_days: 1
user_db_path: "./my_user_db.sqlite3"
login_url: "/auth/login"
token_refresh_url: "/auth/token"
```

Set the environment variable and run your application:

```shell
export SETTINGS_PATH=./auth.yaml
uvicorn main:app --reload
```

## Setting Individual Settings Dynamically

If required, you can set individual settings from within your application:

```python
from fastapi import FastAPI
from fast_auth import fast_auth, settings

app = FastAPI()

settings.user_db_path = "./my_user_db.sqlite3"
fast_auth(app)
```