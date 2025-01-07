#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Bloque 1: 📚 Importaciones
import pandas as pd
import sys
import tkinter as tk
from config.settings import GUI_CONFIG, PATHS
from pathlib import Path
from src.core.interfaces import DataProvider, HistoryManager
from src.core.providers import CSVDataProvider, FileHistoryManager
from src.gui.cotizaciontab import CotizacionTab
from src.gui.historialtab import HistorialTab
from src.gui.inventariotab import InventarioTab
from tkinter import ttk, messagebox
from typing import Optional, List


# Bloque 2: Configuracion de la ruta base
BASE_DIR = Path(__file__).resolve().parent


# Bloque 3: 📚 Clase principal de la aplicación
class CotizacionesApp:


# Bloque 4: 📚 Inicialización de la aplicación. Args: data_provider (Proveedor de datos) y history_manager (Gestor de historial)
    def __init__(
        self, data_provider: DataProvider, history_manager: HistoryManager
    ) -> None:
        self.data_provider = data_provider
        self.history_manager = history_manager
        self.config = GUI_CONFIG
        self.root = tk.Tk()
        self.root.title(GUI_CONFIG["window"]["title"])

        # Configurar ventana
        window_width = GUI_CONFIG["window"]["width"]
        window_height = GUI_CONFIG["window"]["height"]
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calcular posición para centrar
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        # Configurar geometría
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Cargar datos
        self.cargar_datos()

        # Crear notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=5, pady=5)

        # Crear pestañas
        self.cotizacion_tab = CotizacionTab(self)
        self.historial_tab = HistorialTab(self.notebook, self)
        self.inventario_tab = InventarioTab(self.notebook, self.df_inventario)
        self.inventario_tab.actualizar_tabla_inventario()


# Bloque 5: 📚 Carga de datos necesarios para la aplicación
    def cargar_datos(self) -> None:
        try:
            self.df_inventario = self.data_provider.get_inventory_data()
            self.df_sistemas = self.data_provider.get_systems_data()
            self.df_marcas = self.data_provider.get_brands_data()
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar los datos: {str(e)}")
            sys.exit(1)


# Bloque 6: 📚 Inicia la aplicación
    def run(self) -> None:
        self.root.mainloop()


# Bloque 7: 📚 Crea los directorios necesarios si no existen
def crear_directorios() -> None:
    for dir_path in [PATHS["ASSETS_DIR"], PATHS["OUTPUT_DIR"]]:
        Path(dir_path).mkdir(parents=True, exist_ok=True)


# Bloque 8: 📚 Verifica que existan los directorios necesarios
def verificar_directorios() -> None:
    directorios = [
        BASE_DIR / PATHS["DATA_DIR"],
        BASE_DIR / PATHS["ASSETS_DIR"],
        BASE_DIR / PATHS["OUTPUT_DIR"],
    ]
    for directorio in directorios:
        directorio.mkdir(exist_ok=True)


# Bloque 9: 📚 Verifica que existan los archivos necesarios. True si todos los archivos existen, False en caso contrario
def verificar_archivos() -> bool:
    archivos_requeridos = [
        BASE_DIR / PATHS["DATA_DIR"] / "HojaInventario.csv",
        BASE_DIR / PATHS["DATA_DIR"] / "HojaSistemas.csv",
        BASE_DIR / PATHS["DATA_DIR"] / "HojaMarcas.csv",
        BASE_DIR / PATHS["ASSETS_DIR"] / "logo.png",
    ]

    for archivo in archivos_requeridos:
        if not archivo.exists():
            print(f"Archivo no encontrado: {archivo}")
            return False
    return True


# Bloque 10: 📚 Función principal de la aplicación
def main() -> None:
    verificar_directorios()
    if not verificar_archivos():
        sys.exit(1)

    data_provider = CSVDataProvider(BASE_DIR)
    history_manager = FileHistoryManager(BASE_DIR)

    app = CotizacionesApp(data_provider, history_manager)
    app.run()


# Bloque 11: 📚 Punto de entrada de la aplicación
if __name__ == "__main__":
    main()
