from fastapi import FastAPI, Depends

from fast_auth import (
    fast_auth,
    logged_in_user,
    User,
)

app = FastAPI()
fast_auth(app)


@app.get("/", dependencies=[Depends(logged_in_user)])
async def root():
    return {"message": "Hello World"}


@app.get("/hello/")
async def say_hello(user: User = Depends(logged_in_user)):
    return {"message": f"Hello {user.username}"}
