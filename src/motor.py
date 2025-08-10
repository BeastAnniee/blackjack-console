import time
from typing import List

from cartas import Baraja
from jugadores import Usuario, JugadorAleatorio, JugadorIA, Crupier, Jugador
from estadisticas import mostrar_estadisticas


class Blackjack:
    def __init__(self, usar_retrasos: bool = True, cartas_minimas: int = 10):
        self.usar_retrasos = usar_retrasos
        self.cartas_minimas = cartas_minimas
        self.baraja = Baraja()
        self.jugador = Usuario("Usuario")
        self.jugador_aleatorio = JugadorAleatorio("Jugador 1")
        self.jugador_IA = JugadorIA("Jugador 2")
        self.crupier = Crupier()

    def _sleep(self, segundos: float) -> None:
        if self.usar_retrasos:
            time.sleep(segundos)

    def verificar_saldos(self) -> bool:
        agotados = []
        if self.jugador.saldo <= 0:
            agotados.append("Usuario")
        if self.jugador_aleatorio.saldo <= 0:
            agotados.append("Jugador 1")
        if self.jugador_IA.saldo <= 0:
            agotados.append("Jugador 2")
        if agotados:
            print("Sin saldo:", ", ".join(agotados), "— fin del juego.")
            return True
        return False

    def mostrar_saldos(self) -> None:
        print("\n=============================== SALDOS ACTUALES ===============================")
        for jugador in [self.jugador, self.jugador_aleatorio, self.jugador_IA]:
            print(f"{jugador.nombre}: {jugador.saldo} fichas.")
        print("=" * 80)

    def iniciar_apuestas(self) -> None:
        print(f"\n{'-'*30} INICIANDO APUESTAS {'-'*30}")
        for jugador in [self.jugador, self.jugador_aleatorio, self.jugador_IA]:
            if isinstance(jugador, Usuario):
                while True:
                    try:
                        apuesta = int(input(f"{jugador.nombre}, ingresa tu apuesta (mín. 5): "))
                        if apuesta >= 5 and jugador.realizar_apuesta(apuesta):
                            break
                        print("Apuesta inválida o saldo insuficiente.")
                    except ValueError:
                        print("Por favor, ingresa un número válido.")
            elif isinstance(jugador, JugadorAleatorio):
                jugador.realizar_apuesta_aleatoria()
            elif isinstance(jugador, JugadorIA):
                jugador.gestionar_apuesta(self.baraja.cartas)

    def verificar_mazo(self) -> None:
        if len(self.baraja.cartas) < self.cartas_minimas:
            print("Se ha alcanzado el mínimo de cartas en la baraja. Mezclando...")
            self.baraja = Baraja()
            self.baraja.mezclar()

    def repartir_inicial(self) -> None:
        self.verificar_mazo()
        for _ in range(2):
            self.jugador.recibir_carta(self.baraja.repartir())
            self.jugador_aleatorio.recibir_carta(self.baraja.repartir())
            self.jugador_IA.recibir_carta(self.baraja.repartir())
            self.crupier.recibir_carta(self.baraja.repartir())
            self._sleep(0.6)

    def mostrar_estado_juego(self, ocultar_crupier: bool = False) -> None:
        print(f"\n{'-'*31} ESTADO DEL JUEGO {'-'*32}")
        self.jugador.mostrar_mano()
        self.jugador_aleatorio.mostrar_mano()
        self.jugador_IA.mostrar_mano()
        self.crupier.mostrar_mano(ocultar_crupier)
        print("-" * 82)
        self._sleep(0.4)

    def _turno_jugador(self, jugador: Jugador, jugadores: List[Jugador]) -> None:
        while True:
            if jugador.calcular_valor_mano() > 21:
                print(f"---> {jugador.nombre} ha perdido.")
                break
            if isinstance(jugador, Usuario):
                decision = jugador.decidir()
            elif isinstance(jugador, JugadorAleatorio):
                decision = jugador.decidir()
            elif isinstance(jugador, JugadorIA):
                decision = jugador.decidir(jugadores, self.crupier, self.baraja.cartas)
            else:
                decision = False
            if not decision:
                break
            jugador.recibir_carta(self.baraja.repartir())
            self.mostrar_estado_juego(ocultar_crupier=True)

    def _turno_crupier(self) -> None:
        print("\nTURNO DEL CRUPIER:")
        self.mostrar_estado_juego(ocultar_crupier=False)
        while self.crupier.decidir():
            self.crupier.recibir_carta(self.baraja.repartir())
            self.mostrar_estado_juego(ocultar_crupier=False)
            self._sleep(0.5)
        self.mostrar_estado_juego()

    def _liquidar_apuestas(self) -> None:
        jugadores = [self.jugador, self.jugador_aleatorio, self.jugador_IA]
        if self.crupier.calcular_valor_mano() > 21:
            for jugador in jugadores:
                if jugador.calcular_valor_mano() <= 21:
                    jugador.ganar_apuesta()
                else:
                    jugador.perder_apuesta()
            return

        crupier_valor = self.crupier.calcular_valor_mano()
        for jugador in jugadores:
            jugador_valor = jugador.calcular_valor_mano()
            if jugador_valor > 21:
                jugador.perder_apuesta()
            elif jugador_valor > crupier_valor:
                jugador.ganar_apuesta()
            elif jugador_valor == crupier_valor:
                jugador.reembolsar_apuesta()
            else:
                jugador.perder_apuesta()

    def reiniciar_manos(self) -> None:
        for jugador in [self.jugador, self.jugador_aleatorio, self.jugador_IA, self.crupier]:
            jugador.mano = []

    def jugar_ronda(self) -> None:
        self.reiniciar_manos()
        self.baraja.mezclar()
        self.mostrar_saldos()
        self.iniciar_apuestas()
        self.repartir_inicial()
        self.mostrar_estado_juego(ocultar_crupier=True)

        jugadores = [self.jugador, self.jugador_aleatorio, self.jugador_IA]
        for jugador in jugadores:
            self._turno_jugador(jugador, jugadores)

        self._turno_crupier()
        self._liquidar_apuestas()

    def iniciar_juego(self) -> None:
        while True:
            if self.verificar_saldos():
                break
            self.jugar_ronda()
            eleccion = input("¿Quieres jugar otra ronda? (s/n): ").strip().lower()
            while eleccion not in ["s", "n"]:
                eleccion = input("Por favor, introduce una opción válida (s/n): ").strip().lower()
            if eleccion != "s":
                break
            self.baraja.mezclar()
        print("¡Gracias por jugar!")
        mostrar_estadisticas([self.jugador, self.jugador_aleatorio, self.jugador_IA])
