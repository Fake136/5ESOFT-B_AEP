"""
Exceções personalizadas para tratamento explícito de erros.
Prática Clean Code: Fail Fast - erros são detectados e tratados imediatamente.
"""


class ProtocoloNaoEncontradoError(Exception):
    """Exceção quando protocolo não existe no sistema."""
    
    def __init__(self, protocolo: str):
        self.protocolo = protocolo
        self.mensagem = f"Protocolo '{protocolo}' não encontrado no sistema."
        super().__init__(self.mensagem)


class ValidacaoError(Exception):
    """Exceção para erros de validação de campos."""
    
    def __init__(self, campo: str, motivo: str):
        self.campo = campo
        self.motivo = motivo
        self.mensagem = f"Erro no campo '{campo}': {motivo}"
        super().__init__(self.mensagem)


class PermissaoError(Exception):
    """Exceção para tentativas de acesso não autorizado."""
    
    def __init__(self, acao: str):
        self.acao = acao
        self.mensagem = f"Permissão negada para: {acao}"
        super().__init__(self.mensagem)