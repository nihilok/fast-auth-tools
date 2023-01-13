import sqlite3
from getpass import getpass

from auth.create_user import create_user, run_create_user
from auth.funcs import run
from constants import USER_DB


def create_user_table():
    SQL = """CREATE TABLE IF NOT EXISTS users (
        username text PRIMARY KEY,
        password text NOT NULL
    );"""

    db = sqlite3.connect(USER_DB)
    cursor = db.cursor()
    cursor.execute(SQL)
    db.commit()
    if input("Would you like to create a user? [Y/n]: ").strip().lower() in {
        "n",
        "no",
    }:
        return
    run_create_user()


if __name__ == "__main__":
    create_user_table()
