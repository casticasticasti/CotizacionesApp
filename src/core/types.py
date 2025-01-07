"""Custom type definitions for the application."""
from typing import TypedDict, Union, List, Dict

class ProductData(TypedDict):
    producto: str
    cantidad: int
    precio: float
    total: float

class QuoteData(TypedDict):
    nombre: str
    fecha: str
    marca: str
    modelo: str
    duracion: str
    productos: List[ProductData]
    total: float

NumericType = Union[int, float]
StringDict = Dict[str, str]
ProductList = List[ProductData]
