# Modelagem de Dados

> **Versão:** 0.1.0  
> **Projeto:** ERP Campo Forte

---

# Índice

1. Objetivo
2. Convenções Gerais
3. Entidades
   - Cliente
   - Fornecedor
   - Produto
   - MovimentacaoEstoque
4. Relacionamentos
5. Pendências
6. Diagrama Entidade-Relacionamento (DER)

---

# Objetivo

Este documento descreve o modelo de dados do ERP Campo Forte, servindo como base para a implementação utilizando PostgreSQL e Django ORM.

As entidades aqui documentadas representam a tradução da modelagem de domínio para um modelo de dados consistente.

---

# Convenções Gerais

## Chave Primária

Todas as entidades utilizarão `BigAutoField` como chave primária.

---

## Auditoria

Todas as entidades possuirão os seguintes campos:

- created_at
- updated_at

---

## Exclusão Lógica

Entidades cadastrais utilizarão o campo `ativo`.

Entidades transacionais não utilizarão exclusão lógica.

---

## Convenções de Nomenclatura

### Modelos

Utilizar **PascalCase**.

Exemplos:

- Produto
- Cliente
- Fornecedor
- Venda
- ItemVenda

### Campos

Utilizar **snake_case**.

Exemplos:

- nome
- preco_venda
- codigo_barras
- created_at
- updated_at

Evitar abreviações sempre que possível.

Utilizar nomes descritivos.

---

# Entidades

## Cliente

### Objetivo

Representar clientes da Campo Forte para vendas, entregas, cobranças e controle de fiado.

### Campos

| Campo       | Obrigatório |
| ----------- | ----------- |
| id          | Sim         |
| nome        | Sim         |
| cpf_cnpj    | Não         |
| telefone    | Sim         |
| email       | Não         |
| endereco    | Não         |
| observacoes | Não         |
| ativo       | Sim         |
| created_at  | Sim         |
| updated_at  | Sim         |

### Regras

- Não pode ser excluído.
- Pode ser desativado.
- Cadastro não é obrigatório para vendas à vista.
- Cadastro é obrigatório para vendas fiado.
- Um cliente pode possuir várias vendas.
- Um cliente pode possuir várias contas a receber.

---

## Fornecedor

### Objetivo

Representar pessoas físicas ou jurídicas responsáveis pelo fornecimento dos produtos.

### Campos

| Campo         | Obrigatório |
| ------------- | ----------- |
| id            | Sim         |
| nome          | Sim         |
| nome_fantasia | Não         |
| cpf_cnpj      | Não         |
| telefone      | Sim         |
| email         | Não         |
| endereco      | Não         |
| observacoes   | Não         |
| ativo         | Sim         |
| created_at    | Sim         |
| updated_at    | Sim         |

### Regras

- Pode ser Pessoa Física ou Jurídica.
- Não pode ser excluído.
- Pode ser desativado.
- Um fornecedor pode fornecer vários produtos.
- Um fornecedor pode possuir várias compras.

---

## Produto

### Objetivo

Representar os produtos comercializados pela Campo Forte.

### Campos

| Campo          | Obrigatório |
| -------------- | ----------- |
| id             | Sim         |
| codigo         | Sim         |
| nome           | Sim         |
| codigo_barras  | Não         |
| unidade_medida | Sim         |
| preco_custo    | Sim         |
| preco_venda    | Sim         |
| preco_minimo   | Sim         |
| estoque_minimo | Não         |
| estoque_atual  | Sim         |
| ativo          | Sim         |
| created_at     | Sim         |
| updated_at     | Sim         |

### Unidade de Medida

- UN
- KG
- SC
- LT

### Regras

- Nome único.
- Código interno gerado automaticamente.
- Código de barras opcional.
- Todos os produtos controlam estoque.
- Produtos por unidade e por peso serão cadastrados separadamente.
- Não podem ser excluídos.
- Podem ser desativados.

---

## MovimentacaoEstoque

### Objetivo

Registrar todo o histórico de entradas, saídas e ajustes de estoque.

### Campos

| Campo          | Obrigatório |
| -------------- | ----------- |
| id             | Sim         |
| produto        | Sim         |
| tipo           | Sim         |
| quantidade     | Sim         |
| saldo_anterior | Sim         |
| saldo_atual    | Sim         |
| observacao     | Não         |
| created_at     | Sim         |

### Tipos de Movimentação

- Entrada por compra
- Saída por venda
- Ajuste positivo
- Ajuste negativo

### Regras

- Toda alteração de estoque deve gerar uma movimentação.
- O estoque não deve ser alterado diretamente.
- O campo `estoque_atual` do Produto é atualizado automaticamente após cada movimentação.

---

## Venda

### Objetivo

Representar uma venda realizada pela Campo Forte.

Uma venda pode conter um ou mais produtos e possuir uma ou mais formas de pagamento.

### Campos

| Campo       | Obrigatório |
| ----------- | ----------- |
| id          | Sim         |
| cliente     | Não         |
| valor_total | Sim         |
| observacoes | Não         |
| created_at  | Sim         |
| updated_at  | Sim         |

### Regras

- O cliente é opcional para vendas à vista.
- O cliente é obrigatório quando existir valor em fiado.
- A venda não poderá ser excluída após finalizada.
- A venda não poderá ser editada após finalizada.
- A finalização da venda gera a baixa do estoque.
- Não é permitido vender quantidade superior ao estoque disponível.
- O sistema deverá exibir o estoque disponível durante a venda.

---

## ItemVenda

### Objetivo

Representar cada produto vendido em uma venda.

### Campos

