
import numpy as np



# CÁLCULO DE MÉTRICAS


def calcular_metricas(x, x_reconstruida):

    # Error medio cuadrático con raíz (RMSE)
    error_rmse = np.sqrt(
        np.mean((x - x_reconstruida)**2)
    )

    # Potencia de la señal original
    potencia_original = np.mean(x**2)

    # Potencia de la señal reconstruida
    potencia_reconstruida = np.mean(x_reconstruida**2)

    return error_rmse, potencia_original, potencia_reconstruida
