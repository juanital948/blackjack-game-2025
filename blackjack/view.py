from blackjack.model import Blackjack

class Blackjack:
 pass

class ConsolaBlackjack:

    def __init__(self):
     self.blackjack: Blackjack = Blackjack()
     self.opciones = {
         "1": self.iniciar_nuevo_juego,
         "0": self.salir
     }

     @staticmethod
     def mostrar_menu():
         print(f"\n{'BLACK JACK':_^30}")
         print("1. Iniciar nuevo juego")
         print("0. Salir")
         print(f"{'_':-^30}")

     def ejecutar_app(self):
         print("\nBIENVENIDO A UN NUEVO JUEGO DE BLACKJACK")
         self.registrar_usuario()
         while True:
             self.mostrar_menu()
             opcion = input("Seleccione una opción: ")
             accion = self.opciones.get(opcion)
             if accion:
                 accion()
             else:
                 print(f"{opcion} no es una opción válida")

     def registrar_usuario(self):
         nombre: str = input("¿Cuál es tu nombre?: ")
         self.blackjack.registrar_jugador(nombre)

     def iniciar_nuevo_juego(self):
         if not self.blackjack.jugador.tiene_fichas():
             print("¡LO SENTIMOS! NO TIENES FICHAS PARA JUGAR")
             return

         apuesta: int = self.recibir_apuesta_jugador()
         self.blackjack.iniciar_juego(apuesta)
         self.mostrar_manos(self.blackjack.cupier.mano, self.blackjack.jugador.mano)

         if not self.blackjack.jugador.mano.es_blackjack():
             self.hacer_jugada_de_jugador()
         else:
             self.finalizar.juego()

        def hacer_jugada_del_jugador(self):
            while not self.blackjack.jugador.mano.calcular_valor() > 21:
                respuesta = input("¿Deseas otra carta? (s/n): ")
                if respuesta == "s":
                    self.blackjack.repartir_carta_a_jugador()
                    self.mostrar_manos(self.blackjack.cupier.mano, self.blackjack.jugador.mano)
                elif respuesta == "n":
                    break

            if self.blackjack.jugador.mano.calcular_valor() > 21:
                self.finalizar_juego()

            else:
                self.hacer_jugada_de_la_casa()

        def hacer_jugada_de_la_casa(self):
            print("\nAHORA ES EL TURNO DE LA CASA\n")
            self.blackjack.destapar_mano_de_la_casa()
            self.mostrar_manos(self.blackjack.cupier.mano, self)

         def mostrar_manos(self, mano_casa, mano_jugador):
             print(f"\n{'MANO DE LA CASA': <15}\n{str(mano_casa):<15}")
             print(f"\n{'TU MANO':<15}\n{str(mano_jugador):<15}")
             print(f"{'VALOR: ' + str(mano_casa.calcular_valor()):15}")
             print(f"{'VALOR: ' + str(mano_jugador.calcular_valor()):15}")

     def recibir_apuesta_jugador(self):
         while True:
             apuesta = input("¿Cuántas fichas deseas apostar?: ")
             if apuesta.isdigit():
                 apuesta = int(apuesta)
                 if self.blackjack.jugador.tiene_fichas(apuesta):
                     return apuesta
                 else:
                     print("No tienes suficientes fichas para realizar apuesta")
             else:
                 print("Ingrese un valor numerico")

     @staticmethod
     def salir():
         print("¡GRACIAS POR JUGAR BLACKJACK!")
         exit(0)


