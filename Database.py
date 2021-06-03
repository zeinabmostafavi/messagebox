from datetime import datetime
from os import name
from sqlite3 import connect
from typing import Text
from time import time


class Database:

    @staticmethod
    def insert(name, text):
        try:
            my_con = connect('messages.db')
            my_cursor = my_con.cursor()

            time = datetime.now()
            time = time.strftime("%Y-%m-%d %H:%M")
            my_cursor.execute(
                f"INSERT INTO messages(name, text,time) VALUES('{name}','{text}', '{time}')")
            my_con.commit()
            my_con.close()
            return True
        except Exception as e:
            print("error:", e)
            return False

    @staticmethod
    def select():
        try:
            my_con = connect('messages.db')
            my_cursor = my_con.cursor()
            my_cursor.execute("SELECT * FROM messages")
            result = my_cursor.fetchall()
            my_con.close()
            return result
        except Exception as e:
            print("error:", e)
            return []

    @staticmethod
    def delete(id):
        try:
            my_con = connect('messages.db')
            my_cursor = my_con.cursor()
            my_cursor.execute(f"DELETE FROM messages WHERE ID ='{id}'")
            my_con.commit()
            my_con.close()
            return True
        except Exception as e:
            print("error=:", e)
            return False

    @staticmethod
    def deleteall():
        try:
            my_con = connect('messages.db')
            my_cursor = my_con.cursor()
            my_cursor.execute(f"DELETE FROM messages")
            my_con.commit()
            my_con.close()
            return True

        except Exception as e:
            print("error:", e)
            return False
