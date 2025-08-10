from typing import List
from jugadores import Jugador


def mostrar_estadisticas(jugadores: List[Jugador]) -> None:
    print("\n=============================== ESTADÍSTICAS ===============================")
    nombres = [jugador.nombre for jugador in jugadores]
    rondas_ganadas = [jugador.rondas_ganadas for jugador in jugadores]
    rondas_perdidas = [jugador.rondas_perdidas for jugador in jugadores]

    for jugador in jugadores:
        print(
            f"{jugador.nombre} ha ganado {jugador.rondas_ganadas} rondas y ha perdido {jugador.rondas_perdidas}."
        )

    try:
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots()
        ax.bar(nombres, rondas_ganadas, label="Rondas Ganadas", color="green")
        ax.bar(
            nombres,
            rondas_perdidas,
            label="Rondas Perdidas",
            color="red",
            bottom=rondas_ganadas,
        )
        ax.set_xlabel("Jugadores")
        ax.set_ylabel("Rondas")
        ax.set_title("Rondas Ganadas y Perdidas por Jugador")
        ax.legend()
        plt.show()
    except Exception as e:
        # En entornos sin backend gráfico, evita romper la ejecución
        print("No fue posible mostrar el gráfico de estadísticas:", e)
