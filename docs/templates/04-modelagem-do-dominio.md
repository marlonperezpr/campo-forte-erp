# 02 - Especificação Funcional

## 1. Introdução

Este documento descreve o comportamento funcional do ERP Campo Forte, detalhando como os usuários interagem com o sistema, quais fluxos existem e como as regras de negócio são aplicadas na prática.

Ele transforma a modelagem de domínio em ações concretas dentro do sistema.

---

## 2. Visão Geral do Sistema

O ERP Campo Forte é um sistema de gestão para controle de vendas, estoque, compras e financeiro.

O sistema é dividido nos seguintes módulos principais:

- Vendas
- Caixa
- Produtos
- Clientes
- Fornecedores
- Compras
- Estoque
- Usuários e Permissões
- Contas a Receber
- Contas a Pagar
- Relatórios

## 3. Módulo de Vendas

### 3.1 Objetivo

Permitir a realização de vendas de forma rápida (PDV), com suporte a vendas à vista e a prazo (fiado), garantindo integração com caixa e controle financeiro.

---

### 3.2 Abertura da Venda

O sistema inicia uma venda sempre em uma tela de PDV (ponto de venda) em branco.

#### Características da tela inicial:

- Venda inicia sem cliente obrigatório
- Venda inicia sem forma de pagamento definida
- Usuário pode adicionar produtos imediatamente
- Venda é considerada "em andamento" até sua finalização

---

### 3.3 Adição de Produtos

O usuário pode adicionar produtos à venda através de:

- Busca por nome
- Código de barras

Cada item é adicionado à lista da venda em tempo real.

O sistema recalcula automaticamente:

- Subtotal
- Total
- Descontos (quando aplicável)

---

### 3.4 Vinculação de Cliente

A vinculação de cliente é opcional durante o processo de venda.

O cliente pode ser associado em dois momentos:

- Durante a venda (antes da finalização)
- No momento da finalização (obrigatório apenas para fiado)

#### Regra importante:

- Venda à vista não exige cliente
- Venda a prazo (fiado) exige cliente obrigatório

---

### 3.5 Edição da Venda

A venda pode ser editada enquanto estiver em andamento:

- Adicionar produtos
- Remover produtos
- Alterar quantidades
- Vincular cliente

Após finalização, a venda não pode ser editada, apenas cancelada.

---

### 3.6 Finalização da Venda

A finalização depende diretamente da forma de pagamento escolhida.

O usuário pode selecionar:

- Dinheiro
- Pix
- Cartão
- Boleto
- Fiado

#### Fluxo de finalização:

1. Usuário clica em "Finalizar Venda"
2. Sistema solicita forma de pagamento
3. Se for fiado:
   - Cliente torna-se obrigatório
   - Sistema gera Conta a Receber
4. Sistema registra a venda como concluída
5. Sistema envia a movimentação para o Caixa

---

### 3.7 Integração com Caixa

Toda venda finalizada deve ser registrada no Caixa aberto.

#### Regras:

- Venda só pode ser finalizada com caixa aberto
- Cada forma de pagamento é registrada separadamente no caixa
- Fiado não gera entrada imediata de dinheiro no caixa
- Venda impacta o caixa conforme sua forma de pagamento

---

### 3.8 Estados da Venda

- Em andamento
- Finalizada
- Cancelada

---

### 3.9 Regras de Negócio do Módulo

- Venda inicia sempre sem cliente obrigatório
- Cliente só é obrigatório para vendas a prazo (fiado)
- Venda não pode ser excluída, apenas cancelada
- Produtos podem ser adicionados livremente durante edição
- Venda só pode ser finalizada com caixa aberto
- Venda pode ter múltiplas formas de pagamento (futuro aprimoramento)
