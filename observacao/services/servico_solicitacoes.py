"""
Serviço principal de solicitações.
Prática Clean Code: Separação de responsabilidades - serviço orquestra operações.
"""

import json
import os
from datetime import datetime
from typing import List, Optional, Dict

# Imports dos módulos do projeto
from models.solicitacao import Solicitacao, StatusSolicitacao
from models.fila import FilaAtendimento
from models.categoria import Categoria
from models.historico import HistoricoStatus
from utils.protocolo import gerar_protocolo_unico
from utils.validador import Validador
from exceptions import ProtocoloNaoEncontradoError, ValidacaoError


class ServicoSolicitacoes:
    """
    Serviço principal que gerencia todo o ciclo de vida das solicitações.
    
    Prática Clean Code: Métodos pequenos com nomes descritivos.
    """
    
    ARQUIVO_DADOS = "data/solicitacoes.json"
    
    def __init__(self):
        self.fila = FilaAtendimento()
        self._carregar_dados()
    
    # ==================== OPERAÇÕES CRUD ====================
    
    def criar_solicitacao(
        self,
        categoria: Categoria,
        descricao: str,
        localizacao: str,
        anonimo: bool = True,
        nome_solicitante: Optional[str] = None,
        contato_solicitante: Optional[str] = None,
        anexo: Optional[str] = None,
        prioridade: int = 2
    ) -> Solicitacao:
        """
        Cria nova solicitação com validação completa.
        
        Prática Clean Code: Single Responsibility - apenas cria, não valida tudo.
        """
        # Validações extraídas para métodos auxiliares
        self._validar_campos_obrigatorios(descricao, localizacao)
        
        # Geração de protocolo único
        protocolo = self._gerar_protocolo_unico()
        
        # Criação da solicitação
        solicitacao = Solicitacao(
            protocolo=protocolo,
            data_criacao=datetime.now(),
            categoria=categoria,
            descricao=descricao,
            localizacao=localizacao,
            anonimo=anonimo,
            nome_solicitante=nome_solicitante if not anonimo else None,
            contato_solicitante=contato_solicitante if not anonimo else None,
            anexo=anexo,
            prioridade=prioridade
        )
        
        # Persistência
        self._salvar_solicitacao(solicitacao)
        
        return solicitacao
    
    def buscar_por_protocolo(self, protocolo: str) -> Solicitacao:
        """
        Busca solicitação pelo protocolo.
        
        Prática Clean Code: Fail Fast - erro explícito ao invés de retornar None.
        """
        solicitacao = self.fila.obter(protocolo)
        
        if solicitacao is None:
            # Levanta exceção específica em vez de retornar None
            raise ProtocoloNaoEncontradoError(protocolo)
        
        return solicitacao
    
    def listar_solicitacoes(
        self,
        filtro_status: Optional[str] = None,
        filtro_categoria: Optional[Categoria] = None,
        ordenar_por: str = "prioridade"
    ) -> List[Solicitacao]:
        """
        Lista solicitações com filtros e ordenação.
        
        Prática Clean Code: Parâmetros opcionais claros.
        """
        resultado = self.fila.listar_todas()
        
        # Aplica filtros
        if filtro_status:
            resultado = [s for s in resultado if s.status == filtro_status]
        
        if filtro_categoria:
            resultado = [s for s in resultado if s.categoria == filtro_categoria]
        
        # Aplica ordenação
        if ordenar_por == "prioridade":
            resultado.sort(key=lambda s: (s.prioridade, s.data_criacao))
        elif ordenar_por == "data":
            resultado.sort(key=lambda s: s.data_criacao)
        elif ordenar_por == "bairro":
            resultado.sort(key=lambda s: s.localizacao)
        
        return resultado
    
    # ==================== ATUALIZAÇÃO DE STATUS ====================
    
    def atualizar_status(
        self,
        protocolo: str,
        novo_status: str,
        responsavel: str,
        comentario: str
    ) -> HistoricoStatus:
        """
        Atualiza status com registro de histórico.
        
        Prática Clean Code: Extração de método para registro de movimentação.
        """
        # Busca com tratamento de erro explícito
        solicitacao = self.buscar_por_protocolo(protocolo)
        
        # Validação do comentário
        Validador.validar_comentario(comentario)
        
        # Atualiza status (método extraído na classe Solicitacao)
        movimentacao = solicitacao.atualizar_status(
            novo_status=novo_status,
            responsavel=responsavel,
            comentario=comentario
        )
        
        # Persiste alterações
        self._persistir_dados()
        
        return movimentacao
    
    def registrar_comentario(
        self,
        protocolo: str,
        responsavel: str,
        comentario: str
    ) -> None:
        """
        Adiciona comentário sem mudar status.
        
        Prática Clean Code: Sobrecarga clara de intenção.
        """
        solicitacao = self.buscar_por_protocolo(protocolo)
        
        # Registra como "sem mudança de status"
        movimentacao = HistoricoStatus(
            status_anterior=solicitacao.status,
            status_novo=solicitacao.status,
            data_hora=datetime.now(),
            responsavel=responsavel,
            comentario=f"[COMENTÁRIO] {comentario}"
        )
        
        solicitacao.historico.append(movimentacao)
        self._persistir_dados()
    
    # ==================== MÉTODOS PRIVADOS (AUXILIARES) ====================
    
    def _validar_campos_obrigatorios(self, descricao: str, localizacao: str) -> None:
        """
        Valida campos obrigatórios.
        
        Prática Clean Code: Extração de método para clareza.
        """
        Validador.validar_descricao(descricao)
        Validador.validar_localizacao(localizacao)
    
    def _gerar_protocolo_unico(self) -> str:
        """
        Gera protocolo garantindo unicidade.
        
        Prática Clean Code: Método com responsabilidade única.
        """
        while True:
            protocolo = gerar_protocolo_unico()
            if self.fila.obter(protocolo) is None:
                return protocolo
    
    def _salvar_solicitacao(self, solicitacao: Solicitacao) -> None:
        """Adiciona à fila e persiste."""
        self.fila.adicionar(solicitacao)
        self._persistir_dados()
    
    # ==================== PERSISTÊNCIA ====================
    
    def _carregar_dados(self) -> None:
        """Carrega dados do arquivo JSON."""
        if not os.path.exists(self.ARQUIVO_DADOS):
            os.makedirs(os.path.dirname(self.ARQUIVO_DADOS), exist_ok=True)
            return
        
        try:
            with open(self.ARQUIVO_DADOS, 'r', encoding='utf-8') as f:
                dados = json.load(f)
                
            for item in dados:
                solicitacao = Solicitacao.from_dict(item)
                self.fila.adicionar(solicitacao)
                
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Aviso: Erro ao carregar dados: {e}")
    
    def _persistir_dados(self) -> None:
        """Salva todas as solicitações em arquivo."""
        dados = [s.to_dict() for s in self.fila.listar_todas()]
        
        os.makedirs(os.path.dirname(self.ARQUIVO_DADOS), exist_ok=True)
        
        with open(self.ARQUIVO_DADOS, 'w', encoding='utf-8') as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
    
    # ==================== ESTATÍSTICAS ====================
    
    def obter_estatisticas(self) -> Dict:
        """Retorna estatísticas do sistema."""
        return self.fila.obter_estatisticas()