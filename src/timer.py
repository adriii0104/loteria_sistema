import re
from datetime import datetime, timedelta

loterias = {
    "AnguiladiezAM": "Anguila Mañana 10:00 AM",
    "AnguilaunaPM": "Anguila Medio Día 1:00 PM",
    "AnguilaseisPM": "Anguila Medio Tarde 6:00 PM",
    "AnguilaseisPM": "Anguila Medio Tarde 12:43 PM"
    # ... (las demás loterías con sus respectivas horas de cierre)
}

hora_actual = datetime.now()

for nombre, hora_cierre in loterias.items():
    patron_hora = r'\d{1,2}:\d{2}\s?[APap][Mm]\.?[ ]?[Mm]?'
    resultado = re.search(patron_hora, hora_cierre)

    if resultado:
        hora_cierre_str = resultado.group().strip()
        hora_cierre_dt = datetime.strptime(hora_cierre_str, "%I:%M %p")

        # Asignamos la fecha actual a la hora de cierre
        hora_cierre_dt = hora_cierre_dt.replace(year=hora_actual.year, month=hora_actual.month, day=hora_actual.day)

        # Calculamos la diferencia de tiempo entre la hora de cierre y la hora actual
        diferencia_tiempo = hora_cierre_dt - hora_actual

        # Verificamos si faltan 10 minutos o menos para el cierre de la lotería
        if diferencia_tiempo <= timedelta(minutes=10):
            print(f"La lotería {nombre} cierra en menos de 10 minutos ({hora_cierre_str}). No puedes hacer una jugada.")
        else:
            print(f"La lotería {nombre} aún está abierta. Puedes hacer una jugada.")
