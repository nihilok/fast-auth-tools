from fastapi import FastAPI, Depends

from fast_auth import (
    fast_auth,
    get_current_user,
    User,
)

app = FastAPI()
fast_auth(app)


@app.get("/", dependencies=[Depends(get_current_user)])
async def root():
    return {"message": "Hello World"}


@app.get("/hello/")
async def say_hello(user: User = Depends(get_current_user)):
    return {"message": f"Hello {user.username}"}
