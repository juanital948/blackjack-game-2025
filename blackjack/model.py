import random
from dataclasses import dataclass, field
from typing import ClassVar

import self

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

    def __str__(self) -> str:
    if self.oculta:
        return OCULTA
    else:
        return f"{self.valor}"


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

    def limpiar(self):
        self.cartas.clear()

    def __str__(self) -> str:
        str_mano = ""
        for carta in self.cartas:
            str_mano += f"{str(carta):^5}"
        return str_mano


@dataclass
class Casa:
    mano: Mano = field(init=False, default=None)

    def inicializar_mano(self, cartas: list[Carta]):
        self.mano = Mano(cartas)

    def recibir_carta(self, carta: Carta):
        self.mano.agregar_carta(carta)

@dataclass
class Jugador:
    nombre: str
    fichas: int = field(init=False, default=100)
    mano: Mano = field(init=False, default=None)

    def inicializar_mano(self, cartas: list[Carta]):
        self.mano = Mano(cartas)

    def recibir_carta(self, carta: Carta):
        self.mano.agregar_carta(carta)

    def agregar_fichas(self, fichas: int):
        self.fichas += fichas

    def tiene_fichas(self, apuesta: int = 1) -> bool:
        return self.fichas >= apuesta


class Blackjack:

    def __init__(self):
        self.apuesta_inicial: int = 0
        self.cupier: Casa = Casa()
        self.jugador: Jugador | None = None
        self.baraja: Baraja = Baraja()

    def registrar_jugador(self, nombre: str):
        self.jugador = Jugador(nombre)

    def iniciar_juego(self, apuesta: int):
        self.apuesta_inicial = apuesta
        if self.jugador.mano:
            self.jugador.mano.limpiar()
        if self.cupier.mano:
            self.cupier.mano.limpiar()
        self.baraja.reiniciar()
        self.baraja.revolver()

    # Repartir mano del jugador
        cartas_jugador: list[Carta] =  [self.baraja.repartir_carta(), self.baraja.repartir_carta()]
        self.jugador.inicializar_mano(cartas_jugador)

    # Repartir mano de la casa
        cartas_cupier: list[Carta] = [self.baraja.repartir_carta(), self.baraja.repartir_carta(oculta=True)]
        self.cupier.inicializar_mano(cartas_cupier)

    def repartir_carta_a_jugador(self):
        self.jugador.recibir_carta(self.baraja.repartir_carta())

    def destapar_mano_de_la_casa(self):
        self.cupier.mano.destapar()

    def casa_puede_pedir(self)-> bool:
        valor_mano_casa = self.cupier.mano.calcular_valor()
        valor_mano_jugador = self.jugador.mano.calcular_valor()
        return valor_mano_casa <= valor_mano_jugador and valor_mano_casa <= 16

    def finalizar_juego(self):
        if self.jugador_gano():
            self.jugador.agregar_fichas(self.apuesta_inicial)

        elif self.casa_gano():
            self.jugador.agregar_fichas(-self.apuesta_inicial)

        self.apuesta_inicial = 0

    def jugador_gano(self) -> bool:
        valor_mano_casa = self.cupier.mano.calcular_valor()
        valor_mano_jugador = self.jugador.mano.calcular_valor()
        return self.jugador.mano.es_blackjack() or (valor_mano_casa < valor_mano_jugador <= 21)

    def casa_gano(self) -> bool:
        valor_mano_casa = self.cupier.mano.calcular_valor()
        valor_mano_jugador = self.jugador.mano.calcular_valor()
        return (not self.jugador.mano.es_blackjack()) and (valor_mano_jugador < valor_mano_casa <= 21)

    def hay_empate(self) -> bool:
        valor_mano_casa = self.cupier.mano.calcular_valor()
        valor_mano_jugador = self.jugador.mano.calcular_valor()
        return not self.jugador.mano.es_blackjack() and valor_mano_casa == valor_mano_jugador