| Campo          | Obrigatório |
| -------------- | ----------- |
| id             | Sim         |
| venda          | Sim         |
| produto        | Sim         |
| quantidade     | Sim         |
| valor_unitario | Sim         |
| desconto       | Sim         |
| subtotal       | Sim         |
| created_at     | Sim         |

### Regras

- O mesmo produto não poderá ser lançado duas vezes na mesma venda.
- Caso seja selecionado novamente, o sistema deverá somar as quantidades.
- O desconto será informado separadamente do preço do produto.
- O subtotal representa o valor final do item após o desconto.

---

## PagamentoVenda

### Objetivo

Registrar todas as formas de pagamento utilizadas em uma venda.

### Campos

| Campo           | Obrigatório |
| --------------- | ----------- |
| id              | Sim         |
| venda           | Sim         |
| forma_pagamento | Sim         |
| valor           | Sim         |
| created_at      | Sim         |

### Regras

- Uma venda pode possuir várias formas de pagamento.
- O somatório dos pagamentos deve ser igual ao valor total da venda.
- Caso exista valor em fiado, esse valor deverá gerar uma movimentação na ContaReceber.

---

## ContaReceber

### Objetivo

Representar o saldo devedor de um cliente.

Cada cliente possuirá apenas uma ContaReceber.

### Campos

| Campo       | Obrigatório |
| ----------- | ----------- |
| id          | Sim         |
| cliente     | Sim         |
| saldo_atual | Sim         |
| created_at  | Sim         |
| updated_at  | Sim         |

### Regras

- Cada cliente possui apenas uma ContaReceber.
- O saldo é atualizado automaticamente através das movimentações.
- O saldo nunca deverá ser alterado manualmente.

---

## MovimentoContaReceber

### Objetivo

Registrar todo o histórico financeiro da ContaReceber.

### Campos

| Campo          | Obrigatório |
| -------------- | ----------- |
| id             | Sim         |
| conta_receber  | Sim         |
| tipo           | Sim         |
| valor          | Sim         |
| saldo_anterior | Sim         |
| saldo_atual    | Sim         |
| observacao     | Não         |
| created_at     | Sim         |

### Tipos de Movimentação

- Venda Fiado
- Pagamento
- Ajuste Positivo
- Ajuste Negativo

### Regras

- Toda alteração da ContaReceber deve gerar uma movimentação.
- O saldo da ContaReceber é atualizado automaticamente.
- O histórico financeiro nunca poderá ser excluído.

## Caixa

### Objetivo

Controlar a abertura, movimentação e fechamento diário do caixa da empresa.

### Campos

| Campo            | Obrigatório |
| ---------------- | ----------- |
| id               | Sim         |
| data             | Sim         |
| usuario          | Sim         |
| valor_abertura   | Sim         |
| valor_fechamento | Não         |
| status           | Sim         |
| observacoes      | Não         |
| created_at       | Sim         |
| updated_at       | Sim         |

### Regras

- Será aberto um caixa por dia.
- O caixa deve informar o valor inicial.
- O fechamento calcula automaticamente:
  - Total vendido.
  - Total recebido em dinheiro.
  - Total recebido em PIX.
  - Total recebido em cartão.
  - Diferença entre o valor esperado e o valor contado.
- Não poderá existir mais de um caixa aberto simultaneamente.

## Usuario

### Objetivo

Representar os usuários autorizados a utilizar o ERP.

### Campos

| Campo      | Obrigatório |
| ---------- | ----------- |
| id         | Sim         |
| nome       | Sim         |
| telefone   | Não         |
| cargo      | Sim         |
| ativo      | Sim         |
| created_at | Sim         |
| updated_at | Sim         |

### Regras

- Apenas usuários ativos poderão acessar o sistema.
- As permissões serão definidas de acordo com o cargo.
- Senhas serão armazenadas utilizando o sistema de autenticação do Django.

## LogAuditoria

### Objetivo

Registrar as ações realizadas pelos usuários dentro do sistema.

### Campos

| Campo       | Obrigatório |
| ----------- | ----------- |
| id          | Sim         |
| usuario     | Sim         |
| acao        | Sim         |
| entidade    | Sim         |
| entidade_id | Sim         |
| observacoes | Não         |
| created_at  | Sim         |

### Regras

- Toda ação importante deverá gerar um registro.
- Os registros não poderão ser alterados ou excluídos.
- O histórico servirá para auditoria e rastreabilidade.

# Relacionamentos

- Usuario → Caixa (1:N)
- Usuario → LogAuditoria (1:N)
- Compra → ItemCompra (1:N)
- Produto → ItemCompra (1:N)
- Produto → ItemVenda (1:N)
- Venda → ItemVenda (1:N)
- Venda → PagamentoVenda (1:N)
- Cliente → ContaReceber (1:1)
- ContaReceber → MovimentoContaReceber (1:N)

---

# Pendências

- Criar o DER.
- Definir restrições (constraints).
- Definir índices.

## Decisões Técnicas

- O estoque disponível será exibido durante a realização da venda.
- O desconto será armazenado separadamente do preço do produto.
- Uma venda poderá possuir múltiplas formas de pagamento.
- Cada cliente possuirá uma única ContaReceber.
- O histórico financeiro será armazenado em MovimentoContaReceber.

# Diagrama Entidade-Relacionamento (DER)

Será elaborado após a conclusão da modelagem de todas as entidades.

---

# Próximos Passos

Após a modelagem de todas as entidades serão documentados:

## Restrições

Será preenchido durante a modelagem das entidades.

---

## Índices

Será preenchido durante a modelagem das entidades.

---

## DER Completo

Será criado após a conclusão da modelagem de todas as entidades.
