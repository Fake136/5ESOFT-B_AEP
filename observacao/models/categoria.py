"""
Categorias de solicitação.
Prática Clean Code: Enumeração clara evita strings mágicas.
"""

from enum import Enum


class Categoria(Enum):
    """Categorias de serviços públicos disponíveis."""
    
    ILUMINACAO = "Iluminação Pública"
    BURACO = "Buraco na Via"
    LIMPEZA = "Limpeza e Zeladoria"
    SAUDE = "Saúde Pública"
    SEGURANCA = "Segurança"
    COLETA_LIXO = "Coleta de Lixo"
    AGUA_ESGOTO = "Água e Esgoto"
    PODA_ARVORE = "Poda de Árvore"
    SINALIZACAO = "Sinalização de Trânsito"
    OUTROS = "Outros"
    
    @classmethod
    def listar_todas(cls) -> list:
        """Retorna lista de todas as categorias para exibição."""
        return [c for c in cls]
    
    @classmethod
    def obter_por_indice(cls, indice: int):
        """Obtém categoria por índice numérico."""
        categorias = list(cls)
        if 0 <= indice < len(categorias):
            return categorias[indice]
        return None