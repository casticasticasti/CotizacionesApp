#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Bloque 1: 📚 Importaciones
import json
import os
from typing import Dict, List, Any, Tuple
from config.settings import PDF_CONFIG, PATHS
from datetime import datetime
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
)


# Bloque 2: 🎨 Función para formatear un número como moneda
def format_currency(amount: float) -> str:
    """Formatea un número como moneda.

    Args:
        amount: Cantidad a formatear

    Returns:
        str: Cantidad formateada con separador de miles y sin decimales
    """
    return f"${amount:,.0f}".replace(",", ".")


# Bloque 3: 📚 Clase PDFGenerator
class PDFGenerator:


# Bloque 4: 🎨 Inicializador
    def __init__(self) -> None:
        """Initialize the PDF generator."""
        self.config = PDF_CONFIG
        self.margin = self.config["page"]["margin"]
        self.page_width = letter[0] - (2 * self.margin)
        self.page_height = letter[1] - (2 * self.margin)


# Bloque 5: 📚 Método para generar un PDF de cotización
    def generar_cotizacion(self, datos: Dict[str, Any], output_path: str) -> bool:
        """Genera un PDF de cotización con los datos proporcionados.

        Args:
            datos: Diccionario con los datos de la cotización
            output_path: Ruta donde se guardará el PDF

        Returns:
            bool: True si se generó correctamente, False en caso contrario
        """
        try:
            doc = SimpleDocTemplate(
                output_path,
                pagesize=letter,
                rightMargin=self.margin,
                leftMargin=self.margin,
                topMargin=self.margin,
                bottomMargin=self.margin,
            )

            # Crear elementos del documento
            elements = []

            # Agregar logo
            logo_path = Path(PATHS["LOGO_PATH"])
            if logo_path.exists():
                img = Image(str(logo_path))

                # Obtener proporciones originales de la imagen
                aspect_ratio = img.imageWidth / img.imageHeight  # Ancho/Alto

                # Ajustar el ancho al ancho de la página
                img.drawWidth = self.page_width  # Usa el ancho disponible en la página
                img.drawHeight = (
                    self.page_width / aspect_ratio
                )  # Calcula la altura proporcional

                # Agregar imagen y espacio
                elements.append(img)
                elements.append(Spacer(1, 20))  # Espaciado opcional

            # Agregar título
            title_style = ParagraphStyle(
                "CustomTitle",
                parent=getSampleStyleSheet()["Heading1"],
                fontSize=24,
                spaceAfter=30,
                alignment=1,  # Centrado
            )

            # Usar etiquetas <u> para subrayar
            title = "<u>Cotización</u>"
            elements.append(Paragraph(title, title_style))

            # Datos del cliente
            client_data = [
                ["Cliente:", datos["cliente"]],
                ["Fecha:", datos["fecha"]],
                ["Marca:", datos["marca"]],
                ["Modelo:", datos["modelo"]],
                ["Año:", datos["anio"]],
                ["Patente:", datos["patente"]],
                ["Duración:", datos["duracion"]],
            ]

            # Crear tabla de datos del cliente
            client_table = Table(
                client_data,
                colWidths=[self.page_width * 0.2, self.page_width * 0.8],
                style=TableStyle(
                    [
                        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                        ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
                        ("FONTSIZE", (0, 0), (-1, -1), 12),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                        ("GRID", (0, 0), (-1, -1), 1, colors.black),  # Agregamos bordes
                        (
                            "BACKGROUND",
                            (0, 0),
                            (0, -1),
                            colors.lightgrey,
                        ),  # Fondo para etiquetas
                    ]
                ),
            )

            elements.append(client_table)
            elements.append(Spacer(1, 20))

            # Tabla de productos
            if datos["productos"]:
                headers = ["Producto", "Cantidad", "Precio", "Total"]
                products_data = [
                    [
                        prod["producto"],
                        str(prod["cantidad"]),
                        format_currency(prod["precio"]),
                        format_currency(prod["total"]),
                    ]
                    for prod in datos["productos"]
                ]

                # Agregar productos
                products_table = Table(
                    [headers] + products_data,
                    colWidths=[
                        self.page_width * 0.4,
                        self.page_width * 0.2,
                        self.page_width * 0.2,
                        self.page_width * 0.2,
                    ],
                    style=TableStyle(
                        [
                            ("ALIGN", (0, 0), (0, -1), "LEFT"),
                            ("ALIGN", (1, 0), (-1, -1), "CENTER"),
                            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                            ("FONTSIZE", (0, 0), (-1, -1), 12),
                            ("GRID", (0, 0), (-1, -1), 1, colors.black),
                            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                            ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                            ("TOPPADDING", (0, 0), (-1, -1), 10),
                        ]
                    ),
                )
                elements.append(products_table)
                elements.append(Spacer(1, 20))

                # Agregar total
                total_style = ParagraphStyle(
                    "Total",
                    parent=getSampleStyleSheet()["Normal"],
                    fontSize=14,
                    alignment=2,  # RIGHT
                    fontName="Helvetica-Bold",
                )
                total_table = Table(
                    [["", "", "Total con IVA:", format_currency(datos["total"])]],
                    colWidths=[
                        self.page_width * 0.4,
                        self.page_width * 0.2,
                        self.page_width * 0.2,
                        self.page_width * 0.2,
                    ],
                    style=TableStyle(
                        [
                            ("ALIGN", (2, 0), (-1, -1), "RIGHT"),
                            ("FONTNAME", (2, 0), (-1, -1), "Helvetica-Bold"),
                            ("FONTSIZE", (2, 0), (-1, -1), 12),
                        ]
                    ),
                )
                elements.append(total_table)

            # Generar PDF
            doc.build(elements)
            return True

        except Exception as e:
            print(f"Error al generar PDF: {str(e)}")
            return False


# Bloque 6: 📚 Función para guardar la cotización en el historial
def guardar_historial(datos: Dict[str, Any]) -> None:
    """Guarda los datos de la cotización en el historial.

    Args:
        datos: Diccionario con los datos de la cotización
    """
    try:
        # Cargar historial existente
        if os.path.exists(PATHS["HISTORIAL_PATH"]):
            with open(PATHS["HISTORIAL_PATH"], "r", encoding="utf-8") as f:
                historial = json.load(f)
        else:
            historial = []

        # Agregar nueva cotización
        historial.append(datos)

        # Guardar historial actualizado
        with open(PATHS["HISTORIAL_PATH"], "w", encoding="utf-8") as f:
            json.dump(historial, f, indent=4, ensure_ascii=False)

    except Exception as e:
        print(f"Error al guardar historial: {str(e)}")
