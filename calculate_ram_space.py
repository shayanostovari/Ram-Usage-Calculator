import os
import sqlite3
import time

def get_ram_usage():
    with os.popen('free -m') as r:
        lines = r.readlines()

    total_ram = int(lines[1].split()[1])  # Total RAM in MB
    used_ram = int(lines[1].split()[2])   # Used RAM in MB
    free_ram = int(lines[1].split()[3])   # Free RAM in MB
    return total_ram, used_ram, free_ram

def create_database():
    connection = sqlite3.connect('ram_usage.db')
    c = connection.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS ram_usage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            total INTEGER,
            used INTEGER,
            free INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    connection.commit()
    return connection

def save_to_db(connection, total, used, free):
    c = connection.cursor()
    c.execute('''
        INSERT INTO ram_usage (total, used, free) VALUES (?, ?, ?)
    ''', (total, used, free))  # Store integers directly
    connection.commit()

def main():
    connection = create_database()
    try:
        while True:
            total, used, free = get_ram_usage()
            save_to_db(connection, total, used, free)
            print(f'Total RAM : {total} MB\nUsed RAM : {used} MB\nFree RAM : {free} MB\n')
            time.sleep(60)  # 1 minute
    except KeyboardInterrupt:
        print("Program stopped by user.")
    finally:
        connection.close()

if __name__ == "__main__":
    main()
