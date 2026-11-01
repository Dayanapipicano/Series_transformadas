import tkinter as tk
from tkinter import ttk, messagebox

import numpy as np

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from senales import (
    generar_senal_cuadrada,
    generar_senal_triangular,
    generar_senal_diente_sierra
)

from fourier import reconstruir_senal, calcular_espectro

from metricas import calcular_metricas


def iniciar_aplicacion():

    
    # 2. VENTANA PRINCIPAL
    

    # Configurar la ventana principal de la aplicación
    ventana = tk.Tk()
    ventana.title("Reconstrucción de señales - Series de Fourier")
    ventana.geometry("1100x750")
    ventana.minsize(900, 650)


   
    # 3. TÍTULO
   

    titulo = ttk.Label(
       ventana,
       text="RECONSTRUCCIÓN DE SEÑALES MEDIANTE SERIES DE FOURIER",
       font=("Arial", 16, "bold")
    )
    titulo.pack(pady=15)


   
    # 4. CONFIGURACIÓN DE PARÁMETROS
  

    # Crear el contenedor para los controles de configuración
    marco_parametros = ttk.LabelFrame(
       ventana,
       text="Configuración de la simulación",
       padding=12
    )
    marco_parametros.pack(fill="x", padx=20, pady=10)
      # Dar prioridad de espacio a la columna donde se muestran las métricas
    marco_parametros.columnconfigure(4, weight=1)


    # Selección de señal
    ttk.Label(
       marco_parametros,
       text="Seleccionar señal:"
    ).grid(row=0, column=0, padx=10, pady=8)

    # StringVar permite vincular una variable de Python con el selector de señales
    senal_seleccionada = tk.StringVar(value="Cuadrada")

    selector_senal = ttk.Combobox(
       marco_parametros,
       textvariable=senal_seleccionada,
       values=["Cuadrada", "Triangular", "Diente de sierra"],
       state="readonly",
       width=20
    )
    selector_senal.grid(row=0, column=1, padx=10, pady=8)


    # Número de armónicos
    ttk.Label(
       marco_parametros,
       text="Número de armónicos (N):"
    ).grid(row=0, column=2, padx=10, pady=8)

    # Variable asociada al número de armónicos seleccionado
    numero_armonicos = tk.StringVar(value="1")

    selector_armonicos = ttk.Combobox(
       marco_parametros,
       textvariable=numero_armonicos,
       values=["1", "2", "3", "5", "10", "20", "50", "100", "150", "200"],
       state="readonly",
       width=10
    )
    selector_armonicos.grid(row=0, column=3, padx=10, pady=8)


    # Intervalo temporal
    ttk.Label(
       marco_parametros,
       text="Tiempo inicial:"
    ).grid(row=1, column=0, padx=10, pady=8)

    # Variables vinculadas a las entradas de tiempo, con valores iniciales
    tiempo_inicial = tk.StringVar(value="-3.1416")

    entrada_inicio = ttk.Entry(
        marco_parametros,
        textvariable=tiempo_inicial,
        width=15
    )
    entrada_inicio.grid(row=1, column=1, padx=10, pady=8)


    ttk.Label(
       marco_parametros,
       text="Tiempo final:"
    ).grid(row=1, column=2, padx=10, pady=8)

    tiempo_final = tk.StringVar(value="3.1416")

    entrada_final = ttk.Entry(
        marco_parametros,
        textvariable=tiempo_final,
        width=15
    )
    entrada_final.grid(row=1, column=3, padx=10, pady=8)


   
    # ÁREA DE MÉTRICAS
   

    # Contenedor donde se muestran los resultados de las metricas
    marco_metricas = ttk.LabelFrame(
       marco_parametros,
       text="Métricas de evaluación",
       padding=12
    )
    marco_metricas.grid(
       row=0,
       column=4,
       rowspan=2,
       padx=15,
       pady=5,
       sticky="nsew"
    )

    # Etiquetas que mostrarán los resultados calculados
    etiqueta_error = ttk.Label(
       marco_metricas,
       text="RMSE: --",
       font=("Arial", 11, "bold")
    )
    etiqueta_error.grid(row=0, column=0, padx=20, pady=5)

    # Potencia original
    etiqueta_potencia_original = ttk.Label(
       marco_metricas,
       text="Potencia original: --",
       font=("Arial", 11, "bold")
    )
    etiqueta_potencia_original.grid(row=0, column=1, padx=20, pady=5)

    # Potencia reconstruida
    etiqueta_potencia_reconstruida = ttk.Label(
       marco_metricas,
       text="Potencia reconstruida: --",
       font=("Arial", 11, "bold")
    )
    etiqueta_potencia_reconstruida.grid(row=0, column=2, padx=20, pady=5)


    # 5. ÁREA DE GRÁFICAS
   

    # Crear el contenedor para integrar las gráficas de Matplotlib
    marco_graficas = ttk.LabelFrame(
       ventana,
       text="Visualización de señales",
       padding=10
    )
    marco_graficas.pack(fill="both", expand=True, padx=20, pady=5)

    # Crear la figura que contiene las tres gráficas
    figura = Figure(figsize=(10, 5), dpi=100)

    # Gráfica 1: señal original y reconstruida
    eje1 = figura.add_subplot(311)

    # Gráfica 2: error absoluto
    eje2 = figura.add_subplot(312)

    # Gráfica 3: espectro de línea
    eje3 = figura.add_subplot(313)


