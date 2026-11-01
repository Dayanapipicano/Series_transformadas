
import numpy as np
from senales import T


# ==========================================
# RECONSTRUCCIÓN MEDIANTE SERIES DE FOURIER
# ==========================================

def reconstruir_senal(t, N, tipo_senal):

    # Inicializar la señal reconstruida
    x_reconstruida = np.zeros(len(t))

    # Reconstrucción de la señal cuadrada
    if tipo_senal == "Cuadrada":

        for n in range(1, N + 1, 2):
            x_reconstruida += (4 / np.pi) * (np.sin(n * t) / n)

    # Reconstrucción de la señal triangular
    elif tipo_senal == "Triangular":

        for n in range(1, N + 1, 2):
            x_reconstruida += (8 / np.pi**2) * (np.cos(n * t) / n**2)

    # Reconstrucción de la señal diente de sierra
    elif tipo_senal == "Diente de sierra":

        for n in range(1, N + 1):
            x_reconstruida += (
                (2 / np.pi) *
                ((-1)**(n + 1)) *
                (np.sin(n * t) / n)
            )

    return x_reconstruida


# ==========================================
# CÁLCULO DEL ESPECTRO DE LÍNEA
# ==========================================

def calcular_espectro(N, tipo_senal):

    frecuencias = []
    amplitudes = []

    frecuencia_fundamental = 1 / T

    for n in range(1, N + 1):

        # Coeficientes inicializados
        an = 0
        bn = 0

        if tipo_senal == "Cuadrada":

            if n % 2 != 0:
                bn = 4 / (n * np.pi)

        elif tipo_senal == "Triangular":

            if n % 2 != 0:
                an = 8 / (n**2 * np.pi**2)

        elif tipo_senal == "Diente de sierra":

            bn = (2 * (-1)**(n + 1)) / (n * np.pi)

        # Amplitud del armónico
        amplitud = np.sqrt(an**2 + bn**2)

        # Frecuencia del armónico
        frecuencia = n * frecuencia_fundamental

        if amplitud != 0:
            frecuencias.append(frecuencia)
            amplitudes.append(amplitud)

    return frecuencias, amplitudes
