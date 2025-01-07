"""Core interfaces for the application."""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
import pandas as pd


class DataProvider(ABC):
    """Interface for data access operations."""

    @abstractmethod
    def get_inventory_data(self) -> pd.DataFrame:
        """Get inventory data.

        Returns:
            pd.DataFrame: The inventory data
        """
        pass

    @abstractmethod
    def get_systems_data(self) -> pd.DataFrame:
        """Get systems data.

        Returns:
            pd.DataFrame: The systems data
        """
        pass

    @abstractmethod
    def get_brands_data(self) -> pd.DataFrame:
        """Get brands data.

        Returns:
            pd.DataFrame: The brands data
        """
        pass


class PDFGeneratorInterface(ABC):
    """Interface for PDF generation operations."""

    @abstractmethod
    def generate_quote(self,
        client_data: Dict[str, str],
        products_data: List[Dict[str, Union[str, float, int]]],
        quote_date: datetime,
        output_path: str
    ) -> bool:
        """Generate a quote PDF.

        Args:
            client_data: Dictionary containing client information
            products_data: List of dictionaries containing product information
            quote_date: Date of the quote
            output_path: Path where to save the PDF

        Returns:
            bool: True if generation was successful, False otherwise
        """
        pass


class HistoryManager(ABC):
    """Interface for managing quote history."""

    @abstractmethod
    def save_quote_history(self,
        client_data: Dict[str, str],
        products_data: List[Dict[str, Union[str, float, int]]],
        quote_date: datetime
    ) -> bool:
        """Save quote to history.

        Args:
            client_data: Dictionary containing client information
            products_data: List of dictionaries containing product information
            quote_date: Date of the quote

        Returns:
            bool: True if save was successful, False otherwise
        """
        pass

    @abstractmethod
    def get_quote_history(self) -> pd.DataFrame:
        """Get quote history.

        Returns:
            pd.DataFrame: The quote history data
        """
        pass
