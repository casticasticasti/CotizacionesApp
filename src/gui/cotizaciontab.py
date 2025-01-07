#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Bloque 1: Importaciones
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from datetime import datetime
from typing import Dict, Any, Optional
from src.gui.cotizacionmanager import CotizacionManager


# Bloque 2: Clase CotizacionTab
class CotizacionTab:

# Bloque 3: Inicializador de la clase
    def __init__(self, parent_app: Any) -> None:
        self.parent_app = parent_app
        self.notebook = parent_app.notebook
        self.manager = CotizacionManager(self)
        self.init_cotizacion_tab()
        self.cargar_marcas()


# Bloque 4: Método para inicializar la pestaña de cotización
    def init_cotizacion_tab(self) -> None:
        """Inicializa la pestaña de cotización"""
        self.cotizacion_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.cotizacion_frame, text="Cotización")

        # Frame para datos del cliente
        self.cliente_frame = ttk.LabelFrame(
            self.cotizacion_frame, text="Datos del Cliente"
        )
        self.cliente_frame.pack(fill="x", padx=5, pady=5)

        # Configurar el grid para expandir los campos
        self.cliente_frame.columnconfigure(1, weight=1)

        # Crear campos del formulario
        self.crear_campos_cliente()
        self.crear_tabla_productos()
        self.crear_botones_cotizacion()


# Bloque 5: Métodos para crear campos del formulario
    def crear_campos_cliente(self) -> None:
        """Crea los campos del formulario de cliente"""
        self.crear_campo_nombre()
        self.crear_campo_fecha()
        self.crear_campo_marca()
        self.crear_campo_modelo()
        self.crear_campo_anio()
        self.crear_campo_patente()
        self.crear_campo_duracion()


# Bloque 6: Método para crear el campo de nombre
    def crear_campo_nombre(self) -> None:
        """Crea el campo de nombre"""
        row = 0
        label = ttk.Label(self.cliente_frame, text="Nombre:", anchor="w", width=15)
        label.grid(row=row, column=0, padx=5, pady=5, sticky="w")
        self.entry_nombre = ttk.Entry(self.cliente_frame)
        self.entry_nombre.grid(row=row, column=1, columnspan=2, padx=5, pady=5, sticky="ew")


# Bloque 7: Método para crear campo de fecha
    def crear_campo_fecha(self) -> None:
        """Crea el campo de fecha con calendario"""
        row = 1
        label = ttk.Label(self.cliente_frame, text="Fecha:", anchor="w", width=15)
        label.grid(row=row, column=0, padx=5, pady=5, sticky="w")

        fecha_frame = ttk.Frame(self.cliente_frame)
        fecha_frame.grid(row=row, column=1, columnspan=2, sticky="ew")
        fecha_frame.columnconfigure(0, weight=1)

        self.fecha_entry = ttk.Entry(fecha_frame)
        self.fecha_entry.grid(row=0, column=0, sticky="ew")
        self.fecha_entry.insert(0, datetime.now().strftime("%d/%m/%Y"))

        calendar_button = ttk.Button(
            fecha_frame, text="📅", width=3, command=self.mostrar_calendario
        )
        calendar_button.grid(row=0, column=1, padx=(2, 0))


# Bloque 8: Método para mostrar calendario
    def mostrar_calendario(self) -> None:
        """Muestra el calendario para seleccionar fecha"""

        def seleccionar_fecha() -> None:
            self.fecha_entry.delete(0, tk.END)
            self.fecha_entry.insert(0, cal.selection_get().strftime("%d/%m/%Y"))
            top.destroy()

        top = tk.Toplevel(self.cliente_frame)
        top.title("Seleccionar Fecha")
        cal = Calendar(top, selectmode="day", date_pattern="dd/mm/yyyy", locale="es_ES")
        cal.pack(padx=10, pady=5)
        ttk.Button(top, text="Seleccionar", command=seleccionar_fecha).pack(pady=5)


# Bloque 9: Método para crear campo de marca
    def crear_campo_marca(self) -> None:
        """Crea el campo de marca"""
        row = 2
        label = ttk.Label(self.cliente_frame, text="Marca:", anchor="w", width=15)
        label.grid(row=row, column=0, padx=5, pady=5, sticky="w")
        self.marca_combo = ttk.Combobox(self.cliente_frame, state="readonly")
        self.marca_combo.grid(row=row, column=1, columnspan=2, padx=5, pady=5, sticky="ew")
        self.marca_combo.bind("<<ComboboxSelected>>", self.actualizar_modelos)


