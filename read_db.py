import sqlite3


def read_database():
    c = sqlite3.connect('ram_usage.db')
    cursor = c.cursor()
    cursor.execute('SELECT * FROM ram_usage')
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    c.close()


if __name__ == "__main__":
    read_database()
