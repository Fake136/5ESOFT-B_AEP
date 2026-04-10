"""
Histórico de movimentações.
Prática Clean Code: Classe coesa com responsabilidade única.
"""

from datetime import datetime
from dataclasses import dataclass


@dataclass
class HistoricoStatus:
    """
    Registra uma mudança de status.
    
    Attributes:
        status_anterior: Status antes da mudança
        status_novo: Status atual
        data_hora: Momento da alteração
        responsavel: Quem fez a alteração
        comentario: Justificativa obrigatória
    """
    
    status_anterior: str
    status_novo: str
    data_hora: datetime
    responsavel: str
    comentario: str
    
    def __post_init__(self):
        """Validação após criação."""
        if not self.comentario or len(self.comentario.strip()) < 5:
            raise ValueError("Comentário deve ter pelo menos 5 caracteres")
    
    def to_dict(self) -> dict:
        """Converte para dicionário para serialização."""
        return {
            'status_anterior': self.status_anterior,
            'status_novo': self.status_novo,
            'data_hora': self.data_hora.isoformat(),
            'responsavel': self.responsavel,
            'comentario': self.comentario
        }
    
    @classmethod
    def from_dict(cls, dados: dict) -> 'HistoricoStatus':
        """Cria instância a partir de dicionário."""
        return cls(
            status_anterior=dados['status_anterior'],
            status_novo=dados['status_novo'],
            data_hora=datetime.fromisoformat(dados['data_hora']),
            responsavel=dados['responsavel'],
            comentario=dados['comentario']
        )
    
    def __str__(self) -> str:
        """Representação legível do histórico."""
        data_formatada = self.data_hora.strftime("%d/%m/%Y %H:%M")
        return f"[{data_formatada}] {self.status_anterior} → {self.status_novo} | {self.responsavel}: {self.comentario}"