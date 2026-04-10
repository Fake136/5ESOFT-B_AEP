"""
Fila de atendimento com priorização.
Prática Clean Code: Separação de responsabilidades - fila gerencia ordenação.
"""

from typing import List, Optional, Callable
from datetime import datetime

from .solicitacao import Solicitacao, StatusSolicitacao


class FilaAtendimento:
    """
    Gerencia a fila de solicitações com múltiplas estratégias de ordenação.
    
    Prática Clean Code: Métodos pequenos e focados em uma única tarefa.
    """
    
    def __init__(self):
        self._solicitacoes: List[Solicitacao] = []
    
    # ==================== OPERAÇÕES BÁSICAS ====================
    
    def adicionar(self, solicitacao: Solicitacao) -> None:
        """Adiciona solicitação à fila."""
        self._solicitacoes.append(solicitacao)
    
    def remover(self, protocolo: str) -> Optional[Solicitacao]:
        """Remove e retorna solicitação pelo protocolo."""
        for i, sol in enumerate(self._solicitacoes):
            if sol.protocolo == protocolo:
                return self._solicitacoes.pop(i)
        return None
    
    def obter(self, protocolo: str) -> Optional[Solicitacao]:
        """Busca solicitação sem remover."""
        return next(
            (s for s in self._solicitacoes if s.protocolo == protocolo), 
            None
        )
    
    def listar_todas(self) -> List[Solicitacao]:
        """Retorna cópia da lista."""
        return self._solicitacoes.copy()
    
    def quantidade(self) -> int:
        """Retorna total de solicitações."""
        return len(self._solicitacoes)
    
    def esta_vazia(self) -> bool:
        """Verifica se fila está vazia."""
        return len(self._solicitacoes) == 0
    
    # ==================== FILTROS ====================
    
    def filtrar_por_status(self, status: str) -> List[Solicitacao]:
        """Retorna solicitações com status específico."""
        return [s for s in self._solicitacoes if s.status == status]
    
    def filtrar_por_categoria(self, categoria) -> List[Solicitacao]:
        """Retorna solicitações de uma categoria."""
        return [s for s in self._solicitacoes if s.categoria == categoria]
    
    def filtrar_por_bairro(self, bairro: str) -> List[Solicitacao]:
        """Retorna solicitações de um bairro (busca parcial)."""
        bairro_lower = bairro.lower()
        return [
            s for s in self._solicitacoes 
            if bairro_lower in s.localizacao.lower()
        ]
    
    def filtrar_abertas(self) -> List[Solicitacao]:
        """Retorna solicitações não finalizadas."""
        finalizados = [StatusSolicitacao.RESOLVIDO, StatusSolicitacao.ENCERRADO]
        return [s for s in self._solicitacoes if s.status not in finalizados]
    
    def filtrar_atrasadas(self) -> List[Solicitacao]:
        """Retorna solicitações fora do prazo."""
        return [s for s in self.filtrar_abertas() if s.esta_atrasada()]
    
    # ==================== ORDENAÇÃO ====================
    
    def ordenar_por_prioridade(self) -> List[Solicitacao]:
        """
        Ordena por prioridade (1=Alta primeiro) e data.
        
        Prática Clean Code: Expressão lambda clara e documentada.
        """
        return sorted(
            self._solicitacoes,
            key=lambda s: (s.prioridade, s.data_criacao)
        )
    
    def ordenar_por_antiguidade(self) -> List[Solicitacao]:
        """Ordena por data de criação (mais antiga primeiro)."""
        return sorted(self._solicitacoes, key=lambda s: s.data_criacao)
    
    def ordenar_por_bairro(self) -> List[Solicitacao]:
        """Agrupa por bairro/localização."""
        return sorted(self._solicitacoes, key=lambda s: s.localizacao.lower())
    
    # ==================== ESTATÍSTICAS ====================
    
    def obter_estatisticas(self) -> dict:
        """Retorna estatísticas da fila."""
        total = len(self._solicitacoes)
        if total == 0:
            return {"total": 0}
        
        por_status = {}
        for s in self._solicitacoes:
            por_status[s.status] = por_status.get(s.status, 0) + 1
        
        atrasadas = len(self.filtrar_atrasadas())
        
        return {
            "total": total,
            "por_status": por_status,
            "atrasadas": atrasadas,
            "percentual_atraso": round((atrasadas / total) * 100, 2) if total > 0 else 0
        }