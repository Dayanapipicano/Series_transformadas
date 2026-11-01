
import numpy as np

# Periodo de las señales
T = 2 * np.pi


# Generación de la señal cuadrada
def generar_senal_cuadrada(t):
    fase = np.mod(t + np.pi, T) - np.pi
    x = np.where(fase < 0, -1, 1)
    return x


# Generación de la señal triangular
def generar_senal_triangular(t):
    fase = np.mod(t + np.pi, T) - np.pi
    x = 1 - (2 * np.abs(fase) / np.pi)
    return x


# Generación de la señal diente de sierra
def generar_senal_diente_sierra(t):
    fase = np.mod(t + np.pi, T) - np.pi
    x = fase / np.pi
    return x
