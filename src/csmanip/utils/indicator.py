INDICATOR_MAP = {
    "Precipitation": 3,
    'Maximum temperature': 4,
    'Minimum temperature': 5
}

def get_indicator_code(indicator_name: str) -> int:
    return INDICATOR_MAP.get(indicator_name, -1)  # Retorna -1 se não encontrado