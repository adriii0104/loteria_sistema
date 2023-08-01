# Cadena original
cadena = "25 (Palé)"

# Usamos una función de expresiones regulares para extraer los números y el guión "-"
import re
resultado = re.sub(r'[^\d-]', '', cadena)

# Imprimimos el resultado
print(resultado)
