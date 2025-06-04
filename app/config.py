import mysql.connector

def get_db_connection():

    try:
        conn = mysql.connector.connect(

            host="localhost",
            user="root",
            passwd="",
            database="p4security"
        )

        print("CONEXÃO COM O BANCO REALIZADA.")

        return conn

    except mysql.connector.Error as err:

        print(f"ERRO, CONEXÃO NÃO REALIZADA: {err}")

        return None

