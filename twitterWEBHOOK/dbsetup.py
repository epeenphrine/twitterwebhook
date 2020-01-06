import mysql.connector as mysql
import sqlite3
import config ## db info should be here


try: ## try connecting to mysql first
    conn = mysql.connect(
        host = config.host,
        user = config.user,
        passwd = config.passwd,
        port = config.port
    )
    print(conn)
except:
    conn = sqlite3.connect("twitterDB.db")
    print(conn)

def url_parse(urls):
    urls_split = []
    for url in urls:
        print(url)
        split_ = url.split("/")
        split_.remove("")
        print(split_)
        urls_split.append(split_)
    print(urls_split)
    return urls_split

def db_check():
    c = conn.cursor()
    db_type = str(type(conn)).lower()
    print(type(db_type))
    if "mysql" in db_type:
        print("MySQL being used")
        print(conn)
        c.execute("show databases")
        databases = c.fetchall()
        print(databases)
        database = config.database
        print(database)
        return MySQL_db(database, c)

    elif "sqlite3" in db_type:
        print("SQLite3 being used")
        print("\n\n")
        return SQLite_db(c, conn)
    else:
        print("no connection to either databases")

##check if database present in MySQLdatabases
def MySQL_db(database, c):
    print("\n\nin mysql_db function")
    c.execute(f"SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = '{database}'") ## checking if database exists
    print(f"database {database} present")
    db = c.fetchall()
    tables = url_parse(config.twitter_url)
    if db:
        print("\n\ngoing to table check")
        c.execute("use twitterDB")
        c.execute("show tables")
        print(f"showing all tables {c.fetchall()}")
        for table in tables:
            print(table)
            table_ = table[2]
            c.execute(f"SELECT * FROM information_schema.tables WHERE table_schema = '{database}' and table_name = '{table_}'") ## check if tables exist
            table_check = c.fetchall()
            print(f"\n\n{table_check}")
            if not table_check:
                print(f"adding {table_}")
                c.execute(f"CREATE TABLE {table_} (url text, tweet text, entry_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")  ## table schema
                c.execute("show tables")
                print(c.fetchall())
            else:
                print(f"{table_} table present")
    else:
        print(f"database {database} not present")
        print(f"creating {database}")
        c.execute(f"CREATE DATABASE {database}")
        c.execute(f"SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = '{database}'")  ## checking if database exists
        db = c.fetchall()
        if db:
            print("\n\ngoing to table check")
            c.execute("use twitterDB")
            c.execute("show tables")
            print(f"showing all tables {c.fetchall()}")
            for table in tables:
                table_ = table[2]
                c.execute(
                    f"SELECT * FROM information_schema.tables WHERE table_schema = '{database}' and table_name = '{table_}'")  ## check if tables exist
                table_check = c.fetchall()
                print(f"\n\n{table_check}")
                if not table_check:
                    print(f"adding {table_}")
                    c.execute(
                        f"CREATE TABLE {table_} (url text, tweet text, entry_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")  ## table schema
                    c.execute("show tables")
                    print(c.fetchall())
                else:
                    print(f"{table_} table present")
    print("\n\nclosing connection")
    conn.close

def SQLite_db(c, conn):
    tables = url_parse(config.twitter_url)
    for table in tables:
        table_ = table[2]
        print(f"\nchecking if table : {table_} in database")
        query_table_check = c.execute(f"SELECT name FROM sqlite_master where type = 'table' AND name = '{table_}'").fetchall()
        if query_table_check:
            print(query_table_check)
            print("table present")
        else:
            print(f"creating new table for : {table_}")
            c.execute(f"""CREATE TABLE {table_}(
                        url text,
                        tweet text,
                        entry_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP                    
                        )""")
            conn.commit()
