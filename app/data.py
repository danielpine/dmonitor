import sqlite3
from enum import Enum
from app.pysqltemplate import PySqlTemplate, DataSource, DBTypes


class MonProcessState(Enum):
    OFF = 0
    ON = 1


db = 'test.db'

# TABLE record
create_record_sql = '''
    CREATE TABLE IF NOT EXISTS record 
    (timestamp NUMBER, 
    pid NUMBER, 
    pname TEXT, 
    memres NUMBER,
    cpuused NUMBER
    );'''

# TABLE monprocess
create_monprocess_sql = '''
    CREATE TABLE IF NOT EXISTS monprocess 
    (
    id TEXT, 
    state NUMBER, 
    key TEXT,
    type TEXT, 
    timestamp NUMBER
    );'''

PySqlTemplate.set_data_source(
    DataSource(
        dbType=DBTypes.Sqlite3,
        db=db))


def create_tables():
    execute(db, create_record_sql)
    execute(db, create_monprocess_sql)


def execute(db, sql):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    close_resource(cur, conn)


def insert_many(db, sql, data):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.executemany(sql, data)
    conn.commit()
    close_resource(cur, conn)


def insert_many_to_record(data):
    insert_many(db, 'INSERT INTO record VALUES (?,?,?,?,?)', data)


def insert_many_to_monprocess(data):
    insert_many(db, 'INSERT INTO monprocess VALUES (?,?,?,?,?)', data)


def select_process_from_record_by_key_words(key_words):
    return PySqlTemplate.statement(
        'select DISTINCT pname from record where pname LIKE ?'
    ).params(key_words).list_all()


def select_all_monprocess():
    return PySqlTemplate.statement('select * from monprocess').list_json()


def select_from_record(start, end):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(
        "select * from record where timestamp between ? and ? order by timestamp", (start, end))
    return cur.fetchall()


def select_from_record_filter(start, end, processfilter):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(
        "select * from record where pname=? and timestamp between ? and ? order by timestamp", (processfilter, start, end))
    return cur.fetchall()


def close_resource(cur, conn):
    cur.close()
    conn.close()


if __name__ == "__main__":
    # print(select_from_record(1601221267, 1601221767))
    print(select_all_monprocess())
