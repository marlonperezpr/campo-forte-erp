# Objetivo

Este documento descreve a arquitetura do ERP Campo Forte.

Seu objetivo é definir como a aplicação será organizada internamente, estabelecendo responsabilidades dos módulos, estrutura do projeto e convenções utilizadas durante o desenvolvimento.

A arquitetura foi projetada priorizando simplicidade, baixo acoplamento, alta coesão e facilidade de manutenção.

# Visão Geral

Usuário
↓
Django
↓
Apps do Sistema
↓
PostgreSQL

# Organização do Projeto

A aplicação será dividida em apps Django, onde cada app representa um contexto de negócio.

Apps previstos:

- core
- accounts
- catalog
- purchases
- inventory
- sales
- finance
- audit

# Stack Tecnologica

Python

Django

Django REST Framework

PostgreSQL

Docker

Git

Pytest

# Estrutura do Projeto e Responsabilidades

## core

**Responsável por:** configurações compartilhadas.

### Exemplos

- Configurações globais
- Classes base
- Utilitários
- Mixins
- Permissões comuns

> Não conterá regras de negócio.

---

## cadastros

**Responsável por:** dados cadastrais do sistema.

### Entidades

- Usuario
- Cliente
- Fornecedor
- Produto
- ProdutoFornecedor

### Responsabilidades

- Cadastro
- Alteração
- Consulta
- Ativação e desativação

---

## compras

**Responsável por:** processo de compra.

### Entidades

- Compra
- ItemCompra

### Responsabilidades

- Registrar compras
- Atualizar custo médio
- Solicitar movimentação de estoque

> O módulo Compras não altera o estoque diretamente.

---

## estoque

**Responsável por:** controle de estoque.

### Entidades

- MovimentacaoEstoque

### Responsabilidades

- Registrar entradas
- Registrar saídas
- Registrar ajustes
- Calcular saldo atual

> Toda movimentação de estoque passa por este módulo.

---

## vendas

**Responsável por:** processo de venda.

### Entidades

- Venda
- ItemVenda
- PagamentoVenda

### Responsabilidades

- Registrar vendas
- Aplicar descontos
- Validar estoque
- Gerar Contas a Receber quando houver fiado
- Solicitar movimentação de estoque

---

## financeiro

**Responsável por:** controle financeiro.

### Entidades

- Caixa
- ContaReceber
- MovimentoContaReceber
- ContaPagar

### Responsabilidades

- Controle do caixa
- Controle de fiados
- Baixa de pagamentos
- Contas a pagar

---

## auditoria

**Responsável por:** histórico do sistema.

### Entidades

- LogAuditoria

### Responsabilidades

- Registrar ações dos usuários
- Permitir rastreabilidade

# Comunicação entre Módulos

Os módulos do sistema devem possuir baixo acoplamento.

Cada módulo é responsável apenas pelas suas próprias regras de negócio.

Quando uma operação depender de outro módulo, ela deverá solicitar que o módulo responsável execute a ação.

Exemplos:

- Compras solicitam movimentações ao módulo Estoque.
- Vendas solicitam movimentações ao módulo Estoque.
- Vendas solicitam a criação de Contas a Receber ao módulo Financeiro.
- Auditoria registra as ações executadas pelos demais módulos.

erp-campo-forte/

docs/

config/

apps/
core/
cadastros/
compras/
estoque/
vendas/
financeiro/
auditoria/

requirements/

docker/

manage.py

# Decisões Arquiteturais

- A aplicação será organizada em apps Django por contexto de negócio.
- Cada app será responsável apenas por suas próprias regras de negócio.
- O módulo Estoque será responsável por todas as movimentações de estoque.
- O módulo Financeiro será responsável pelas contas a receber, contas a pagar e caixa.
- Alterações importantes serão registradas pelo módulo de Auditoria.
- O banco de dados utilizado será PostgreSQL.

# Estrutura Física do Projeto

A estrutura de diretórios do ERP Campo Forte será organizada da seguinte forma:

```text
erp-campo-forte/
│
├── apps/
│   ├── core/
│   ├── accounts/
│   ├── catalog/
│   ├── purchases/
│   ├── inventory/
│   ├── sales/
│   ├── finance/
│   └── audit/
│
├── config/
├── docs/
├── docker/
├── requirements/
├── static/
├── media/
├── templates/
│
├── .env
├── .gitignore
├── docker-compose.yml
├── manage.py
└── README.md
```

Cada diretório possui uma responsabilidade específica, mantendo a organização do projeto e facilitando sua manutenção.

Apps técnicos em inglês; entidades e domínio em português