# Bloque 10: Método para crear campo de modelo
    def crear_campo_modelo(self) -> None:
        """Crea el campo de modelo"""
        row = 3
        label = ttk.Label(self.cliente_frame, text="Modelo:", anchor="w", width=15)
        label.grid(row=row, column=0, padx=5, pady=5, sticky="w")
        self.modelo_combo = ttk.Combobox(self.cliente_frame)  
        self.modelo_combo.grid(row=row, column=1, columnspan=2, padx=5, pady=5, sticky="ew")
        self.modelo_combo.bind('<Return>', self.guardar_nuevo_modelo)


# Bloque 11: Método para crear campo de año
    def crear_campo_anio(self) -> None:
        """Crea el campo de año"""
        row = 4
        label = ttk.Label(self.cliente_frame, text="Año:", anchor="w", width=15)
        label.grid(row=row, column=0, padx=5, pady=5, sticky="w")
        self.entry_anio = ttk.Entry(self.cliente_frame)
        self.entry_anio.grid(row=row, column=1, columnspan=2, padx=5, pady=5, sticky="ew")


# Bloque 12: Método para crear campo de patente
    def crear_campo_patente(self) -> None:
        """Crea el campo de patente"""
        row = 5
        label = ttk.Label(self.cliente_frame, text="Patente:", anchor="w", width=15)
        label.grid(row=row, column=0, padx=5, pady=5, sticky="w")
        self.entry_patente = ttk.Entry(self.cliente_frame)
        self.entry_patente.grid(row=row, column=1, columnspan=2, padx=5, pady=5, sticky="ew")


# Bloque 13: Método para crear campo de duración
    def crear_campo_duracion(self) -> None:
        """Crea el campo de duración"""
        row = 6
        label = ttk.Label(self.cliente_frame, text="Duración:", anchor="w", width=15)
        label.grid(row=row, column=0, padx=5, pady=5, sticky="w")

        # Frame para contener el combobox y el checkbox
        duracion_frame = ttk.Frame(self.cliente_frame)
        duracion_frame.grid(row=row, column=1, columnspan=2, sticky="ew")
        duracion_frame.columnconfigure(0, weight=1)

        self.duracion_combo = ttk.Combobox(
            duracion_frame,
            values=self.parent_app.config["duracion_options"],
            state="readonly",
        )
        self.duracion_combo.grid(row=0, column=0, padx=(0,5), sticky="ew")
        self.duracion_combo.set(self.parent_app.config["duracion_options"][0])

        # Crear el checkbox de agotar stock
        self.agotar_stock_var = tk.BooleanVar(value=True)  # Default to True
        self.agotar_stock_check = ttk.Checkbutton(
            duracion_frame,
            text="Hasta agotar stock",
            variable=self.agotar_stock_var,
        )
        self.agotar_stock_check.grid(row=0, column=1, padx=5, sticky="w")


# Bloque 14: Método para crear tabla de productos
    def crear_tabla_productos(self) -> None:
        """Crea la tabla de productos y sus controles"""
        # Frame para productos
        productos_frame = ttk.LabelFrame(self.cotizacion_frame, text="Productos")
        productos_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Frame para campos de entrada de productos
        entrada_frame = ttk.Frame(productos_frame)
        entrada_frame.pack(fill="x", padx=5, pady=5)

        # Campos de entrada para productos
        ttk.Label(entrada_frame, text="Producto:").grid(row=0, column=0, padx=5, pady=5)
        self.producto_entry = ttk.Entry(entrada_frame, width=40)
        self.producto_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(entrada_frame, text="Cantidad:").grid(row=0, column=2, padx=5, pady=5)
        self.cantidad_entry = ttk.Entry(entrada_frame, width=10)
        self.cantidad_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(entrada_frame, text="Precio:").grid(row=0, column=4, padx=5, pady=5)
        self.precio_entry = ttk.Entry(entrada_frame, width=10)
        self.precio_entry.grid(row=0, column=5, padx=5, pady=5)

        # Botones de acción para productos
        botones_frame = ttk.Frame(entrada_frame)
        botones_frame.grid(row=0, column=6, padx=5, pady=5)

        ttk.Button(botones_frame, text="Agregar", command=self.agregar_producto).pack(
            side="left", padx=2
        )
        ttk.Button(
            botones_frame, text="Limpiar", command=self.limpiar_campos_producto
        ).pack(side="left", padx=2)

        # Frame para la tabla y scrollbar
        tabla_frame = ttk.Frame(productos_frame)
        tabla_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Scrollbar
        scrollbar = ttk.Scrollbar(tabla_frame)
        scrollbar.pack(side="right", fill="y")

        # Crear tabla
        self.tabla_productos = ttk.Treeview(
            tabla_frame,
            columns=("Producto", "Cantidad", "Precio", "Total"),
            show="headings",
            yscrollcommand=scrollbar.set,
        )

        # Configurar columnas
        self.tabla_productos.heading("Producto", text="Producto")
        self.tabla_productos.heading("Cantidad", text="Cantidad")
        self.tabla_productos.heading("Precio", text="Precio")
        self.tabla_productos.heading("Total", text="Total")

        # Ajustar anchos de columna
        self.tabla_productos.column("Producto", width=350)
        self.tabla_productos.column("Cantidad", width=100, anchor="e")
        self.tabla_productos.column("Precio", width=100, anchor="e")
        self.tabla_productos.column("Total", width=100, anchor="e")

        self.tabla_productos.pack(fill="both", expand=True)
        scrollbar.config(command=self.tabla_productos.yview)

        # Frame para botones de acción y total
        acciones_frame = ttk.Frame(productos_frame)
        acciones_frame.pack(fill="x", padx=5, pady=5)

        # Botones de editar y eliminar
        ttk.Button(
            acciones_frame, text="Editar", command=self.editar_producto_seleccionado
        ).pack(side="left", padx=5)
        ttk.Button(
            acciones_frame, text="Eliminar", command=self.eliminar_producto
        ).pack(side="left", padx=5)

        # Label para el total
        self.total_label = ttk.Label(
            acciones_frame, text="Total con IVA: $0", font=("Helvetica", 12, "bold")
        )
        self.total_label.pack(side="right", padx=5)


