"""
Validações reutilizáveis.
Prática Clean Code: Centraliza validações para evitar duplicação.
"""

from typing import Optional


class Validador:
    """Classe utilitária para validações."""
    
    TAMANHO_MINIMO_DESCRICAO = 10
    TAMANHO_MINIMO_LOCALIZACAO = 3
    TAMANHO_MINIMO_COMENTARIO = 5
    
    @staticmethod
    def validar_texto_nao_vazio(valor: Optional[str], nome_campo: str) -> str:
        """
        Valida se texto não está vazio.
        
        Raises:
            ValueError: Se texto for vazio ou None
        """
        if not valor or not valor.strip():
            raise ValueError(f"{nome_campo} é obrigatório")
        return valor.strip()
    
    @classmethod
    def validar_descricao(cls, descricao: str) -> str:
        """Valida campo descrição."""
        texto = cls.validar_texto_nao_vazio(descricao, "Descrição")
        if len(texto) < cls.TAMANHO_MINIMO_DESCRICAO:
            raise ValueError(
                f"Descrição deve ter pelo menos {cls.TAMANHO_MINIMO_DESCRICAO} caracteres"
            )
        return texto
    
    @classmethod
    def validar_localizacao(cls, localizacao: str) -> str:
        """Valida campo localização."""
        texto = cls.validar_texto_nao_vazio(localizacao, "Localização")
        if len(texto) < cls.TAMANHO_MINIMO_LOCALIZACAO:
            raise ValueError(
                f"Localização deve ter pelo menos {cls.TAMANHO_MINIMO_LOCALIZACAO} caracteres"
            )
        return texto
    
    @classmethod
    def validar_comentario(cls, comentario: str) -> str:
        """Valida comentário de atualização."""
        texto = cls.validar_texto_nao_vazio(comentario, "Comentário")
        if len(texto) < cls.TAMANHO_MINIMO_COMENTARIO:
            raise ValueError(
                f"Comentário deve ter pelo menos {cls.TAMANHO_MINIMO_COMENTARIO} caracteres"
            )
        return texto
    
    @staticmethod
    def validar_email(email: str) -> bool:
        """Validação básica de email."""
        return "@" in email and "." in email.split("@")[-1]