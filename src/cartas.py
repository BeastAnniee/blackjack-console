import random as rd
from dataclasses import dataclass
from typing import List

PALOS = ("Corazones", "Diamantes", "Tréboles", "Picas")
VALORES = ("2","3","4","5","6","7","8","9","10","J","Q","K","A")


@dataclass(frozen=True)
class Carta:
    valor: str
    palo: str

    def __str__(self) -> str:
        return f"{self.valor} de {self.palo}"


class Baraja:
    def __init__(self) -> None:
        self.cartas: List[Carta] = self._crear_baraja()
        self.mezclar()

    def _crear_baraja(self) -> List[Carta]:
        return [Carta(valor, palo) for palo in PALOS for valor in VALORES]

    def mezclar(self) -> None:
        rd.shuffle(self.cartas)

    def repartir(self) -> Carta:
        if not self.cartas:
            # Baraja agotada: regenerar y mezclar
            self.cartas = self._crear_baraja()
            self.mezclar()
        return self.cartas.pop()

    def cartas_restantes(self) -> int:
        return len(self.cartas)
