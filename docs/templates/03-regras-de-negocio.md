# Regras de Negócio

**Projeto:** ERP Campo Forte  
**Versão:** 1.0  
**Status:** Em desenvolvimento  
**Última atualização:** 02/07/2026

---

# Objetivo

Este documento descreve as regras de negócio do ERP Campo Forte.

Seu objetivo é definir como cada processo da empresa deve funcionar, servindo como referência para a modelagem do domínio, banco de dados e implementação do sistema.

---

# 1. Produtos

## Cadastro

- Todo produto deverá ser cadastrado antes de participar de qualquer operação.
- Compras sempre referenciam um produto previamente cadastrado.
- Produtos poderão ser cadastrados por usuários com permissão para essa operação.

## Exclusão

- Produtos não deverão ser excluídos após participarem de qualquer operação do sistema.
- Caso um produto tenha participado de compras, vendas ou movimentações de estoque, ele poderá apenas ser desativado.
- Produtos criados incorretamente e que nunca tenham sido utilizados poderão ser excluídos.

## Alteração

- Alterações realizadas em produtos deverão ser registradas na auditoria.
- O histórico do produto deverá ser preservado.

## Permissões

As permissões serão configuráveis por usuário.

Exemplos:

- Cadastrar produtos
- Editar produtos
- Alterar preços
- Desativar produtos
- Excluir produtos

---

# 2. Estoque

## Controle

O estoque nunca será alterado diretamente.

Toda alteração deverá ocorrer através de uma movimentação.

Tipos de movimentação:

- Compra
- Venda
- Ajuste
- Inventário
- Perda

## Ajustes

Todo ajuste deverá registrar:

- Produto
- Quantidade
- Motivo
- Usuário responsável
- Data e hora

## Estoque Negativo

Não será permitido estoque negativo.

Caso o produto não possua quantidade suficiente para a venda, a operação deverá ser bloqueada.

---

# 3. Compras

## Cadastro

Toda compra deverá possuir:

- Fornecedor
- Produtos
- Quantidades
- Valor de custo
- Usuário responsável

## Atualização de Estoque

Ao finalizar uma compra:

- O estoque será atualizado automaticamente.
- Será registrada uma movimentação de estoque.
- Será registrada uma auditoria.

## Preço de Custo

Durante o registro da compra, o sistema poderá sugerir a atualização do preço de custo do produto.

A confirmação da atualização dependerá da permissão do usuário.

O preço de venda nunca será alterado automaticamente.

---

# 4. Vendas

## Cadastro

Toda venda deverá possuir pelo menos um produto.

## Finalização

Somente após a confirmação da venda o sistema deverá:

- Atualizar o estoque.
- Atualizar o caixa.
- Registrar auditoria.
- Gerar contas a receber quando houver fiado.

Enquanto a venda não for finalizada, nenhuma informação deverá alterar o estoque ou o caixa.

## Descontos

O preço poderá ser alterado durante a venda.

O sistema deverá respeitar:

- Preço padrão.
- Preço mínimo permitido.
- Permissões do usuário.

## Cancelamento

Somente administradores poderão cancelar vendas.

Vendas canceladas permanecerão registradas para fins de auditoria.

Nunca deverão ser excluídas.

## Formas de Pagamento

Uma mesma venda poderá possuir múltiplas formas de pagamento.

Exemplos:

- Dinheiro
- PIX
- Cartão
- Fiado

Será permitido combinar diferentes formas de pagamento na mesma venda.

---

# 5. Contas a Receber (Fiado)

## Funcionamento

O fiado funcionará como uma conta corrente do cliente.

O cliente poderá:

- Realizar novas compras fiadas.
- Efetuar pagamentos parciais.
- Possuir múltiplas compras em aberto.

## Recebimentos

Todo pagamento recebido deverá:

- Atualizar o saldo devedor.
- Registrar entrada no caixa.
- Registrar auditoria.

---

# 6. Caixa

## Operações

Usuários autorizados poderão:

- Abrir caixa.
- Fechar caixa.
- Registrar sangrias.
- Registrar entradas.
- Registrar saídas.

## Auditoria

Toda operação realizada no caixa deverá registrar:

- Usuário
- Data
- Hora
- Operação realizada

---

# 7. Auditoria

O sistema deverá registrar todas as operações relevantes.

Exemplos:

- Cadastro de produtos.
- Alteração de preços.
- Compras.
- Vendas.
- Cancelamentos.
- Ajustes de estoque.
- Abertura e fechamento de caixa.
- Recebimento de fiados.

Cada registro deverá conter:

- Usuário responsável.
- Data.
- Hora.
- Operação realizada.

---

# 8. Regras Gerais

- Produtos não poderão ser excluídos após participarem de operações.
- O estoque será sempre calculado a partir das movimentações.
- Não será permitido estoque negativo.
- Toda movimentação deverá registrar o usuário responsável.
- Compras atualizarão automaticamente o estoque.
- Vendas atualizarão automaticamente o estoque e o caixa.
- Vendas fiadas gerarão contas a receber.
- Pagamentos de fiados atualizarão automaticamente o saldo devedor e o caixa.
- O sistema deverá preservar o histórico de todas as operações.
- Toda operação relevante deverá ser registrada na auditoria.

---

# Observações

Este documento poderá ser atualizado conforme novas regras de negócio forem identificadas durante o desenvolvimento do ERP.
