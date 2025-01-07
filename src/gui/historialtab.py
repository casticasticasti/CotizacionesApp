#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Bloque 1: 📚 Importaciones
import tkinter as tk
from tkinter import ttk, messagebox
import os
import json
import platform
import subprocess
from datetime import datetime
from src.utils.pdf_generator import PDFGenerator


# Bloque 2: 🎨 Clase HistorialTab
class HistorialTab:
    def __init__(self, notebook, parent_app):
        self.frame = ttk.Frame(notebook)
        self.parent_app = parent_app
        notebook.add(self.frame, text="Historial")

        # Inicializar componentes
        self.init_components()
        self.cargar_historial()


# Bloque 3: 📦 Inicialización de componentes
    def init_components(self):
        # Frame principal con scroll
        self.main_frame = ttk.Frame(self.frame)
        self.main_frame.pack(fill="both", expand=True)

        # Frame de búsqueda
        self.search_frame = ttk.LabelFrame(
            self.main_frame, text="Búsqueda", padding="10"
        )
        self.search_frame.pack(fill="x", padx=5, pady=5)

        # Configurar grid
        self.search_frame.grid_columnconfigure(1, weight=1)
        self.search_frame.grid_columnconfigure(3, weight=1)

        # Campos de búsqueda
        self.crear_campos_busqueda()

        # Tabla de historial
        self.crear_tabla_historial()

        # Botones de acción
        self.crear_botones_accion()


# Bloque 4: 📦 Creación de campos de búsqueda
    def crear_campos_busqueda(self):
        # Campo fecha
        label = ttk.Label(self.search_frame, text="Fecha:", anchor="w", width=15)
        label.grid(row=0, column=0, padx=(5, 10), pady=5, sticky="w")
        self.fecha_entry = ttk.Entry(self.search_frame)
        self.fecha_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Campo cliente
        label = ttk.Label(self.search_frame, text="Cliente:", anchor="w", width=15)
        label.grid(row=0, column=2, padx=(5, 10), pady=5, sticky="w")
        self.cliente_entry = ttk.Entry(self.search_frame)
        self.cliente_entry.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        # Campo marca
        label = ttk.Label(self.search_frame, text="Marca:", anchor="w", width=15)
        label.grid(row=1, column=0, padx=(5, 10), pady=5, sticky="w")
        self.marca_combo = ttk.Combobox(self.search_frame, state="readonly")
        self.marca_combo.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Campo modelo
        label = ttk.Label(self.search_frame, text="Modelo:", anchor="w", width=15)
        label.grid(row=1, column=2, padx=(5, 10), pady=5, sticky="w")
        self.modelo_combo = ttk.Combobox(self.search_frame, state="readonly")
        self.modelo_combo.grid(row=1, column=3, padx=5, pady=5, sticky="ew")


# Bloque 5: 📦 Creación de tabla de historial
    def crear_tabla_historial(self):
        # Frame para la tabla con scrollbar
        table_frame = ttk.Frame(self.main_frame)
        table_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame)
        scrollbar.pack(side="right", fill="y")

        # Tabla
        columns = ("Fecha", "Cliente", "Marca", "Modelo", "Total")
        self.tabla_historial = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=10,
            yscrollcommand=scrollbar.set,
        )

        # Configurar columnas
        for col in columns:
            self.tabla_historial.heading(col, text=col)
            self.tabla_historial.column(col, width=100)

        self.tabla_historial.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.tabla_historial.yview)

        # Binding para doble clic
        self.tabla_historial.bind("<Double-1>", self.abrir_cotizacion)


# Bloque 6: 📦 Creación de botones de acción
    def crear_botones_accion(self):
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(fill="x", padx=5, pady=5)

        # Botones izquierda
        left_frame = ttk.Frame(button_frame)
        left_frame.pack(side="left")

        ttk.Button(left_frame, text="Buscar", command=self.buscar_cotizaciones).pack(
            side="left", padx=5
        )

        ttk.Button(left_frame, text="Editar", command=self.editar_cotizacion).pack(
            side="left", padx=5
        )

        ttk.Button(left_frame, text="Ver PDF", command=self.abrir_cotizacion).pack(
            side="left", padx=5
        )


# Bloque 7: 📦 Cargar historial
    def cargar_historial(self):
        """Carga el historial desde el archivo JSON"""
        historial_file = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "output",
            "historial.json",
        )

        try:
            if os.path.exists(historial_file):
                with open(historial_file, "r") as f:
                    self.historial = json.load(f)
                self.actualizar_tabla()
            else:
                self.historial = []
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar el historial: {str(e)}")
            self.historial = []


# Bloque 8: 📦 Actualizar tabla
    def actualizar_tabla(self, filtrado=None):
        """Actualiza la tabla con los datos del historial"""
        # Limpiar tabla
        for item in self.tabla_historial.get_children():
            self.tabla_historial.delete(item)

        # Datos a mostrar
        datos = filtrado if filtrado is not None else self.historial

        # Insertar datos
        for cotizacion in datos:
            self.tabla_historial.insert(
                "",
                "end",
                values=(
                    cotizacion["fecha"],
                    cotizacion["cliente"],
                    cotizacion["marca"],
                    cotizacion["modelo"],
                    f"${cotizacion['total']:,.0f}",
                ),
            )


# Bloque 9: 📦 Buscar cotizaciones
    def buscar_cotizaciones(self):
        """Filtra las cotizaciones según los criterios de búsqueda"""
        fecha = self.fecha_entry.get().strip()
        cliente = self.cliente_entry.get().strip().lower()
        marca = self.marca_combo.get()
        modelo = self.modelo_combo.get()

        filtrado = []
        for cotizacion in self.historial:
            if fecha and fecha not in cotizacion["fecha"]:
                continue
            if cliente and cliente not in cotizacion["cliente"].lower():
                continue
            if marca and marca != cotizacion["marca"]:
                continue
            if modelo and modelo != cotizacion["modelo"]:
                continue
            filtrado.append(cotizacion)

        self.actualizar_tabla(filtrado)


# Bloque 10: 📦 Abre el PDF de la cotización seleccionada
    def abrir_cotizacion(self, event=None):
        seleccion = self.tabla_historial.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor seleccione una cotización")
            return

        item = seleccion[0]
        idx = self.tabla_historial.index(item)

        # Generar ruta del PDF
        fecha_str = self.historial[idx]["fecha"].replace("/", "")
        cliente = self.historial[idx]["cliente"]
        pdf_path = f"output/cotizaciones/cotizacion_{cliente}_{fecha_str}.pdf"

        if os.path.exists(pdf_path):
            if platform.system() == "Darwin":  # macOS
                subprocess.run(["open", pdf_path])
            elif platform.system() == "Windows":
                os.startfile(pdf_path)
            else:  # Linux
                subprocess.run(["xdg-open", pdf_path])
        else:
            messagebox.showerror("Error", "No se encontró el archivo PDF")


# Bloque 11: 📦 Editar cotización
    def editar_cotizacion(self) -> None:
        seleccion = self.tabla_historial.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione una cotización para editar")
            return

        item = seleccion[0]
        idx = self.tabla_historial.index(item)
        cotizacion = self.historial[idx]

        # Cambiar a pestaña de cotización
        self.parent_app.notebook.select(0)

        # Cargar datos en el formulario
        self.parent_app.cotizacion_tab.cargar_cotizacion(cotizacion)

