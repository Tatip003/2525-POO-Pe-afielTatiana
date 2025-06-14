# Clase base que representa la información del clima de un día
class TemperatureDay:
    def __init__(self, day, temp_mini, temp_maxi, unidad="C"):
        self.day = day  # Día de la semana
        self.__temperatura_minima = temp_mini  # Atributo privado
        self.__temperatura_maxima = temp_maxi  # Atributo privado
        self.unidad = unidad  # Unidad de temperatura (por defecto Celsius)

    # Método para calcular la temperatura promedio del día
    def temperatura_promedio(self):
        return (self.__temperatura_minima + self.__temperatura_maxima) / 2

    # Método para mostrar la temperatura promedio del día
    def mostrar_info(self):
        print(f"{self.day}: {self.temperatura_promedio():.2f}°{self.unidad.upper()}")

# Clase hija que hereda de TemperatureDay
# Añade una evaluación cualitativa del clima (caluroso, templado, frío)
class TemperatureDayExtended(TemperatureDay):
    def clasificar_clima(self):
        promedio = self.temperatura_promedio()
        if promedio >= 35:
            return " Caluroso"
        elif promedio >= 25:
            return " Templado"
        else:
            return " Frío"

    # Sobrescribimos el método mostrar_info (Polimorfismo)
    def mostrar_info(self):
        # Mostramos además del promedio, la categoría del clima
        print(f"{self.day}: {self.temperatura_promedio():.2f}°{self.unidad.upper()} - {self.clasificar_clima()}")

# Lista de objetos (usando la clase hija) con datos de temperatura de Guayaquil - Semana 1
dias = [
    TemperatureDayExtended("Lunes", 34, 34),
    TemperatureDayExtended("Martes", 30, 30),
    TemperatureDayExtended("Miércoles", 25, 25),
    TemperatureDayExtended("Jueves", 39, 39),
    TemperatureDayExtended("Viernes", 25, 25),
    TemperatureDayExtended("Sábado", 38, 38),
    TemperatureDayExtended("Domingo", 22, 22)
]

# Mostrar la información diaria con la clasificación del clima
print("🌤 Temperatura promedio diaria con clasificación:")
for dia in dias:
    dia.mostrar_info()

# Calcular el promedio semanal
total_promedios = sum(dia.temperatura_promedio() for dia in dias)
promedio_semanal = total_promedios / len(dias)

print(f"\n Promedio semanal: {promedio_semanal:.2f}°C")

