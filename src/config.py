import mysql.connector



def connection_intent():
    try:
        conexion = mysql.connector.connect(
            host='190.166.27.19',
            user='root',
            password='ACD20803@',
            db='lotteria_genuine'
        )
        conexion2 = mysql.connector.connect(
            host='190.166.27.19',
            user='root',
            password='ACD20803@',
            db='resultados'
        )
    
        if conexion.is_connected() and conexion2.is_connected():
            conection = True

            return conexion, conexion2
        else:
            conection = None
            return conection
    
    except mysql.connector.Error as e:
        #print("Error al conectarse con la base de datos:", e)
        conection = None
        return conection
    
