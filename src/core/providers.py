from typing import Dict, List, Optional, Any, Union
from datetime import datetime
import pandas as pd
from pathlib import Path
from src.core.interfaces import DataProvider, PDFGeneratorInterface, HistoryManager
from config.settings import PATHS

class CSVDataProvider(DataProvider):
    def __init__(self, base_dir: Path) -> None:
        self.base_dir = base_dir
        self.data_dir = base_dir / PATHS["DATA_DIR"]

    def get_inventory_data(self) -> pd.DataFrame:
        return pd.read_csv(self.data_dir / "HojaInventario.csv")

    def get_systems_data(self) -> pd.DataFrame:
        return pd.read_csv(self.data_dir / "HojaSistemas.csv")

    def get_brands_data(self) -> pd.DataFrame:
        return pd.read_csv(self.data_dir / "HojaMarcas.csv")

class FileHistoryManager(HistoryManager):
    def __init__(self, base_dir: Path) -> None:
        self.base_dir = base_dir
        self.history_file = base_dir / PATHS["DATA_DIR"] / "historial_cotizaciones.csv"

    def save_quote_history(
        self,
        client_data: Dict[str, str],
        products_data: List[Dict[str, Union[str, float, int]]],
        quote_date: datetime
    ) -> bool:
        try:
            # Implementation of save logic
            return True
        except Exception:
            return False

    def get_quote_history(self) -> pd.DataFrame:
        if not self.history_file.exists():
            return pd.DataFrame()
        return pd.read_csv(self.history_file)
