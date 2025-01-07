# 🚗 CotizacionesApp - Sistema de Gestión de Cotizaciones e Inventario Automotriz

## 📋 Índice

1. [Descripción General](#descripción-general)
2. [Especificaciones Técnicas](#especificaciones-técnicas)
3. [Arquitectura del Sistema](#arquitectura-del-sistema)
4. [Componentes Principales](#componentes-principales)
5. [Estructura de Datos](#estructura-de-datos)
6. [Interfaz de Usuario](#interfaz-de-usuario)
7. [Almacenamiento y Persistencia](#almacenamiento-y-persistencia)
8. [Configuración del Sistema](#configuración-del-sistema)
9. [Gestión de Tipos](#gestión-de-tipos)
10. [Implementaciones Pendientes](#implementaciones-pendientes)
11. [Cambios Realizados](#cambios-realizados)

## Descripción General

Sistema profesional de gestión de cotizaciones e inventario desarrollado en Python, diseñado específicamente para la gestión de repuestos automotrices. La aplicación proporciona una interfaz gráfica robusta para la creación, gestión y seguimiento de cotizaciones, así como el manejo de inventario.

## Especificaciones Técnicas

### Requisitos del Sistema

- Sistema Operativo: Linux/Windows/MacOS
- RAM: 4GB mínimo
- Espacio en Disco: 500MB
- Python >= 3.8

### Dependencias Principales

- Python >= 3.8
- pandas >= 2.0.0 (manipulación de datos)
- tkcalendar >= 1.6.1 (widgets de calendario)
- reportlab >= 3.6.12 (generación de PDFs)
- typing-extensions >= 4.5.0 (soporte de tipos)

### Requisitos de Desarrollo

- mypy >= 1.0.0 (verificación de tipos)
- pandas-stubs >= 2.0.0
- types-reportlab >= 3.6.12

## Arquitectura del Sistema

### Estructura del Proyecto

```console
$HOME/Proyectos/Geral/CotizacionesApp
├── app.log
├── assets
│   ├── logo.png
│   ├── logoOriginal.png
│   ├── logo_enhanced.png
│   ├── logo_resized.png
│   └── logo_resized_sharpened.png
├── config
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-312.pyc
│   │   └── settings.cpython-312.pyc
│   └── settings.py
├── data
│   ├── HojaInventario.csv
│   ├── HojaMarcas.csv
│   └── HojaSistemas.csv
├── drafts
│   └── cotizacionestab.py
├── main.py
├── mypy.ini
├── output
│   ├── cotizaciones
│   │   ├── cotizacion_Basti_20250102.pdf
│   │   ├── cotizacion_Geral_20250103.pdf
│   │   └── cotizacion_Mariana_20250104.pdf
│   ├── historial.json
│   └── reportes
├── readMe.md
├── requirements.txt
└── src
    ├── __init__.py
    ├── __pycache__
    │   └── __init__.cpython-312.pyc
    ├── core
    │   ├── __init__.py
    │   ├── __pycache__
    │   │   ├── __init__.cpython-312.pyc
    │   │   ├── interfaces.cpython-312.pyc
    │   │   └── providers.cpython-312.pyc
    │   ├── interfaces.py
    │   ├── providers.py
    │   └── types.py
    ├── datos
    │   ├── procesador.py
    │   └── validaciones.py
    ├── gui
    │   ├── __pycache__
    │   │   ├── cotizacionestab.cpython-312.pyc
    │   │   ├── cotizacionmanager.cpython-312.pyc
    │   │   ├── cotizaciontab.cpython-312.pyc
    │   │   ├── historialtab.cpython-312.pyc
    │   │   └── inventariotab.cpython-312.pyc
    │   ├── cotizacionmanager.py
    │   ├── cotizaciontab.py
    │   ├── historialtab.py
    │   └── inventariotab.py
    └── utils
        ├── __pycache__
        │   └── pdf_generator.cpython-312.pyc
        ├── excel_handler.py
        └── pdf_generator.py

18 directories, 45 files
```

## Componentes Principales

### 1. Módulo de Cotizaciones (`CotizacionTab`)

- Gestión de datos del cliente
  - Nombre
  - Fecha (con selector de calendario)
  - Marca y modelo del vehículo
  - Duración de la cotización
- Tabla de productos
  - Selección de productos del inventario
  - Cálculo automático de totales
  - Edición y eliminación de items
- Generación de documentos
  - Exportación a PDF con formato personalizado
  - Almacenamiento en historial

### 2. Módulo de Historial (`HistorialTab`)

- Funcionalidades:
  - Búsqueda avanzada de cotizaciones
  - Visualización de cotizaciones anteriores
  - Edición de cotizaciones existentes
  - Exportación de cotizaciones a PDF
- Sistema de filtrado por:
  - Cliente
  - Fecha
  - Marca/Modelo

### 3. Módulo de Inventario (`InventarioTab`)

- Gestión completa de productos
  - Nombre y descripción
  - Marca y modelo
  - Sistema y componente
  - Estado y precio
  - Control de cantidad
- Funcionalidades:
  - Búsqueda de productos
  - Actualización de inventario
  - Exportación de datos

## Estructura de Datos

### Formato del Inventario (CSV)

- NOMBRE_DEL_PRODUCTO
- DESCRIPCION_DEL_PRODUCTO
- MARCA
- MODELO
- SISTEMA
- COMPONENTE
- ESTADO
- PRECIO
- CANTIDAD
- IMAGEN

### Formato de Cotización (PDF)

1. Encabezado
   - Logo empresarial
   - Título "Cotización"
2. Información del Cliente
   - Tabla con datos del comprador
   - Detalles del vehículo
3. Detalle de Productos
   - Tabla de productos seleccionados
   - Cantidades y valores
   - Total calculado

## Interfaz de Usuario

### Ventana Principal

- Sistema de pestañas (Notebook)
  - Pestaña de Cotizaciones
  - Pestaña de Historial
  - Pestaña de Inventario
- Dimensiones configurables
- Posicionamiento automático centrado

### Validaciones

- Verificación de campos requeridos
- Validación de formatos de fecha
- Control de existencias
- Verificación de precios y cantidades

## Almacenamiento y Persistencia

### Sistema de Archivos

- Cotizaciones: `/output/cotizaciones/`
- Reportes: `/output/reportes/`
- Datos: `/data/`
  - `HojaInventario.csv`
  - `HojaSistemas.csv`
  - `HojaMarcas.csv`

## Configuración del Sistema

El sistema utiliza archivos de configuración en el directorio `/config/` para:

- Parámetros de la interfaz gráfica
- Rutas de archivos
- Configuraciones de exportación
- Formatos de documentos

## Gestión de Tipos

El proyecto implementa verificación estática de tipos usando:

- Anotaciones de tipo Python
- Verificación con mypy
- Stubs de tipos para dependencias externas

## Implementaciones pendientes

### Nuevos campos

- Agregar campo "Disponibilidad" al final.

### Mejoras en la interfaz

- Agregar "Limpiar caché" a la pestaña de historial.
- Agregar "Salir" a todas las pestañas.

### Exportación y vista previa

- Exportación a JPG.
- Vista previa de documentos.

## Cambios realizados

- Se agregó "con IVA" al final del total.
- Se ajustó el campo nombre para que acepte carecteres especiales.
- Se ajustó "Hasta agotar stock": que el checkbox sea predeterminado y se muestre en el PDF junto a la duración.
- Se agregó campo "Año" luego del campo "Modelo".
- Se agregó campo "Patente" luego del campo "Año".
- Se ajustó traspaso de datos al editar la cotización.
- Se ajustó el campo "Modelo" para que sea editable.
