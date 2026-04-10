# 5ESOFT-B_AEP
# ObservaAção - Sistema de Solicitações Públicas

Sistema desenvolvido para a AEP do 1º Bimestre - Engenharia de Software.

##  Requisitos Atendidos

### IHC - Perfis e Personas
-  3 perfis definidos (Cidadão baixa familiaridade digital, Cidadão vulnerável, Servidor público)
-  9 personas detalhadas com contexto, dores, objetivos e medos

### POO - Versão Beta
-  Classes bem definidas: Solicitacao, Usuario, HistoricoStatus, Categoria, FilaAtendimento
-  Operações: criar, listar, buscar por protocolo, atualizar status, registrar comentário
-  Persistência em arquivo JSON

### Clean Code - 3 Funções Documentadas
1. `criar_solicitacao()` - SRP e Nomes Significativos
2. `atualizar_status()` - Extração de Método
3. `buscar_por_protocolo()` - Fail Fast e Exceções Personalizadas

##  Como Executar

### Pré-requisitos
- Python 3.8 ou superior

### Instalação
```bash
# Clone ou baixe o projeto
cd observacao

# Execute o sistema
python main.py
