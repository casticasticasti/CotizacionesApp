#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Bloque 1: 📚 Importaciones
import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox


# Bloque 2: 🏭 Clase InventarioTab
class InventarioTab:
    def __init__(self, notebook, df_inventario):
        self.notebook = notebook
        self.df_inventario = df_inventario
        self.init_tab()


# Bloque 3: 📦 Inicialización de pestaña
    def init_tab(self):
        self.inventario_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.inventario_frame, text="Inventario")

        # Crear componentes
        self.crear_tabla_inventario()
        self.crear_botones_inventario()


# Bloque 4: 📊 Tabla de inventario
    def crear_tabla_inventario(self):
        # Frame contenedor con padding
        tabla_frame = ttk.Frame(self.inventario_frame, padding="5 5 5 5")
        tabla_frame.pack(fill="both", expand=True)

        columns = (
            "Producto", "Descripción", "Marca", "Modelo",
            "Sistema", "Componente", "Estado", "Precio", "Cantidad"
        )

        self.tabla_inventario = ttk.Treeview(
            tabla_frame,
            columns=columns,
            show="headings",
            style="Custom.Treeview"
        )


        # Configurar columnas
        for col in columns:
            self.tabla_inventario.heading(col, text=col)
            self.tabla_inventario.column(col, width=80)

        # Crear scrollbars
        self.scrolly = ttk.Scrollbar(
            self.inventario_frame,
            orient="vertical",
            command=self.tabla_inventario.yview
        )
        self.scrollx = ttk.Scrollbar(
            self.inventario_frame,
            orient="horizontal",
            command=self.tabla_inventario.xview
        )
        self.tabla_inventario.configure(
            yscrollcommand=self.scrolly.set,
            xscrollcommand=self.scrollx.set
        )

        # Posicionar elementos
        self.tabla_inventario.pack(fill="both", expand=True)
        self.scrolly.pack(side="right", fill="y")
        self.scrollx.pack(side="bottom", fill="x")


# Bloque 5: 🔘 Botones de inventario
    def crear_botones_inventario(self):
        self.botones_frame = ttk.Frame(self.inventario_frame)
        self.botones_frame.pack(fill="x", padx=5, pady=5)

        ttk.Button(
            self.botones_frame,
            text="Actualizar Inventario",
            command=self.actualizar_tabla_inventario
        ).pack(side="left", padx=5)

        ttk.Button(
            self.botones_frame,
            text="Exportar",
            command=self.exportar_inventario
        ).pack(side="right", padx=5)


# Bloque 6: 🔄 Actualización de tabla
    def actualizar_tabla_inventario(self):
        try:
            # Limpiar tabla actual
            for item in self.tabla_inventario.get_children():
                self.tabla_inventario.delete(item)

            # Insertar datos actualizados
            for _, row in self.df_inventario.iterrows():
                self.tabla_inventario.insert("", "end", values=tuple(row))
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar inventario: {str(e)}")


# Bloque 7: 📤 Exportación de inventario
    def exportar_inventario(self):
        # TODO: Implementar exportación de datos
        pass


# Bloque 8: 🔍 Búsqueda en inventario
    def buscar_producto(self, criterio):
        # TODO: Implementar búsqueda de productos
        pass


# Bloque 9: ✏️ Edición de inventario
    def editar_producto(self, item_id):
        # TODO: Implementar edición de productos
        pass


# Bloque 10: ➕ Agregar producto
    def agregar_producto(self):
        # TODO: Implementar agregación de productos
        pass


# Bloque 11: ❌ Eliminar producto
    def eliminar_producto(self, item_id):
        # TODO: Implementar eliminación de productos
        pass
