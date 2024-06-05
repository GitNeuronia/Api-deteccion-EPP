import psycopg2


class ConnData:
    ENGINE= 'django.db.backends.postgresql_psycopg2'
    NAME= 'EPP_PRODUCCION'
    USER= 'admin'
    PASSWORD= 'admin'
    HOST= 'localhost'
    PORT= '5432'

def doexecute(sql_query):
    try:
        conn=connect()
        cursor=conn[0]
        cursor.execute(sql_query,)
        conn[1].commit()
        return True
        
    except Exception as e:
        print(str(e))
        return None

def connect():
    try:
        conndata=ConnData()
        conn = psycopg2.connect(
            dbname=conndata.NAME,
            user=conndata.USER,
            password=conndata.PASSWORD,
            host=conndata.HOST,
            port=conndata.PORT
        )
        return conn.cursor(),conn
    except Exception as e:
        print(str(e))
        return None,None