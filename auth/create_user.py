from getpass import getpass

from auth import User
from auth.funcs import run


async def create_user(username, password):
    await User.create(username=username, password=password)
    print(f"{username} user created")


if __name__ == "__main__":
    run(create_user(input("username: "), getpass("password: ")))
