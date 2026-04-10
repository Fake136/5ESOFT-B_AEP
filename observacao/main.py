#!/usr/bin/env python3
"""
Sistema ObservaAção - Versão Beta
Aplicação CLI para gestão de solicitações públicas.

Prática Clean Code: Interface separada da lógica de negócio.
"""

import os
import sys
from typing import Optional

# Adiciona diretório atual ao path para imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.servico_solicitacoes import ServicoSolicitacoes
from models.categoria import Categoria
from models.solicitacao import StatusSolicitacao
from models.usuario import Cidadao, ServidorPublico
from exceptions import ProtocoloNaoEncontradoError, ValidacaoError


class InterfaceObservacao:
    """
    Interface de linha de comando do sistema.
    
    Prática Clean Code: Separação clara entre UI e lógica de negócio.
    """
    
    def __init__(self):
        self.servico = ServicoSolicitacoes()
        self.usuario_atual: Optional[Cidadao | ServidorPublico] = None
    
    def limpar_tela(self):
        """Limpa a tela do terminal."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def exibir_cabecalho(self, titulo: str):
        """Exibe cabeçalho formatado."""
        print("\n" + "=" * 60)
        print(f"  {titulo}")
        print("=" * 60)
    
    def exibir_menu_principal(self):
        """Menu principal do sistema."""
        while True:
            self.limpar_tela()
            self.exibir_cabecalho("OBSERVAÇÃO - Sistema de Solicitações Públicas")
            
            print("\n  [1] 📝 Nova Solicitação (Cidadão)")
            print("  [2] 🔍 Acompanhar Solicitação")
            print("  [3] 👤 Área do Servidor/Gestor")
            print("  [4] 📊 Estatísticas do Sistema")
            print("  [0] 🚪 Sair")
            
            opcao = input("\n  Escolha uma opção: ").strip()
            
            if opcao == "1":
                self.tela_nova_solicitacao()
            elif opcao == "2":
                self.tela_acompanhar_solicitacao()
            elif opcao == "3":
                self.tela_area_servidor()
            elif opcao == "4":
                self.tela_estatisticas()
            elif opcao == "0":
                print("\n  Obrigado por usar o ObservaAção!")
                break
            else:
                input("\n  ❌ Opção inválida. Pressione ENTER...")
    
    def tela_nova_solicitacao(self):
        """Tela de criação de nova solicitação."""
        self.limpar_tela()
        self.exibir_cabecalho("NOVA SOLICITAÇÃO")
        
        print("\n  📋 Categorias disponíveis:")
        for i, cat in enumerate(Categoria.listar_todas(), 1):
            print(f"     [{i}] {cat.value}")
        
        try:
            # Seleção de categoria
            while True:
                try:
                    cat_opcao = int(input("\n  Escolha a categoria (número): ")) - 1
                    categoria = Categoria.obter_por_indice(cat_opcao)
                    if categoria:
                        break
                    print("  ❌ Categoria inválida.")
                except ValueError:
                    print("  ❌ Digite um número válido.")
            
            # Descrição
            print("\n  📝 Descreva o problema (mínimo 10 caracteres):")
            descricao = input("  > ").strip()
            
            # Localização
            print("\n  📍 Informe a localização (bairro, rua, ponto de referência):")
            localizacao = input("  > ").strip()
            
            # Anonimato
            print("\n  👤 Deseja registrar como anônimo?")
            print("     [1] Sim - Proteger minha identidade")
            print("     [2] Não - Quero me identificar")
            anonimo_opcao = input("  > ").strip()
            anonimo = anonimo_opcao == "1"
            
            nome = None
            contato = None
            if not anonimo:
                print("\n  Nome completo:")
                nome = input("  > ").strip()
                print("\n  Contato (telefone/email):")
                contato = input("  > ").strip()
            
            # Prioridade
            print("\n  ⚠️  Nível de prioridade:")
            print("     [1] Alta - Risco à segurança/saúde")
            print("     [2] Média - Problema importante")
            print("     [3] Baixa - Melhoria/Manutenção")
            try:
                prioridade = int(input("  > ").strip())
                if prioridade not in [1, 2, 3]:
                    prioridade = 2
            except ValueError:
                prioridade = 2
            
            # Confirmação
            print(f"\n  📌 Resumo da solicitação:")
            print(f"     Categoria: {categoria.value}")
            print(f"     Local: {localizacao}")
            print(f"     Anônimo: {'Sim' if anonimo else 'Não'}")
            print(f"     Prioridade: {'Alta' if prioridade == 1 else 'Média' if prioridade == 2 else 'Baixa'}")
            
            confirmar = input("\n  Confirmar envio? (S/N): ").strip().upper()
            
            if confirmar == 'S':
                solicitacao = self.servico.criar_solicitacao(
                    categoria=categoria,
                    descricao=descricao,
                    localizacao=localizacao,
                    anonimo=anonimo,
                    nome_solicitante=nome,
                    contato_solicitante=contato,
                    prioridade=prioridade
                )
                
                print(f"\n  ✅ SOLICITAÇÃO REGISTRADA COM SUCESSO!")
                print(f"  🎫 PROTOCOLO: {solicitacao.protocolo}")
                print(f"\n  💾 Guarde este número para acompanhar o andamento.")
            else:
                print("\n  ❌ Solicitação cancelada.")
                
        except (ValidacaoError, ValueError) as e:
            print(f"\n  ❌ Erro de validação: {e}")
        except Exception as e:
            print(f"\n  ❌ Erro inesperado: {e}")
        
        input("\n  Pressione ENTER para voltar...")
    
    def tela_acompanhar_solicitacao(self):
        """Tela de acompanhamento por protocolo."""
        self.limpar_tela()
        self.exibir_cabecalho("ACOMPANHAR SOLICITAÇÃO")
        
        protocolo = input("\n  🎫 Digite o número do protocolo: ").strip().upper()
        
        try:
            solicitacao = self.servico.buscar_por_protocolo(protocolo)
            
            print(f"\n  📋 DETALHES DA SOLICITAÇÃO")
            print(f"  {'─' * 50}")
            print(f"  Protocolo: {solicitacao.protocolo}")
            print(f"  Categoria: {solicitacao.categoria.value}")
            print(f"  Status: {solicitacao.status}")
            print(f"  Data: {solicitacao.data_criacao.strftime('%d/%m/%Y %H:%M')}")
            
            if solicitacao.esta_atrasada():
                print(f"  ⚠️  STATUS: ATRASADA (SLA: {solicitacao.obter_sla_dias()} dias)")
            
            print(f"\n  📍 Local: {solicitacao.localizacao}")
            print(f"  📝 Descrição: {solicitacao.descricao}")
            
            tipo = "Anônima" if solicitacao.anonimo else "Identificada"
            print(f"\n  👤 Tipo: {tipo}")
            
            # Histórico
            print(f"\n  📜 HISTÓRICO DE MOVIMENTAÇÕES:")
            print(f"  {'─' * 50}")
            
            if not solicitacao.historico:
                print("  Aguardando primeira movimentação...")
            else:
                for mov in solicitacao.historico:
                    print(f"  • {mov}")
            
            # Próximos passos
            print(f"\n  🔄 PRÓXIMOS PASSOS:")
            fluxo = ["Aberto", "Em Triagem", "Em Execução", "Resolvido", "Encerrado"]
            try:
                idx_atual = fluxo.index(solicitacao.status)
                if idx_atual < len(fluxo) - 1:
                    print(f"  Próximo status: {fluxo[idx_atual + 1]}")
                else:
                    print("  Solicitação finalizada.")
            except ValueError:
                pass
                
        except ProtocoloNaoEncontradoError as e:
            print(f"\n  ❌ {e}")
            print("  💡 Dica: Verifique se digitou o protocolo corretamente.")
        
        input("\n  Pressione ENTER para voltar...")
    
    def tela_area_servidor(self):
        """Área restrita para servidores."""
        self.limpar_tela()
        self.exibir_cabecalho("ÁREA DO SERVIDOR/GESTOR")
        
        # Simulação de login simples
        print("\n  🔐 Identificação:")
        nome = input("  Nome: ").strip()
        matricula = input("  Matrícula: ").strip()
        
        if not nome or not matricula:
            print("\n  ❌ Dados obrigatórios.")
            input("\n  Pressione ENTER...")
            return
        
        while True:
            self.limpar_tela()
            self.exibir_cabecalho(f"PAINEL DO SERVIDOR - {nome}")
            
            print("\n  [1] 📋 Listar todas as solicitações")
            print("  [2] 🔥 Ver prioridades (alta prioridade/atrasadas)")
            print("  [3] 🔍 Buscar por protocolo")
            print("  [4] ✏️  Atualizar status de solicitação")
            print("  [5] 📝 Adicionar comentário")
            print("  [0] ↩️  Voltar ao menu principal")
            
            opcao = input("\n  Escolha: ").strip()
            
            if opcao == "1":
                self._listar_todas_solicitacoes()
            elif opcao == "2":
                self._listar_prioridades()
            elif opcao == "3":
                self._buscar_para_atualizar(nome)
            elif opcao == "4":
                self._atualizar_status(nome)
            elif opcao == "5":
                self._adicionar_comentario(nome)
            elif opcao == "0":
                break
            else:
                input("  ❌ Opção inválida. ENTER...")
    
    def _listar_todas_solicitacoes(self):
        """Lista todas as solicitações com filtros."""
        self.limpar_tela()
        self.exibir_cabecalho("LISTA DE SOLICITAÇÕES")
        
        print("\n  Filtros (deixe em branco para ignorar):")
        status = input("  Status (Aberto/Em Triagem/Em Execução/Resolvido/Encerrado): ").strip()
        
        solicitacoes = self.servico.listar_solicitacoes(
            filtro_status=status if status else None,
            ordenar_por="prioridade"
        )
        
        print(f"\n  📊 Total encontrado: {len(solicitacoes)}")
        print(f"  {'─' * 70}")
        
        if not solicitacoes:
            print("  Nenhuma solicitação encontrada.")
        else:
            for s in solicitacoes:
                prioridade_str = "🔴" if s.prioridade == 1 else "🟡" if s.prioridade == 2 else "🟢"
                atraso = " [ATRASADA]" if s.esta_atrasada() else ""
                print(f"  {prioridade_str} [{s.protocolo}] {s.categoria.value}")
                print(f"      Status: {s.status}{atraso}")
                print(f"      Local: {s.localizacao[:40]}...")
                print(f"      Criado em: {s.data_criacao.strftime('%d/%m/%Y')}")
                print()
        
        input("  Pressione ENTER...")
    
    def _listar_prioridades(self):
        """Lista solicitações prioritárias."""
        self.limpar_tela()
        self.exibir_cabecalho("PRIORIDADES")
        
        todas = self.servico.listar_solicitacoes()
        prioridades = [s for s in todas if s.prioridade == 1 or s.esta_atrasada()]
        
        print(f"\n  🔴 ALTA PRIORIDADE OU ATRASADAS: {len(prioridades)}")
        print(f"  {'─' * 70}")
        
        for s in prioridades:
            tipo = "ALTA" if s.prioridade == 1 else "ATRASO"
            print(f"  [{tipo}] {s.protocolo} - {s.categoria.value}")
            print(f"       Status: {s.status} | Local: {s.localizacao}")
            print()
        
        input("  Pressione ENTER...")
    
    def _buscar_para_atualizar(self, responsavel: str):
        """Busca solicitação para visualização."""
        protocolo = input("\n  Protocolo para buscar: ").strip().upper()
        
        try:
            s = self.servico.buscar_por_protocolo(protocolo)
            print(f"\n  📋 {s}")
            print(f"  Descrição: {s.descricao}")
            print(f"  Histórico: {len(s.historico)} movimentações")
        except ProtocoloNaoEncontradoError as e:
            print(f"\n  ❌ {e}")
        
        input("\n  ENTER...")
    
    def _atualizar_status(self, responsavel: str):
        """Atualiza status de uma solicitação."""
        protocolo = input("\n  🎫 Protocolo: ").strip().upper()
        
        try:
            solicitacao = self.servico.buscar_por_protocolo(protocolo)
            
            print(f"\n  Status atual: {solicitacao.status}")
            print("\n  Novo status:")
            print("  [1] Em Triagem")
            print("  [2] Em Execução")
            print("  [3] Resolvido")
            print("  [4] Encerrado")
            
            op_status = input("  > ").strip()
            status_map = {
                "1": StatusSolicitacao.TRIAGEM,
                "2": StatusSolicitacao.EM_EXECUCAO,
                "3": StatusSolicitacao.RESOLVIDO,
                "4": StatusSolicitacao.ENCERRADO
            }
            
            if op_status not in status_map:
                print("  ❌ Opção inválida.")
                input("  ENTER...")
                return
            
            novo_status = status_map[op_status]
            
            print("\n  📝 Comentário obrigatório sobre a atualização:")
            comentario = input("  > ").strip()
            
            movimentacao = self.servico.atualizar_status(
                protocolo=protocolo,
                novo_status=novo_status,
                responsavel=responsavel,
                comentario=comentario
            )
            
            print(f"\n  ✅ Status atualizado com sucesso!")
            print(f"  📜 Registrado: {movimentacao}")
            
        except ProtocoloNaoEncontradoError as e:
            print(f"\n  ❌ {e}")
        except ValueError as e:
            print(f"\n  ❌ Erro: {e}")
        
        input("\n  ENTER...")
    
    def _adicionar_comentario(self, responsavel: str):
        """Adiciona comentário sem mudar status."""
        protocolo = input("\n  🎫 Protocolo: ").strip().upper()
        
        try:
            print("\n  📝 Comentário:")
            comentario = input("  > ").strip()
            
            self.servico.registrar_comentario(protocolo, responsavel, comentario)
            print("  ✅ Comentário registrado.")
            
        except ProtocoloNaoEncontradoError as e:
            print(f"\n  ❌ {e}")
        
        input("\n  ENTER...")
    
    def tela_estatisticas(self):
        """Exibe estatísticas do sistema."""
        self.limpar_tela()
        self.exibir_cabecalho("ESTATÍSTICAS DO SISTEMA")
        
        stats = self.servico.obter_estatisticas()
        
        print(f"\n  📊 Visão Geral:")
        print(f"  {'─' * 40}")
        print(f"  Total de solicitações: {stats['total']}")
        
        if stats['total'] > 0:
            print(f"\n  📈 Por Status:")
            for status, quantidade in stats['por_status'].items():
                print(f"     {status}: {quantidade}")
            
            print(f"\n  ⚠️  Atrasadas: {stats['atrasadas']}")
            print(f"  📉 Percentual de atraso: {stats['percentual_atraso']}%")
        
        input("\n  Pressione ENTER...")


def main():
    """Função principal."""
    try:
        app = InterfaceObservacao()
        app.exibir_menu_principal()
    except KeyboardInterrupt:
        print("\n\n  Programa interrompido pelo usuário.")
        sys.exit(0)


if __name__ == "__main__":
    main()