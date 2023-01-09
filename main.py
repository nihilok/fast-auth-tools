from fastapi import FastAPI, Depends

from auth import auth_router, get_current_user

app = FastAPI()
app.include_router(auth_router)


@app.get("/", dependencies=[Depends(get_current_user)])
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}", dependencies=[Depends(get_current_user)])
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
