from typing import Dict, Callable

from app.models.conversion_factors import ConversionFactor

class TransformerRegistry:
    
    def __init__(self):
        self.registry:Dict[str, Callable[[str], list[ConversionFactor]]] = {}

    def register(self, country_code:str, transformer:Callable[[str], list[ConversionFactor]]) -> None:
        self.registry[country_code.lower()] = transformer

    def get(self, country_code:str) -> Callable[[str], list[ConversionFactor]]:
        return self.registry[country_code.lower()]
    
registry = TransformerRegistry()