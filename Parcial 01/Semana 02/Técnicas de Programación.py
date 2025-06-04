import random
import time

class Personaje:
    def __init__(self, nombre, velocidad, vida):
        self.nombre = nombre
        self.posicion = 0
        self.velocidad = velocidad
        self.vida = vida

    def avanzar(self):
        self.posicion += self.velocidad
        print(f"{self.nombre} avanza a la posición {self.posicion}.")

    def recibir_daño(self, daño):
        self.vida -= daño
        print(f"{self.nombre} ha recibido {daño} de daño. Vida restante: {self.vida}")

    def esta_vivo(self):
        return self.vida > 0

class Obstaculo:
    def __init__(self, posicion, daño):
        self.posicion = posicion
        self.daño = daño

class Carrera:
    def __init__(self, longitud, personajes):
        self.longitud = longitud
        self.personajes = personajes
        self.obstaculos = self.generar_obstaculos()

    def generar_obstaculos(self):
        obstaculos = []
        for _ in range(self.longitud // 5):  # Cada 5 casillas hay una probabilidad
            pos = random.randint(5, self.longitud - 5)
            daño = random.randint(5, 20)
            obstaculos.append(Obstaculo(pos, daño))
        return obstaculos

    def verificar_obstaculos(self, personaje):
        for obstaculo in self.obstaculos:
            if personaje.posicion >= obstaculo.posicion and personaje.esta_vivo():
                personaje.recibir_daño(obstaculo.daño)
                self.obstaculos.remove(obstaculo)

    def jugar(self):
        turno = 0
        #Ciclo de turnos con while
        while all(p.esta_vivo() and p.posicion < self.longitud for p in self.personajes):
            print(f"\nTurno {turno}")
            for p in self.personajes:
                p.avanzar()
                self.verificar_obstaculos(p)
                #Condicionales para decidir quién gana o si un personaje muere
                if not p.esta_vivo():
                    print(f"{p.nombre} ha sido eliminado.")
            turno += 1
            time.sleep(1)

        vivos = [p for p in self.personajes if p.esta_vivo()]
        if len(vivos) == 1:
            print(f"\n¡{vivos[0].nombre} ha ganado la carrera!")
        elif len(vivos) == 2:
            #Lambda para encontrar al personaje que más ha avanzado:
            ganador = max(vivos, key=lambda p: p.posicion)
            print(f"\n¡{ganador.nombre} ha ganado la carrera por llegar más lejos!")
        else:
            print("\n¡Todos han sido eliminados!")

# Crear personajes
jugador1 = Personaje("Dash", velocidad=3, vida=50)
jugador2 = Personaje("Nick", velocidad=4, vida=40)

# Crear carrera
carrera = Carrera(longitud=30, personajes=[jugador1, jugador2])

# Iniciar juego
carrera.jugar()