# Bloque 15: Método para crear botones de cotización
    def crear_botones_cotizacion(self) -> None:
        """Crea los botones de acción"""
        buttons_frame = ttk.Frame(self.cotizacion_frame)
        buttons_frame.pack(fill="x", padx=5, pady=5)

        ttk.Button(
            buttons_frame, text="Generar PDF", command=self.generar_cotizacion, width=15
        ).pack(side="left", padx=5)

        ttk.Button(
            buttons_frame, text="Salir", command=self.parent_app.root.quit, width=15
        ).pack(side="left", padx=5)


# Bloque 16: Método para limpiar campos de producto
    def limpiar_campos_producto(self) -> None:
        """Limpia los campos de entrada de productos"""
        self.producto_entry.delete(0, tk.END)
        self.cantidad_entry.delete(0, tk.END)
        self.precio_entry.delete(0, tk.END)


# Bloque 17: Método para agregar producto
    def agregar_producto(self) -> None:
        """Agrega un producto a la tabla"""
        try:
            producto = self.producto_entry.get().strip()
            cantidad = int(self.cantidad_entry.get())
            precio = float(self.precio_entry.get())

            if self.manager.agregar_producto(producto, cantidad, precio):
                self.actualizar_tabla_productos()
                self.limpiar_campos_producto()
                self.actualizar_total()

        except ValueError:
            messagebox.showerror(
                "Error",
                "Por favor ingrese valores numéricos válidos para cantidad y precio",
            )


# Bloque 18: Método para editar producto seleccionado
    def editar_producto_seleccionado(self) -> None:
        """Carga el producto seleccionado en los campos de entrada para edición"""
        seleccion = self.tabla_productos.selection()
        if not seleccion:
            messagebox.showwarning(
                "Advertencia", "Por favor seleccione un producto para editar"
            )
            return

        item = seleccion[0]
        idx = self.tabla_productos.index(item)
        producto = self.manager.editar_producto(idx)

        if producto:
            # Cargar datos en los campos
            self.producto_entry.delete(0, tk.END)
            self.producto_entry.insert(0, producto["producto"])

            self.cantidad_entry.delete(0, tk.END)
            self.cantidad_entry.insert(0, str(producto["cantidad"]))

            self.precio_entry.delete(0, tk.END)
            self.precio_entry.insert(0, str(producto["precio"]))

            self.actualizar_tabla_productos()
            self.actualizar_total()


# Bloque 19: Método para actualizar tabla de productos
    def actualizar_tabla_productos(self) -> None:
        """Actualiza la tabla de productos"""
        # Limpiar la tabla actual
        for item in self.tabla_productos.get_children():
            self.tabla_productos.delete(item)

        # Agregar los productos a la tabla
        for producto in self.manager.productos_seleccionados:
            self.tabla_productos.insert(
                "",
                "end",
                values=(
                    producto["producto"],
                    producto["cantidad"],
                    f"${producto['precio']:,.0f}",
                    f"${producto['total']:,.0f}",
                ),
            )


# Bloque 20: Método para actualizar total
    def actualizar_total(self) -> None:
        """Actualiza el total de la cotización"""
        total = self.manager.calcular_total()
        self.total_label.config(text=f"Total con IVA: ${total:,.0f}")


