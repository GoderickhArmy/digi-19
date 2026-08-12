#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Formulario de escritorio con Tkinter que muestra una grilla con los datos
de un archivo CSV (ejemplo.csv) y un botón para salir.
"""

import csv
import os
import tkinter as tk
from tkinter import ttk, messagebox

# Ruta del archivo CSV (mismo directorio que este script)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "ejemplo.csv")


def leer_csv(ruta):
    """Lee el archivo CSV y devuelve (encabezados, filas)."""
    with open(ruta, newline="", encoding="utf-8") as archivo:
        lector = csv.reader(archivo, delimiter=",")
        datos = [fila for fila in lector if fila]  # ignora líneas vacías
    if not datos:
        return [], []
    encabezados = datos[0]
    filas = datos[1:]
    return encabezados, filas


class Aplicacion(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Formulario Grilla de Ejemplo.")

        # Iniciar maximizado (Windows). Fallback para otros sistemas.
        try:
            self.state("zoomed")
        except tk.TclError:
            self.attributes("-zoomed", True)

        self._crear_widgets()
        self._cargar_datos()

    def _crear_widgets(self):
        # Contenedor principal
        contenedor = ttk.Frame(self, padding=10)
        contenedor.pack(fill=tk.BOTH, expand=True)

        # Marco para la grilla + scrollbars
        marco_grilla = ttk.Frame(contenedor)
        marco_grilla.pack(fill=tk.BOTH, expand=True)

        # Configurar estilos de la grilla para cambiar el azul predeterminado de selección por verde
        self.style = ttk.Style()
        self.style.theme_use("clam")  # Usar un tema compatible con personalización de Treeview
        self.style.configure("Treeview", 
                             background="white", 
                             fieldbackground="white")
        self.style.map("Treeview",
                       background=[("selected", "#4CAF50")],  # Verde para selección
                       foreground=[("selected", "white")])

        self.tree = ttk.Treeview(marco_grilla, show="headings")
        
        # Configurar colores para filas alternadas (verde claro y verde un poco más oscuro)
        self.tree.tag_configure("par", background="#E8F5E9")      # Verde clarito
        self.tree.tag_configure("impar", background="#C8E6C9")    # Verde un poco más oscuro

        scroll_y = ttk.Scrollbar(
            marco_grilla, orient=tk.VERTICAL, command=self.tree.yview
        )
        scroll_x = ttk.Scrollbar(
            marco_grilla, orient=tk.HORIZONTAL, command=self.tree.xview
        )
        self.tree.configure(
            yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set
        )

        self.tree.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")

        marco_grilla.rowconfigure(0, weight=1)
        marco_grilla.columnconfigure(0, weight=1)

        # Marco para los botones
        marco_botones = ttk.Frame(contenedor)
        marco_botones.pack(fill=tk.X, pady=(10, 0))

        boton_salir = ttk.Button(
            marco_botones, text="Salir", command=self.destroy
        )
        boton_salir.pack(side=tk.RIGHT)

    def _cargar_datos(self):
        if not os.path.exists(CSV_PATH):
            messagebox.showerror(
                "Error",
                f"No se encontró el archivo:\n{CSV_PATH}",
            )
            return

        try:
            encabezados, filas = leer_csv(CSV_PATH)
        except Exception as error:  # noqa: BLE001
            messagebox.showerror(
                "Error", f"No se pudo leer el archivo CSV:\n{error}"
            )
            return

        if not encabezados:
            messagebox.showwarning(
                "Aviso", "El archivo CSV no contiene datos."
            )
            return

        # Configurar columnas de la grilla
        self.tree["columns"] = encabezados
        for col in encabezados:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, width=150, anchor=tk.W, stretch=True)

        # Insertar filas de manera alternada con tags
        for i, fila in enumerate(filas):
            tag = "par" if i % 2 == 0 else "impar"
            self.tree.insert("", tk.END, values=fila, tags=(tag,))


def main():
    app = Aplicacion()
    app.mainloop()


if __name__ == "__main__":
    main()
