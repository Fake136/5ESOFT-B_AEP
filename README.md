# 5ESOFT-B_AEP

**Heitor Saueressig Mello** – RA: 24042002-2
**Luiz Eduardo Valério Semensato** – RA: 24150613-2
**Gabriel Lopes** – RA: 24224711-2

# ObservaAção – Sistema de Transparência e Atendimento de Demandas Públicas

Sistema desenvolvido para a AEP 2026 do curso de Engenharia de Software (ESOFT5S).

## Sobre o Projeto

O **ObservaAção** é uma solução digital criada para facilitar a comunicação entre cidadãos e órgãos públicos, promovendo maior transparência, organização e rastreabilidade das demandas da população.

O sistema permite que cidadãos registrem solicitações de serviços públicos, acompanhem o andamento por meio de protocolos e recebam retorno sobre o atendimento realizado. Além disso, servidores públicos podem gerenciar, priorizar e atualizar as demandas de forma organizada.

## Objetivos de Desenvolvimento Sustentável (ODS)

O projeto está alinhado aos seguintes objetivos da ONU:

* ODS 10 – Redução das Desigualdades
* ODS 11 – Cidades e Comunidades Sustentáveis
* ODS 16 – Paz, Justiça e Instituições Eficazes

---

# Evolução do Projeto

## 1º Bimestre – Versão Beta (Python)

### Requisitos Atendidos

#### IHC – Perfis e Personas

* 3 perfis definidos:

  * Cidadão com baixa familiaridade digital
  * Cidadão em situação de vulnerabilidade
  * Servidor público / gestor

* 9 personas detalhadas com:

  * Contexto social e digital
  * Objetivos
  * Dores
  * Restrições
  * Necessidades de acessibilidade
  * Medos

#### POO – Versão Beta

* Classes bem definidas:

  * Solicitacao
  * Usuario
  * HistoricoStatus
  * Categoria
  * FilaAtendimento

* Funcionalidades implementadas:

  * Criar solicitação
  * Listar solicitações
  * Buscar por protocolo
  * Atualizar status
  * Registrar comentários

* Persistência em arquivo JSON

#### Clean Code – Funções Documentadas

1. `criar_solicitacao()`

   * Single Responsibility Principle (SRP)
   * Nomes significativos

2. `atualizar_status()`

   * Extração de método
   * Responsabilidade única

3. `buscar_por_protocolo()`

   * Fail Fast
   * Exceções personalizadas

---

# 2º Bimestre – Evolução para Spring Boot

A aplicação foi migrada para Java Spring Boot, adotando arquitetura em camadas para melhorar organização, manutenção e escalabilidade.

## Arquitetura Implementada

* Controller
* Service
* Repository
* Model

## Classes Principais

### Controller

* `SolicitacaoController`

### Service

* `SolicitacaoService`

### Repository

* `SolicitacaoRepository`

### Model

* `Solicitacao`
* `HistoricoStatus`

## Funcionalidades Implementadas

### Cidadão

* Registrar solicitação
* Registrar solicitação anônima
* Consultar protocolo
* Acompanhar status
* Visualizar histórico

### Gestor / Atendente

* Visualizar demandas
* Atualizar status
* Registrar comentários obrigatórios
* Consultar histórico completo

## Fluxo de Status

```text
ABERTO
 ↓
TRIAGEM
 ↓
EM EXECUÇÃO
 ↓
RESOLVIDO
 ↓
ENCERRADO
```

## Endpoints Disponíveis

### Criar Solicitação

```http
POST /api/solicitacoes
```

### Buscar por Protocolo

```http
GET /api/solicitacoes/protocolo/{protocolo}
```

### Listar Solicitações

```http
GET /api/solicitacoes
```

### Atualizar Status

```http
PUT /api/solicitacoes/{id}/status
```

---

# Wireframes e IHC

O sistema foi projetado utilizando abordagem **Mobile First**, priorizando:

* Acessibilidade
* Alto contraste
* Linguagem simples
* Botões grandes
* Navegação intuitiva
* Usuários com baixa familiaridade digital

## Princípios Aplicados

* Heurísticas de Nielsen
* Lei de Fitts
* Lei de Hick-Hyman
* Princípios da Gestalt
* Diretrizes de acessibilidade WCAG

---

# Qualidade e Manutenção

Foi realizada análise estática do código utilizando o **Inspect Code** do IntelliJ IDEA.

## Resultados Encontrados

* 11 Java Warnings
* 8 ocorrências de redundância de declaração
* 3 alertas de Nullability
* 110 observações de ortografia

## Melhorias Identificadas

* Implementação de Bean Validation
* Tratamento avançado de exceções
* Uso de Enum para status
* Testes automatizados
* Integração com banco de dados PostgreSQL

---

# Tecnologias Utilizadas

## Backend

* Java 21
* Spring Boot
* Maven
* Lombok

## Ferramentas

* IntelliJ IDEA
* Postman
* GitHub

---

# Como Executar o Projeto

## Pré-requisitos

* Java 21 ou superior
* Maven instalado

## Clonar o Repositório

```bash
git clone https://github.com/Fake136/5ESOFT-B_AEP.git
```

## Acessar a Pasta do Projeto

```bash
cd 5ESOFT-B_AEP
```

## Executar a Aplicação

```bash
mvn spring-boot:run
```

A aplicação será iniciada em:

```text
http://localhost:8080
```

---

# Conclusão

O ObservaAção foi desenvolvido para reduzir barreiras no acesso aos serviços públicos, aumentar a transparência das instituições e fortalecer a participação cidadã.

O projeto integra conceitos de Interação Humano-Computador, Programação Orientada a Objetos e Manutenção de Software, demonstrando a aplicação prática dos conhecimentos adquiridos ao longo da disciplina.

