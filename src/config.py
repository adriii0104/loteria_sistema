import mysql.connector



def connection_intent():
    try:
        conexion = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            db='lotteria_genuine'
        )
        conexion = conexion
        conexion2 = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            db='resultados'
        )
        conexion2 = conexion2
    
        if conexion.is_connected() and conexion2.is_connected():
            conection = True

            return conexion, conexion2
            return conection
        else:
            conection = None
            return conection
    
    except mysql.connector.Error as e:
        #print("Error al conectarse con la base de datos:", e)
        conection = None
        return conection
    
