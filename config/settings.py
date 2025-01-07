#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Bloque 1: Importaciones
import os
from typing import Dict, Any, List
from pathlib import Path

# Bloque 2: Configuración de rutas
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Bloque 3: Rutas de archivos
PATHS: Dict[str, str] = {
    "ASSETS_DIR": os.path.join(BASE_DIR, "assets"),
    "OUTPUT_DIR": os.path.join(BASE_DIR, "output"),
    "DATA_DIR": os.path.join(BASE_DIR, "data"),
    "LOGO_PATH": os.path.join(BASE_DIR, "assets", "logo.png"),
    "HISTORIAL_PATH": os.path.join(BASE_DIR, "output", "historial.json"),
}

# Bloque 4: Configuración de la GUI
GUI_CONFIG: Dict[str, Any] = {
    "window": {
        "title": "Sistema de Cotizaciones",
        "width": 1193,
        "height": 768,
    },
    "tabs": {
        "cotizacion": "Nueva Cotización",
        "historial": "Historial",
        "inventario": "Inventario",
    },
    "duracion_options": [
        "1 día",
        "2 días",
        "3 días",
        "4 días",
        "5 días",
        "6 días",
        "7 días",
        "10 días",
        "14 días",
        "21 días",
        "28 días",
        "30 días",
        "60 días",
    ],
    "paths": PATHS
}

# Bloque 5: Configuración del PDF
PDF_CONFIG: Dict[str, Any] = {
    "page": {
        "margin": 20,
        "logo_width": 926,
        "logo_height": 272,
    },
    "fonts": {
        "title": {
            "name": "CustomTitle",
            "base": "Heading1",
            "size": 28,
            "alignment": 1,
            "space_after": 30,
            "underline": True,
        },
        "total": {
            "name": "Total",
            "base": "Normal",
            "size": 14,
            "alignment": 2,
            "font_name": "Helvetica-Bold",
        },
        "table": {
            "name": "Helvetica",
            "size": 12,
        },
    },
    "tables": {
        "client": {
            "label_width": 150,
            "style": [
                ("ALIGN", (0, 0), (0, -1), "LEFT"),
                ("ALIGN", (1, 0), (1, -1), "LEFT"),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 12),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ],
        },
        "products": {
            "headers": ["Producto", "Cantidad", "Precio", "Total"],
            "column_ratios": {
                "product": 0.4,
                "quantity": 0.2,
                "value": 0.2,
            },
            "style": [
                ("ALIGN", (0, 0), (0, -1), "LEFT"),
                ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 12),
                ("GRID", (0, 0), (-1, -1), 1, "black"),
                ("BACKGROUND", (0, 0), (-1, 0), "lightgrey"),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
            ],
        },
    },
}
