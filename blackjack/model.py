import random
from dataclasses import dataclass
from typing import ClassVar

CORAZON = "\u2764\uFE0F"
TREBOL = "\u2663\uFE0F"
DIAMANTE = "\u2666\uFE0F"
ESPADA = "\u2660\uFE0F"
OCULTA = "\u25AE\uFE0F"


@dataclass
class Carta:
    VALORES: ClassVar[list[str]] = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    PINTAS: ClassVar[list[str]] = [CORAZON, TREBOL, DIAMANTE, ESPADA]
    pinta: str
    valor: str
    oculta: bool = False

    def ocultar(self):
        self.oculta = True

    def destapar(self):
        self.oculta = False

    def calcular_valor(self, as_como_11=False) -> int:
        if self.valor == "A":
            return 11 if as_como_11 else 1
        elif self.valor in ["J", "Q", "K"]:
            return 10
        else:
            return int(self.valor)


class Baraja:

    def __init__(self):
        self.cartas: list[Carta] = []
        self.reiniciar()

    def reiniciar(self):
        self.cartas.clear()
        for pinta in Carta.PINTAS:
            for valor in Carta.VALORES:
                self.cartas.append(Carta(pinta, valor))

    def revolver(self):
        random.shuffle(self.cartas)

    def repartir_carta(self, oculta: bool = False) -> Carta | None:
        if len(self.cartas) > 0:
            carta = self.cartas.pop()
            if oculta:
                carta.ocultar()
            return carta
        else:
            return None


class Mano:

    def __init__(self, cartas: list[Carta]):
        self.cartas: list[Carta] = []
        self.cantidad_ases: int = 0
        for carta in cartas:
            self.agregar_carta(carta)

    def es_blackjack(self) -> bool:
        if len(self.cartas) > 2:
            return False

        return self.cartas[0].valor == "A" and self.cartas[1].valor in ["10", "J", "Q", "K"] or \
            self.cartas[1].valor == "A" and self.cartas[0].valor in ["10", "J", "Q", "K"]

    def agregar_carta(self, carta: Carta):
        if carta.valor == "A":
            self.cartas.append(carta)
            self.cantidad_ases += 1
        else:
            self.cartas.insert(0, carta)

    def calcular_valor(self) -> int | str:
        for carta in self.cartas:
            if carta.oculta:
                return "--"

        valor_mano: int = 0

        for carta in self.cartas[:-self.cantidad_ases]:
            valor_mano += carta.calcular_valor()

        for carta in self.cartas[-self.cantidad_ases:]:
            as_como_11 = valor_mano < 11
            valor_mano += carta.calcular_valor(as_como_11)

        return valor_mano

    def destapar(self):
        for carta in self.cartas:
            carta.destapar()