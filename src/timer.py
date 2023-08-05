from datetime import datetime, timedelta

# Obtener la hora actual
hora_actual = datetime.now().time()

# Hora dada (puedes cambiar esta hora según tus necesidades)
hora_dada = datetime.strptime("10:04:00", "%H:%M:%S").time()

# Calcular la diferencia entre la hora actual y la hora dada
diferencia = datetime.combine(datetime.today(), hora_actual) - datetime.combine(datetime.today(), hora_dada)

# Obtener el tiempo transcurrido en minutos
minutos_transcurridos = diferencia.total_seconds() / 60

# Comparar si han pasado 15 minutos
if minutos_transcurridos >= 15:
    print("Han pasado 15 minutos desde la hora dada.")
else:
    print("No han pasado 15 minutos desde la hora dada.")