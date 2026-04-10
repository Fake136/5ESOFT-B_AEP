"""
Geração de protocolos únicos.
Prática Clean Code: Função pura com responsabilidade única.
"""

import random
import string
from datetime import datetime


def gerar_protocolo_unico() -> str:
    """
    Gera protocolo único no formato: OBS-AAAAMMDD-XXXX
    
    Exemplo: OBS-20260410-A7K2
    
    Returns:
        String com protocolo único
    """
    data_atual = datetime.now()
    data_str = data_atual.strftime("%Y%m%d")
    
    # Gera 4 caracteres alfanuméricos aleatórios
    sufixo = ''.join(random.choices(
        string.ascii_uppercase + string.digits, 
        k=4
    ))
    
    return f"OBS-{data_str}-{sufixo}"


def validar_formato_protocolo(protocolo: str) -> bool:
    """Valida se string segue formato de protocolo."""
    if not protocolo or len(protocolo) != 17:
        return False
    
    partes = protocolo.split('-')
    if len(partes) != 3:
        return False
    
    prefixo, data, sufixo = partes
    return (
        prefixo == "OBS" and
        len(data) == 8 and data.isdigit() and
        len(sufixo) == 4
    )