from getpass import getpass

from auth import User
from auth.funcs import run


async def create_user(username, password):
    user = User(username=username, password=password)
    await user.save()


if __name__ == '__main__':
    run(create_user(input("username: "), getpass("password: ")))
