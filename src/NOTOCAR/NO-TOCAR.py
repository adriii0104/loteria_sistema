#import mysql.connector
# Reemplaza 'usuario', 'contraseña', 'host' y 'nombre_base_de_datos' con las credenciales correspondientes.
 #Si es necesario, también puedes ajustar el puerto usando 'port'.
#connection = mysql.connector.connect(
#    host="localhost",
#    user="root",
#    password="",
#    database="genuine_services"
#)
# Crea un cursor para interactuar con la base de datos.
#cursor = connection.cursor()
 #Obtiene una lista de todas las tablas en la base de datos.
#cursor.execute("SHOW TABLES")
#tables = [table[0] for table in cursor]
 #Reinicia los valores autoincrementales de cada tabla.
#for table in tables:
   # Desactiva la variable sql_mode 'NO_AUTO_VALUE_ON_ZERO' para permitir reiniciar los valores autoincrementales a 0.
 #   cursor.execute("SET @@SESSION.sql_mode='';")
   
   # Vacía la tabla.
   # cursor.execute(f"TRUNCATE TABLE {table}")
# Reinicia el valor autoincremental a 0.
#    cursor.execute(f"ALTER TABLE {table} AUTO_INCREMENT = 0")
#Realiza el commit para guardar los cambios.
#connection.commit()
#Cierra el cursor y la conexión a la base de datos.
#cursor.close()
#connection.close()

