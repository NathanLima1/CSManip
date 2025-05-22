INDICATOR_MAP = {
    'Precipitação': 3,
    'Temperatura máxima': 4,
    'Temperatura mínima': 5
}

def get_indicator_code(indicator_name: str) -> int:
    return INDICATOR_MAP.get(indicator_name, -1)  # Retorna -1 se não encontrado