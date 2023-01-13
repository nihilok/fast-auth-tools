import sqlite3

from auth.create_user import run_create_user
from settings import settings


def create_user_table():
    SQL = """CREATE TABLE IF NOT EXISTS users (
        username text PRIMARY KEY,
        password text NOT NULL
    );"""

    db = sqlite3.connect(settings.user_db_path)
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
