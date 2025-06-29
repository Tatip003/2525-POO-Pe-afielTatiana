# Programa orientado a objetos para calcular el área de un círculo

import math

class Circulo:
    """Clase que representa un círculo y permite calcular su área"""

    def __init__(self, radio):
        """
        #Método constructor para inicializar el círculo con su radio
        :param radio: float
        """
        self.radio = radio  # Atributo del objeto

    def calcular_area(self):

        return math.pi * self.radio ** 2


# Solicitar el radio al usuario
radio_usuario = float(input("Ingresa el radio del círculo: "))

# Crear objeto de la clase Circulo
mi_circulo = Circulo(radio_usuario)

#Calcular el área usando el método de la clase
area = mi_circulo.calcular_area()

# Mostrar el resultado
print(f"El área del círculo con radio {mi_circulo.radio} es: {area:.2f}")