# Bloque 21: Método para generar cotización
    def generar_cotizacion(self) -> None:
        """Genera la cotización en PDF"""
        datos_form = {
            "Nombre": self.entry_nombre.get().strip(),
            "Fecha": self.fecha_entry.get().strip(),
            "Marca": self.marca_combo.get().strip(),
            "Modelo": self.modelo_combo.get().strip(),
            "Año": self.entry_anio.get().strip(),
            "Patente": self.entry_patente.get().strip(),
            "Duración": self.obtener_duracion(),
        }

        datos = self.manager.preparar_datos_cotizacion(datos_form)
        if datos and self.manager.generar_cotizacion(datos):
            self.limpiar_formulario()


# Bloque 22: Método para limpiar formulario
    def limpiar_formulario(self) -> None:
        """Limpia todos los campos del formulario"""
        self.entry_nombre.delete(0, tk.END)
        self.fecha_entry.delete(0, tk.END)
        self.fecha_entry.insert(0, datetime.now().strftime("%d/%m/%Y"))
        self.marca_combo.set("")
        self.modelo_combo.set("")
        self.entry_anio.delete(0, tk.END)
        self.entry_patente.delete(0, tk.END)
        self.duracion_combo.set(self.parent_app.config["duracion_options"][0])
        self.agotar_stock_var.set(True)
        self.manager.productos_seleccionados = []
        self.actualizar_tabla_productos()
        self.actualizar_total()


# Bloque 23: Método para cargar marcas
    def cargar_marcas(self) -> None:
        """Carga las marcas en el combobox"""
        self.marca_combo["values"] = self.manager.cargar_marcas()


# Bloque 24: Método para actualizar modelos
    def actualizar_modelos(self, event: Optional[Any] = None) -> None:
        """Actualiza los modelos según la marca seleccionada"""
        marca_seleccionada = self.marca_combo.get()
        if marca_seleccionada:
            self.modelo_combo["values"] = self.manager.obtener_modelos(
                marca_seleccionada
            )
            self.modelo_combo.set("")


# Bloque 25: Método para eliminar producto
    def eliminar_producto(self) -> None:
        """Elimina el producto seleccionado"""
        seleccion = self.tabla_productos.selection()
        if not seleccion:
            messagebox.showwarning(
                "Selección requerida", "Por favor, seleccione un producto para eliminar"
            )
            return

        if messagebox.askyesno(
            "Confirmar eliminación", "¿Está seguro de que desea eliminar este producto?"
        ):
            idx = self.tabla_productos.index(seleccion[0])
            if self.manager.eliminar_producto(idx):
                self.actualizar_tabla_productos()
                self.actualizar_total()


# Bloque 26: Método para cargar cotización
    def cargar_cotizacion(self, cotizacion: Dict[str, Any]) -> None:
        """Carga los datos de una cotización existente en el formulario"""
        # Limpiar el formulario actual
        self.limpiar_formulario()

        # Cargar productos
        if "productos" in cotizacion:
            self.manager.productos_seleccionados = cotizacion["productos"]
            self.actualizar_tabla_productos()

        # Cargar datos del cliente
        if "cliente" in cotizacion:
            self.entry_nombre.insert(0, cotizacion["cliente"])

        if "fecha" in cotizacion:
            self.fecha_entry.delete(0, tk.END)
            self.fecha_entry.insert(0, cotizacion["fecha"])

        # Cargar marca y modelo
        if "marca" in cotizacion:
            self.marca_combo.set(cotizacion["marca"])
            # Actualizar modelos disponibles
            self.actualizar_modelos()
            if "modelo" in cotizacion:
                self.modelo_combo.set(cotizacion["modelo"])

        # Cargar año y patente
        if "anio" in cotizacion:
            self.entry_anio.insert(0, cotizacion["anio"])
        if "patente" in cotizacion:
            self.entry_patente.insert(0, cotizacion["patente"])

        # Cargar duración y estado del checkbox
        if "duracion" in cotizacion:
            duracion = cotizacion["duracion"]
            if "o hasta agotar stock" in duracion.lower():
                self.agotar_stock_var.set(True)
                duracion = duracion.replace(" o hasta agotar stock", "")
            else:
                self.agotar_stock_var.set(False)
            self.duracion_combo.set(duracion)


    def obtener_duracion(self) -> str:
        """Obtiene el texto de duración con el sufijo 'o hasta agotar stock' si corresponde"""
        duracion = self.duracion_combo.get()
        if self.agotar_stock_var.get():
            return f"{duracion} o hasta agotar stock"
        return duracion

    def guardar_nuevo_modelo(self, event: Optional[Any] = None) -> None:
        """Guarda el nuevo modelo ingresado en el combobox"""
        nuevo_modelo = self.modelo_combo.get()
        if nuevo_modelo:
            self.manager.guardar_nuevo_modelo(nuevo_modelo)
            self.modelo_combo["values"] = self.manager.obtener_modelos(
                self.marca_combo.get()
            )
