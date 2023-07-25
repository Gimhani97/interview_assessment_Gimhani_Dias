import sqlite3

DB_NAME = 'power_data.db'


def create_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE readings (timestamp INTEGER, name TEXT, value REAL)")

    conn.commit()
    conn.close()


def insert_reading(timestamp, name, value):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO readings VALUE (?,?,?)", (timestamp, name, value))
    conn.commit()
    conn.close()


def get_data_to_average_power(from_date, to_date):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT strftime('%Y-%m-%dT%H:%M:%S.000Z', timestamp, 'unixepoch') as time, name, AVG(value) as "
                   "value FROM readings WHERE date(time, 'unixepoch') BETWEEN ? AND ? GROUP BY date(time, "
                   "'unixepoch'), name"), (from_date, to_date)
    result = cursor.fetchall()
    conn.close()

    return result
