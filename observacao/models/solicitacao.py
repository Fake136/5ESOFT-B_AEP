"""
Classe principal de Solicitação.
Prática Clean Code: Responsabilidade única - apenas dados e comportamento da solicitação.
"""

from datetime import datetime
from typing import List, Optional
from dataclasses import dataclass, field

from .historico import HistoricoStatus
from .categoria import Categoria


class StatusSolicitacao:
    """Constantes de status para evitar strings mágicas."""
    
    ABERTO = "Aberto"
    TRIAGEM = "Em Triagem"
    EM_EXECUCAO = "Em Execução"
    RESOLVIDO = "Resolvido"
    ENCERRADO = "Encerrado"


@dataclass
class Solicitacao:
    """
    Representa uma solicitação de serviço público.
    
    Prática Clean Code: Nomes significativos e estrutura clara.
    """
    
    # Identificação
    protocolo: str
    data_criacao: datetime
    
    # Conteúdo
    categoria: Categoria
    descricao: str
    localizacao: str
    anexo: Optional[str] = None  # Caminho do arquivo, se houver
    
    # Identificação do cidadão
    anonimo: bool = True
    nome_solicitante: Optional[str] = None
    contato_solicitante: Optional[str] = None
    
    # Status e prioridade
    status: str = field(default=StatusSolicitacao.ABERTO)
    prioridade: int = 2  # 1=Alta, 2=Média, 3=Baixa
    
    # Histórico
    historico: List[HistoricoStatus] = field(default_factory=list)
    
    # Controle interno
    _responsavel_atual: Optional[str] = None
    
    def __post_init__(self):
        """Validações após criação."""
        if not self.descricao or len(self.descricao.strip()) < 10:
            raise ValueError("Descrição deve ter pelo menos 10 caracteres")
        
        if not self.localizacao or len(self.localizacao.strip()) < 3:
            raise ValueError("Localização deve ter pelo menos 3 caracteres")
        
        # Se não for anônimo, deve ter dados do solicitante
        if not self.anonimo:
            if not self.nome_solicitante:
                raise ValueError("Solicitação identificada requer nome do solicitante")
    
    # ==================== MÉTODOS DE STATUS ====================
    
    def pode_ser_atualizado(self) -> bool:
        """Verifica se o status ainda pode ser alterado."""
        return self.status not in [StatusSolicitacao.ENCERRADO, StatusSolicitacao.RESOLVIDO]
    
    def atualizar_status(
        self, 
        novo_status: str, 
        responsavel: str, 
        comentario: str
    ) -> HistoricoStatus:
        """
        Atualiza status registrando no histórico.
        
        Prática Clean Code: Método com responsabilidade única bem definida.
        """
        if not self.pode_ser_atualizado():
            raise ValueError(f"Não é possível alterar status de solicitação {self.status}")
        
        if not comentario or len(comentario.strip()) < 5:
            raise ValueError("Comentário obrigatório (mínimo 5 caracteres)")
        
        status_anterior = self.status
        self.status = novo_status
        self._responsavel_atual = responsavel
        
        # Cria registro histórico
        movimentacao = HistoricoStatus(
            status_anterior=status_anterior,
            status_novo=novo_status,
            data_hora=datetime.now(),
            responsavel=responsavel,
            comentario=comentario
        )
        
        self.historico.append(movimentacao)
        return movimentacao
    
    # ==================== MÉTODOS DE CONSULTA ====================
    
    def obter_sla_dias(self) -> int:
        """Retorna prazo SLA em dias baseado na prioridade."""
        sla_map = {1: 3, 2: 7, 3: 15}  # Alta, Média, Baixa
        return sla_map.get(self.prioridade, 7)
    
    def esta_atrasada(self) -> bool:
        """Verifica se a solicitação está dentro do prazo."""
        if self.status in [StatusSolicitacao.RESOLVIDO, StatusSolicitacao.ENCERRADO]:
            return False
        
        dias_passados = (datetime.now() - self.data_criacao).days
        return dias_passados > self.obter_sla_dias()
    
    def obter_tempo_aberto(self) -> str:
        """Retorna tempo decorrido desde a criação."""
        delta = datetime.now() - self.data_creacao
        dias = delta.days
        horas = delta.seconds // 3600
        
        if dias > 0:
            return f"{dias} dias e {horas} horas"
        return f"{horas} horas"
    
    # ==================== SERIALIZAÇÃO ====================
    
    def to_dict(self) -> dict:
        """Converte para dicionário."""
        return {
            'protocolo': self.protocolo,
            'data_criacao': self.data_criacao.isoformat(),
            'categoria': self.categoria.name,
            'descricao': self.descricao,
            'localizacao': self.localizacao,
            'anexo': self.anexo,
            'anonimo': self.anonimo,
            'nome_solicitante': self.nome_solicitante,
            'contato_solicitante': self.contato_solicitante,
            'status': self.status,
            'prioridade': self.prioridade,
            'historico': [h.to_dict() for h in self.historico]
        }
    
    @classmethod
    def from_dict(cls, dados: dict) -> 'Solicitacao':
        """Cria instância a partir de dicionário."""
        solicitacao = cls(
            protocolo=dados['protocolo'],
            data_criacao=datetime.fromisoformat(dados['data_criacao']),
            categoria=Categoria[dados['categoria']],
            descricao=dados['descricao'],
            localizacao=dados['localizacao'],
            anexo=dados.get('anexo'),
            anonimo=dados['anonimo'],
            nome_solicitante=dados.get('nome_solicitante'),
            contato_solicitante=dados.get('contato_solicitante'),
            status=dados['status'],
            prioridade=dados.get('prioridade', 2)
        )
        
        # Restaura histórico
        for hist_dict in dados.get('historico', []):
            solicitacao.historico.append(HistoricoStatus.from_dict(hist_dict))
        
        return solicitacao
    
    def __str__(self) -> str:
        """Representação legível."""
        tipo = "Anônima" if self.anonimo else "Identificada"
        return f"[{self.protocolo}] {self.categoria.value} - {self.status} ({tipo})"
    
    def __repr__(self) -> str:
        """Representação técnica."""
        return f"Solicitacao(protocolo='{self.protocolo}', status='{self.status}')"