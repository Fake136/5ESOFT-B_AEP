"""
Classes de usuários do sistema.
Prática Clean Code: Hierarquia clara com comportamentos específicos.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


@dataclass
class Usuario(ABC):
    """Classe base para todos os usuários."""
    
    nome: str
    email: str
    telefone: Optional[str] = None
    ativo: bool = True
    
    @abstractmethod
    def get_tipo(self) -> str:
        """Retorna o tipo do usuário."""
        pass
    
    @abstractmethod
    def pode_atualizar_status(self) -> bool:
        """Verifica se pode alterar status de solicitações."""
        pass


@dataclass
class Cidadao(Usuario):
    """Cidadão que registra solicitações."""
    
    nivel_familiaridade_digital: str = "medio"  # baixo, medio, alto
    receio_retaliacao: bool = False
    
    def get_tipo(self) -> str:
        return "Cidadão"
    
    def pode_atualizar_status(self) -> bool:
        return False  # Cidadão não altera status
    
    def precisa_anonimato(self) -> bool:
        """Verifica se o perfil sugere necessidade de anonimato."""
        return self.receio_retaliacao


@dataclass
class ServidorPublico(Usuario):
    """Servidor que atende solicitações."""
    
    matricula: str = ""
    departamento: str = ""
    cargo: str = ""
    
    def get_tipo(self) -> str:
        return "Servidor Público"
    
    def pode_atualizar_status(self) -> bool:
        return True
    
    def pode_gerar_relatorios(self) -> bool:
        """Verifica se tem permissão para relatórios."""
        return "gestor" in self.cargo.lower() or "coordenador" in self.cargo.lower()


@dataclass
class Gestor(ServidorPublico):
    """Gestor com permissões elevadas."""
    
    def __post_init__(self):
        if not self.cargo:
            self.cargo = "Gestor"
    
    def get_tipo(self) -> str:
        return "Gestor"
    
    def pode_priorizar(self) -> bool:
        """Pode alterar prioridade de solicitações."""
        return True
    
    def pode_encerrar(self) -> bool:
        """Pode encerrar solicitações."""
        return True