import random as rd
from typing import List, Optional
from dataclasses import dataclass, field

from cartas import Carta


@dataclass
class Jugador:
    nombre: str
    saldo: float = 100
    mano: List[Carta] = field(default_factory=list)
    apuesta: float = 0
    rondas_ganadas: int = 0
    rondas_perdidas: int = 0

    def realizar_apuesta(self, cantidad: float) -> bool:
        if cantidad > self.saldo or cantidad <= 0:
            print(f"{self.nombre} no tiene suficiente saldo para apostar {cantidad}.")
            return False
        self.apuesta = cantidad
        self.saldo -= cantidad
        print(f"{self.nombre} ha apostado {cantidad}.")
        return True

    def ganar_apuesta(self) -> None:
        premio = self.apuesta * 2
        self.saldo += premio
        self.rondas_ganadas += 1
        print(f"{self.nombre} ha ganado {premio}. Saldo actual: {self.saldo}")

    def perder_apuesta(self) -> None:
        self.rondas_perdidas += 1
        print(f"{self.nombre} ha perdido {self.apuesta}. Saldo actual: {self.saldo}")

    def reembolsar_apuesta(self) -> None:
        self.saldo += self.apuesta
        print(f"{self.nombre} ha recuperado su apuesta. Saldo actual: {self.saldo}")

    def recibir_carta(self, carta: Optional[Carta]) -> None:
        if carta is not None:
            self.mano.append(carta)

    def calcular_valor_mano(self, mano: Optional[List[Carta]] = None) -> int:
        if mano is None:
            mano = self.mano
        valor = 0
        ases = 0
        for carta in mano:
            if carta is None:
                continue
            if carta.valor in ["J", "Q", "K"]:
                valor += 10
            elif carta.valor == "A":
                ases += 1
                valor += 11
            else:
                valor += int(carta.valor)
        while valor > 21 and ases:
            valor -= 10
            ases -= 1
        return valor

    def mostrar_mano(self, oculta: bool = False) -> None:
        if oculta and self.mano:
            print(f"{self.nombre} tiene {self.mano[0]} y una carta oculta.")
        else:
            cartas = ", ".join(map(str, self.mano)) if self.mano else "(sin cartas)"
            valor_mano = self.calcular_valor_mano()
            print(f"{self.nombre} tiene {cartas}")
            print(f"-->Valor de la mano: {valor_mano}\n")

    def decidir(self, *args, **kwargs) -> bool:
        # Debe ser implementado por subclases cuando aplique
        return False


class Usuario(Jugador):
    def decidir(self, *_, **__) -> bool:
        while True:
            eleccion = input("¿Quieres otra carta? (s/n): ").strip().lower()
            if eleccion in ["s", "n"]:
                return eleccion == "s"
            print("Por favor, introduce una opción válida.")


class JugadorAleatorio(Jugador):
    def decidir(self, *_, **__) -> bool:
        return rd.choice([True, False])

    def realizar_apuesta_aleatoria(self) -> None:
        cantidad = rd.randint(5, max(5, int(min(20, self.saldo))))
        self.realizar_apuesta(cantidad)


class JugadorIA(Jugador):
    def __init__(self, nombre: str):
        super().__init__(nombre)
        self.conteo_cartas = 0

    def actualizar_conteo(self, carta: Carta) -> None:
        # Sistema Hi-Lo
        if carta.valor in ["10", "J", "Q", "K", "A"]:
            self.conteo_cartas -= 1
        elif carta.valor in ["2", "3", "4", "5", "6"]:
            self.conteo_cartas += 1

    def calcular_probabilidad_ganar(self, mano: List[Carta], carta_visible_crupier: Carta, baraja_restante: List[Carta], crupier_ref) -> float:
        N = 600  # reducción para velocidad manteniendo calidad
        victorias = 0
        for _ in range(N):
            baraja_simulada = baraja_restante[:]
            rd.shuffle(baraja_simulada)
            mano_simulada = mano[:]
            # Estrategia básica: pedir hasta 17
            while self.calcular_valor_mano(mano_simulada) < 17 and baraja_simulada:
                mano_simulada.append(baraja_simulada.pop())

            valor_jugador = self.calcular_valor_mano(mano_simulada)
            if valor_jugador > 21:
                continue

            mano_crupier = [carta_visible_crupier]
            while crupier_ref.calcular_valor_mano(mano_crupier) < 17 and baraja_simulada:
                mano_crupier.append(baraja_simulada.pop())

            valor_crupier = crupier_ref.calcular_valor_mano(mano_crupier)
            if valor_crupier > 21 or valor_jugador > valor_crupier:
                victorias += 1

        return victorias / N if N else 0.0

    def decidir(self, jugadores: List[Jugador], crupier_ref, baraja_restante: List[Carta]) -> bool:
        # Actualizar conteo con cartas visibles
        for jugador in jugadores:
            for carta in jugador.mano:
                self.actualizar_conteo(carta)
        for carta in crupier_ref.mano:
            self.actualizar_conteo(carta)

        valor_mano = self.calcular_valor_mano()
        if valor_mano < 12:
            return True

        carta_visible_crupier = crupier_ref.mano[0]
        prob = self.calcular_probabilidad_ganar(self.mano, carta_visible_crupier, baraja_restante, crupier_ref)
        return prob < 0.6

    def gestionar_apuesta(self, baraja_restante: List[Carta]) -> None:
        true_count = self.conteo_cartas / (len(baraja_restante) / 52) if baraja_restante else 0
        if true_count <= 0:
            apuesta = min(10, self.saldo)
        elif true_count <= 2:
            apuesta = min(self.saldo * 0.1, self.saldo)
        else:
            apuesta = min(self.saldo * 0.25, self.saldo)
        self.realizar_apuesta(apuesta)


class Crupier(Jugador):
    def __init__(self):
        super().__init__("Crupier")

    def decidir(self, *_, **__) -> bool:
        return self.calcular_valor_mano() < 17
