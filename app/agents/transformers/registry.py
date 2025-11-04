from typing import Dict, Callable
import importlib
import pkgutil
import os
from pathlib import Path

from app.models.conversion_factors import ConversionFactor


class TransformerRegistry:
    def __init__(self):
        self.registry: Dict[str, Callable[[Path], list[ConversionFactor]]] = {}

    def register(
        self, country_code: str, transformer: Callable[[Path], list[ConversionFactor]]
    ) -> None:
        self.registry[country_code.lower()] = transformer

    def get(self, country_code: str) -> Callable[[Path], list[ConversionFactor]]:
        key = country_code.lower()
        if key not in self.registry:
            raise KeyError(
                f"No transformer registered for '{key}'. "
                f"Registered countries: {list(self.registry.keys())}"
            )
        return self.registry[key]

    def discover(self):
        package_dir = os.path.dirname(__file__)
        package_name = __package__  # e.g. "app.agents.transformers"

        for _, module_name, is_pkg in pkgutil.iter_modules([package_dir]):
            if not is_pkg and module_name != "registry":
                full_name = f"{package_name}.{module_name}"
                importlib.import_module(full_name)


registry = TransformerRegistry()
