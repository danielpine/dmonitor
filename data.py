import sqlite3
from pysqltemplate import PySqlTemplate, DataSource, DBTypes

db = 'test.db'


def create_table_record():
    record_create_sql = '''CREATE TABLE IF NOT EXISTS record 
           (timestamp NUMBER, 
            pid NUMBER, 
            pname TEXT, 
            memres NUMBER,
            cpuused NUMBER
            );'''
    execute(db, record_create_sql)


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


def select_process_from_record_by_key_words(key_words):
    PySqlTemplate.set_data_source(
        DataSource(
            dbType=DBTypes.Sqlite3,
            db=db))
    return PySqlTemplate.statement(
        'select DISTINCT pname from record where pname LIKE ?'
    ).params(key_words).list_all()


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
    print(select_from_record(1601221267, 1601221767))