# Configurar los títulos, nombres de ejes y cuadrículas iniciales
    eje1.set_title("Señal original y reconstruida")
    eje1.set_ylabel("Amplitud")
    eje1.grid(True)

    eje2.set_title("Error absoluto")
    eje2.set_ylabel("Error")
    eje2.grid(True)

    eje3.set_title("Espectro de línea")
    eje3.set_xlabel("Frecuencia")
    eje3.set_ylabel("Amplitud")
    eje3.grid(True)

    # Integrar la figura de Matplotlib dentro de la ventana Tkinter
    canvas = FigureCanvasTkAgg(
       figura,
       master=marco_graficas
    )

     # Incorporar el lienzo a la ventana y permitir que ocupe el espacio disponible

    canvas.get_tk_widget().pack(fill="both", expand=True)



    # 6. APLICAR PARÁMETROS Y ACTUALIZAR GRÁFICA


    def aplicar_parametros():

        try:
            # Obtener los valores seleccionados o ingresados por el usuario
            senal = senal_seleccionada.get()
            N = int(numero_armonicos.get())

             # Convertir los tiempos ingresados a valores numéricos

            t_inicio = float(tiempo_inicial.get())
            t_final = float(tiempo_final.get())

             # Comprobar que el tiempo final sea mayor que el inicial
            if t_final <= t_inicio:
                messagebox.showerror(
                    "Error",
                    "El tiempo final debe ser mayor que el inicial."
                )
                return

            # Crear el vector de tiempo con 2000 muestras
            t = np.linspace(t_inicio, t_final, 2000)

            # Generar la señal original según la selección del usuario
            if senal == "Cuadrada":
                x = generar_senal_cuadrada(t)

            elif senal == "Triangular":
                x = generar_senal_triangular(t)

            elif senal == "Diente de sierra":
                x = generar_senal_diente_sierra(t)


            # Reconstruir la señal mediante la serie de Fourier
            x_reconstruida = reconstruir_senal(t, N, senal)


            # Calcular el error absoluto entre ambas señales
            error = np.abs(x - x_reconstruida)


            # Obtener el RMSE y las potencias de ambas señales
            rmse, potencia_original, potencia_reconstruida = calcular_metricas(
                x,
                x_reconstruida
            )


            # Actualizar el texto de las etiquetas con los nuevos resultados
            etiqueta_error.config(
                text=f"RMSE: {rmse:.6f}"
            )

            etiqueta_potencia_original.config(
                text=f"Potencia original: {potencia_original:.6f}"
            )

            etiqueta_potencia_reconstruida.config(
                text=f"Potencia reconstruida: {potencia_reconstruida:.6f}"
            )


            # Limpiar las gráficas anteriores para mostrar los nuevos resultados
            eje1.clear()
            eje2.clear()
            eje3.clear()

           
            # GRÁFICA 1: ORIGINAL Y RECONSTRUIDA
         
            # Dibujar la señal original en función del tiempo
            eje1.plot(
                t,
                x,
                label="Señal original",
                linewidth=2
            )
            # Dibujar la señal reconstruida para compararla con la original

            eje1.plot(
                t,
                x_reconstruida,
                label=f"Reconstrucción (N={N})",
                linestyle="--"
            )

            eje1.set_title(f"Señal: {senal}")
            eje1.set_ylabel("Amplitud")
            eje1.grid(True)

            # Mostrar las etiquetas que identifican cada curva
            eje1.legend()

         
            # GRÁFICA 2: ERROR ABSOLUTO

            # Representar el error absoluto calculado para cada muestra de tiempo
            

            eje2.plot(t, error, label="Error absoluto")

            eje2.set_title("Error de reconstrucción")
            eje2.set_ylabel("Error")
            eje2.grid(True)
            eje2.legend()

         
            # GRÁFICA 3: ESPECTRO
          

            # Obtener las frecuencias y amplitudes de los armónicos
            frecuencias, amplitudes = calcular_espectro(N, senal)

            # Representar el espectro mediante líneas verticales para cada armónico

            eje3.stem(frecuencias, amplitudes)

            eje3.set_title("Espectro de línea de la señal reconstruida")
            eje3.set_xlabel("Frecuencia (Hz)")
            eje3.set_ylabel("Amplitud")
            eje3.grid(True)


            # Ajustar la distribución de las gráficas y actualizar el lienzo
            figura.tight_layout()
            canvas.draw()


            # Mostrar en la interfaz los parámetros utilizados en la simulación
            mensaje_estado.config(
                text=f"Señal: {senal} | N: {N} | "
                    f"Intervalo: [{t_inicio}, {t_final}]"
            )

        except ValueError:
            # Informar al usuario cuando los valores ingresados no sean válidos
            messagebox.showerror(
                "Error",
                "Verifica que los valores ingresados sean válidos."
            )



    # 7. BOTÓN
  

    boton_aplicar = ttk.Button(
        marco_parametros,
        text="Aplicar parámetros",
        # Ejecutar aplicar_parametros cuando el usuario presione el botón
        command=aplicar_parametros
    )
    boton_aplicar.grid(row=2, column=0, columnspan=5, pady=12)


   
    # 8. ESTADO
    

    mensaje_estado = ttk.Label(
        ventana,
        text="Selecciona los parámetros para comenzar.",
        font=("Arial", 10)
    )
    mensaje_estado.pack(pady=8)


  
    # 9. EJECUCIÓN
   
    # Mantener activa la ventana y atender las interacciones
    ventana.mainloop()