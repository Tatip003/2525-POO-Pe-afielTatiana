class Calculadora:
    def __init__(self):
        """
        Constructor: se ejecuta automáticamente al crear una nueva instancia.
        Aquí se pueden inicializar atributos si fueran necesarios.
        """
        print("✅ Calculadora creada. Lista para operar.")

    def sumar(self, a, b):
        #Suma dos números y devuelve el resultado.
        return a + b

    def restar(self, a, b):
        #Resta el segundo número del primero.
        return a - b

    def multiplicar(self, a, b):
       #Multiplica dos números.
        return a * b

    def dividir(self, a, b):
        #Divide el primer número por el segundo (si no es cero).
        if b != 0:
            return a / b
        else:
            return " Error: División por cero."

    def __del__(self):
        """
        Destructor: se ejecuta automáticamente cuando el objeto ya no se usa o se elimina con 'del'.
        Aquí podemos hacer limpieza, cerrar recursos, o simplemente mostrar un mensaje.
        """
        print("🗑️ Calculadora destruida. Gracias por usarla.")


# ------------ Uso del programa ------------

# Se crea una instancia de la clase Calculadora
calc = Calculadora()  # Aquí se activa __init__

# Se hacen algunas operaciones
print("Suma:        ", calc.sumar(10, 5))
print("Resta:       ", calc.restar(10, 5))
print("Multiplicación:", calc.multiplicar(10, 5))
print("División:    ", calc.dividir(10, 5))
print("División por cero:", calc.dividir(10, 0))

# Se destruye el objeto (también se destruirá automáticamente al finalizar el programa)
del calc  # Aquí se activa __del__
