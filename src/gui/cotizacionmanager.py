#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Bloque 1: Importaciones
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from tkinter import messagebox
import pandas as pd
from src.utils.pdf_generator import PDFGenerator, guardar_historial
from src.core.interfaces import PDFGeneratorInterface
from config.settings import PATHS, BASE_DIR


# Bloque 2: Clase CotizacionManager
class CotizacionManager:


# Bloque 3: Método inicializador
    def __init__(self, parent_tab: Any) -> None:
        self.parent_tab = parent_tab
        self.productos_seleccionados: List[Dict[str, Any]] = []
        self.df_marcas: pd.DataFrame = parent_tab.parent_app.df_marcas
        self.df_sistemas: pd.DataFrame = parent_tab.parent_app.df_sistemas


# Bloque 4: Método para agregar productos a la cotización
    def agregar_producto(self, producto: str, cantidad: int, precio: float) -> bool:
        """Agrega un producto a la lista de productos seleccionados"""
        try:
            if not producto or cantidad <= 0 or precio <= 0:
                messagebox.showerror(
                    "Error", "Por favor complete todos los campos correctamente"
                )
                return False

            total = cantidad * precio

            # Agregar a la lista de productos
            self.productos_seleccionados.append(
                {
                    "producto": producto,
                    "cantidad": cantidad,
                    "precio": precio,
                    "total": total,
                }
            )
            return True

        except ValueError:
            messagebox.showerror(
                "Error",
                "Por favor ingrese valores numéricos válidos para cantidad y precio",
            )
            return False


# Bloque 5: Método para editar producto seleccionado
    def editar_producto(self, idx: int) -> Optional[Dict[str, Any]]:
        """Retorna un producto para edición y lo elimina de la lista"""
        if 0 <= idx < len(self.productos_seleccionados):
            return self.productos_seleccionados.pop(idx)
        return None


# Bloque 6: Método para eliminar producto de la lista
    def eliminar_producto(self, idx: int) -> bool:
        """Elimina un producto de la lista"""
        if 0 <= idx < len(self.productos_seleccionados):
            self.productos_seleccionados.pop(idx)
            return True
        return False


# Bloque 7: Método para calcular total de la cotización
    def calcular_total(self) -> float:
        """Calcula el total de la cotización"""
        return sum(producto["total"] for producto in self.productos_seleccionados)


# Bloque 8: Método para generar cotización en PDF
    def generar_cotizacion(self, datos: Dict[str, Any]) -> bool:
        """Genera la cotización en PDF"""
        try:
            # Generar nombre del archivo basado en el cliente y la fecha
            fecha_str = datetime.strptime(datos["fecha"], "%d/%m/%Y").strftime("%Y%m%d")
            # Sanitize cliente name by replacing special characters with underscore
            cliente_safe = "".join(c if c.isalnum() else "_" for c in datos["cliente"])
            nombre_archivo = f"cotizacion_{cliente_safe}_{fecha_str}.pdf"

            # Crear directorio de cotizaciones si no existe
            output_dir = Path("output/cotizaciones")
            output_dir.mkdir(parents=True, exist_ok=True)

            # Ruta completa del archivo
            filepath = output_dir / nombre_archivo

            # Generar PDF
            pdf_generator: PDFGeneratorInterface = PDFGenerator()
            if pdf_generator.generar_cotizacion(datos, str(filepath)):
                # Guardar en historial
                guardar_historial(datos)

                # Mostrar mensaje de éxito y preguntar si desea abrir el archivo
                respuesta = messagebox.askyesno(
                    "Éxito",
                    f"Cotización generada exitosamente en:\n{filepath}\n\n¿Desea abrir el archivo?",
                )

                # Abrir el archivo si el usuario lo desea
                if respuesta:
                    if sys.platform == "darwin":  # macOS
                        os.system(f"open {filepath}")
                    elif sys.platform == "win32":  # Windows
                        os.startfile(filepath)
                    else:  # Linux
                        os.system(f"xdg-open {filepath}")

                return True
            else:
                messagebox.showerror(
                    "Error",
                    "Hubo un error al generar la cotización",
                )
                return False

        except Exception as e:
            messagebox.showerror("Error", f"Error al generar PDF: {str(e)}")
            return False


# Bloque 9: Método para cargar marcas
    def cargar_marcas(self) -> List[str]:
        """Retorna la lista de marcas disponibles"""
        return self.df_marcas.columns[1:].tolist()


# Bloque 10: Método para obtener modelos
    def obtener_modelos(self, marca: str) -> List[str]:
        """Retorna la lista de modelos para una marca específica"""
        if marca in self.df_marcas.columns:
            return self.df_marcas[marca].dropna().tolist()
        return []


# Bloque 11: Método para validar datos del formulario
    def validar_datos_formulario(self, datos: Dict[str, str]) -> bool:
        """Valida los datos del formulario"""
        campos_vacios = [k for k, v in datos.items() if not v]
        if campos_vacios:
            messagebox.showerror(
                "Error",
                f"Los siguientes campos son requeridos: {', '.join(campos_vacios)}",
            )
            return False

        if not self.productos_seleccionados:
            messagebox.showerror("Error", "Debe agregar al menos un producto")
            return False

        return True


# Bloque 12: Método para preparar datos de cotización
    def preparar_datos_cotizacion(
        self, datos_form: Dict[str, str]
    ) -> Optional[Dict[str, Any]]:
        """Prepara los datos para la cotización"""
        if not self.validar_datos_formulario(datos_form):
            return None

        total = self.calcular_total()

        return {
            "cliente": datos_form["Nombre"],
            "fecha": datos_form["Fecha"],
            "marca": datos_form["Marca"],
            "modelo": datos_form["Modelo"],
            "anio": datos_form["Año"],
            "patente": datos_form["Patente"],
            "duracion": datos_form["Duración"],
            "productos": self.productos_seleccionados.copy(),
            "total": total,
        }


# Bloque 13: Método para cargar cotización existente
    def cargar_cotizacion_existente(self, cotizacion: Dict[str, Any]) -> None:
        """Carga los datos de una cotización existente"""
        if "productos" in cotizacion:
            self.productos_seleccionados = cotizacion["productos"]


# Bloque 14: Método para guardar nuevos modelos en el DataFrame
    def guardar_nuevo_modelo(self, nuevo_modelo: str) -> bool:
        """Guarda un nuevo modelo para la marca seleccionada.

        Args:
            nuevo_modelo: Nombre del nuevo modelo a guardar

        Returns:
            bool: True si se guardó correctamente, False en caso contrario
        """
        try:
            marca_seleccionada = self.parent_tab.marca_combo.get()
            if not marca_seleccionada:
                messagebox.showerror(
                    "Error", "Por favor seleccione una marca antes de agregar un modelo"
                )
                return False

            # Verificar si el modelo ya existe
            modelos_actuales = self.obtener_modelos(marca_seleccionada)
            if nuevo_modelo in modelos_actuales:
                return True  # El modelo ya existe, no es necesario agregarlo

            # Encontrar el primer índice vacío en la columna de la marca
            marca_col = self.df_marcas[marca_seleccionada]
            primer_indice_vacio = marca_col.isna().idxmax()

            # Agregar el nuevo modelo
            self.df_marcas.at[primer_indice_vacio, marca_seleccionada] = nuevo_modelo

            # Guardar el DataFrame actualizado
            self.df_marcas.to_csv(
                BASE_DIR / PATHS["DATA_DIR"] / "HojaMarcas.csv",
                index=False,
                encoding="utf-8"
            )

            return True

        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar el nuevo modelo: {str(e)}")
            return False
