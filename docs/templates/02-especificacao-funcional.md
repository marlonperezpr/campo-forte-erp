# 02 - Especificação Funcional

## 1. Introdução

Este documento descreve o comportamento funcional do ERP Campo Forte, detalhando como os usuários interagem com o sistema, quais fluxos existem e como as regras de negócio são aplicadas na prática.

O objetivo é servir como referência para o desenvolvimento do backend, frontend, testes e futuras evoluções do sistema.

---

# 2. Visão Geral do Sistema

O ERP Campo Forte é um sistema de gestão para controle de:

- Vendas
- Compras
- Estoque
- Financeiro
- Clientes
- Fornecedores
- Usuários
- Relatórios

---

# 3. Módulo de Vendas

## Objetivo

Permitir a realização de vendas de forma rápida (PDV), integrando estoque, caixa e financeiro.

## Objetivos do Negócio

- Agilizar o atendimento.
- Registrar todas as vendas.
- Controlar pagamentos.
- Atualizar estoque.
- Integrar automaticamente com o Caixa.

## Funcionalidades

- Abrir venda
- Adicionar produtos
- Buscar produto por nome
- Buscar produto por código de barras (evolução)
- Vincular cliente (opcional)
- Aplicar desconto
- Selecionar forma de pagamento
- Finalizar venda
- Cancelar venda

## Fluxo Funcional

Abrir venda

↓

Adicionar produtos

↓

(Opcional) Vincular cliente

↓

Selecionar forma de pagamento

↓

Caso seja Fiado:

→ Cliente obrigatório

↓

Finalizar

↓

Atualizar estoque

↓

Registrar movimentação no Caixa

↓

Encerrar venda

## Experiência da Tela (UX)

- A tela inicia vazia (modelo PDV).
- O operador pode adicionar produtos imediatamente.
- Cliente não é obrigatório no início.
- O foco é minimizar a quantidade de cliques.
- Totais são atualizados em tempo real.

## Regras Funcionais

- Venda inicia sem cliente.
- Cliente torna-se obrigatório apenas para fiado.
- Venda exige Caixa aberto.
- Venda não pode ser editada após finalização.
- Venda pode ser cancelada, mas nunca excluída.

## Validações

- Não permitir finalizar sem itens.
- Não permitir venda sem Caixa aberto.
- Não permitir venda fiada sem cliente.

## Casos de Erro

- Caixa fechado.
- Produto inexistente.
- Produto sem estoque (exceto encomenda).

## Informações Gerenciais

- Total vendido por período.
- Vendas por funcionário.
- Vendas por forma de pagamento.
- Produtos mais vendidos.
- Ticket médio.

## Justificativas das Decisões

A venda foi modelada como um PDV porque a maior parte das operações ocorre no balcão.

Cliente é opcional para reduzir o tempo de atendimento.

## Possíveis Evoluções

- Leitor de código de barras.
- Comissão de vendedores.
- Promoções automáticas.
- Programa de fidelidade.

## Dependências

Depende de:

- Produtos
- Caixa
- Usuários

Utilizado por:

- Estoque
- Contas a Receber
- Relatórios

---

# 4. Módulo de Caixa

## Objetivo

Controlar todas as movimentações financeiras do dia.

## Objetivos do Negócio

- Registrar entradas financeiras.
- Garantir conferência diária.
- Organizar fechamento de caixa.

## Funcionalidades

- Abrir Caixa
- Fechar Caixa
- Registrar entradas
- Registrar recebimentos
- Consultar movimentações

## Fluxo Funcional

Abrir Caixa

↓

Realizar vendas

↓

Receber pagamentos

↓

Registrar movimentações

↓

Fechar Caixa

## Experiência da Tela

- Apenas um Caixa pode permanecer aberto.
- O sistema exibe totais por modalidade de pagamento.

## Regras Funcionais

- Apenas um Caixa aberto.
- Venda exige Caixa aberto.
- Caixa fechado não recebe movimentações.

## Validações

- Não permitir abrir dois Caixas.
- Não permitir movimentações após fechamento.

## Casos de Erro

- Tentativa de venda sem Caixa aberto.
- Tentativa de fechar Caixa inexistente.

## Informações Gerenciais

- Total diário.
- Valores por modalidade.
- Histórico de abertura e fechamento.

## Justificativas das Decisões

Foi adotado Caixa diário para facilitar auditoria e conferência.

## Possíveis Evoluções

- Múltiplos Caixas.
- Sangrias.
- Suprimentos.
- Diferença automática de Caixa.

## Dependências

Depende de:

- Usuários

Utilizado por:

- Vendas
- Financeiro
- Relatórios

---

# 5. Módulo de Contas a Receber

## Objetivo

Controlar vendas realizadas no fiado.

## Objetivos do Negócio

- Substituir o controle manual em papel.
- Manter histórico das vendas.
- Facilitar cobrança.

## Funcionalidades

- Visualizar clientes devedores.
- Consultar histórico.
- Registrar pagamentos.
- Registrar pagamento parcial.
- Consultar saldo.

## Fluxo Funcional

Venda Fiado

↓

Gera Conta a Receber

↓

Cliente realiza pagamento

↓

Registrar pagamento

↓

Atualizar saldo

↓

Registrar entrada no Caixa

## Experiência da Tela

Tela inicial:

Lista de clientes devedores.

Ao selecionar um cliente:

Exibir todas as vendas fiadas contendo:

- Data
- Hora
- Número da Nota Manual
- Valor
- Valor Pago
- Saldo
- Vencimento

O operador informa apenas o valor recebido.

O sistema realiza a baixa conforme a regra definida.

## Regras Funcionais

- Fiado gera Conta a Receber.
- Cliente obrigatório.
- Pagamento parcial permitido.
- Cada venda gera uma Conta a Receber independente.
- O cliente visualiza todas as pendências agrupadas.

## Validações

- Não permitir valor negativo.
- Não permitir pagamento acima do saldo.

## Casos de Erro

- Cliente inexistente.
- Conta quitada.

## Informações Gerenciais

- Clientes inadimplentes.
- Total em aberto.
- Contas vencidas.
- Histórico de pagamentos.

## Justificativas das Decisões

Foi mantida a utilização da nota manual para preservar o processo atual da empresa, utilizando o ERP como apoio e não como substituição imediata.

## Possíveis Evoluções

- Juros automáticos.
- Cobrança por WhatsApp.
- Emissão de boletos.
- PIX Copia e Cola.

## Dependências

Depende de:

- Clientes
- Vendas
- Caixa

Utilizado por:

- Financeiro
- Relatórios

---

# 6. Módulo de Produtos

## Objetivo

Permitir o cadastro e gerenciamento dos produtos comercializados pela Campo Forte, servindo como base para os módulos de Compras, Estoque e Vendas.

## Objetivos do Negócio

- Centralizar o cadastro de produtos.
- Definir preços de venda.
- Facilitar consultas rápidas.
- Disponibilizar produtos para compra e venda.

## Funcionalidades

- Cadastrar produto.
- Editar produto.
- Desativar produto.
- Consultar produto por nome.
- Definir preço de venda.
- Definir unidade de medida.
- Consultar informações do produto.

## Fluxo Funcional

Cadastrar produto

↓

Informar dados básicos

↓

Definir preço de venda

↓

Produto disponível para compras

↓

Entrada em estoque

↓

Produto disponível para venda

## Experiência da Tela (UX)

- Pesquisa rápida por nome.
- Cadastro simples e objetivo.
- Produtos ativos destacados.
- Interface otimizada para uso diário.

## Regras Funcionais

- Produtos não podem ser excluídos, apenas desativados.
- O preço de venda é definido manualmente pelo administrador.
- Produtos vendidos por peso serão cadastrados separadamente.
- Um produto pode possuir múltiplos fornecedores.

## Validações

- Nome obrigatório.
- Preço de venda obrigatório.
- Unidade de medida obrigatória.

## Casos de Erro

- Produto inexistente.
- Produto inativo.
- Tentativa de venda de produto desativado.

## Informações Gerenciais

- Produtos mais vendidos.
- Produtos menos vendidos.
- Histórico de preços.
- Quantidade em estoque.

## Justificativas das Decisões

Optou-se por um cadastro simples para refletir a realidade operacional da Campo Forte, reduzindo o tempo de cadastro e facilitando a utilização pelos funcionários.

## Possíveis Evoluções

- Código de barras.
- QR Code.
- Categorias.
- Marcas.
- Imagens dos produtos.

## Dependências

**Depende de:**

- Usuários e Permissões.

**Utilizado por:**

- Compras.
- Estoque.
- Vendas.
- Relatórios.

---

# 7. Módulo de Estoque

## Objetivo

Controlar a quantidade disponível de cada produto e garantir que as movimentações de entrada e saída sejam registradas corretamente.

## Objetivos do Negócio

- Manter o estoque atualizado.
- Evitar vendas de produtos indisponíveis.
- Controlar entradas e saídas de mercadorias.

## Funcionalidades

- Consultar estoque.
- Registrar entrada de produtos.
- Registrar saída automática pelas vendas.
- Ajustar estoque manualmente (Administrador).

## Fluxo Funcional

Compra

↓

Recebimento

↓

Entrada no estoque

↓

Venda

↓

Baixa automática

## Experiência da Tela (UX)

- Consulta rápida por nome do produto.
- Quantidade disponível destacada.
- Interface limpa e objetiva.

## Regras Funcionais

- Controle apenas por quantidade.
- Não haverá controle por lote no MVP.
- Não haverá controle de validade no MVP.
- Não permitir venda sem estoque, exceto vendas do tipo Encomenda.

## Validações

- Estoque não pode ficar negativo.
- Ajustes de estoque exigem permissão.

## Casos de Erro

- Estoque insuficiente.
- Produto inexistente.

## Informações Gerenciais

- Estoque atual.
- Produtos sem estoque.
- Histórico de movimentações.

## Justificativas das Decisões

Foi priorizada uma operação simples e compatível com a realidade atual da empresa, evitando funcionalidades que aumentariam a complexidade sem agregar valor ao MVP.

## Possíveis Evoluções

- Controle por lote.
- Controle de validade.
- Múltiplos depósitos.
- Transferência entre depósitos.

## Dependências

**Depende de:**

- Produtos.
- Compras.

**Utilizado por:**

- Vendas.
- Relatórios.

---

# 8. Módulo de Compras

## Objetivo

Registrar as compras realizadas pela empresa e atualizar automaticamente o estoque.

## Objetivos do Negócio

- Registrar aquisições de mercadorias.
- Atualizar o estoque.
- Manter histórico de custos.
- Gerar Contas a Pagar quando aplicável.

## Funcionalidades

- Registrar compra.
- Informar fornecedor (opcional).
- Definir origem da compra.
- Registrar frete.
- Registrar parcelas.
- Registrar recebimento parcial.

## Fluxo Funcional

Nova compra

↓

Informar produtos

↓

Informar fornecedor (quando houver)

↓

Registrar origem da compra

↓

Recebimento

↓

Atualizar estoque

↓

Gerar Contas a Pagar

## Experiência da Tela (UX)

- Processo semelhante ao cadastro de vendas.
- Inclusão rápida de produtos.
- Visualização clara do status da compra.

## Regras Funcionais

- Compras podem possuir recebimento parcial.
- Frete é opcional.
- Fornecedor pode ser omitido em compras avulsas.
- A origem da compra poderá ser Distribuidor, Atacado, Marketplace, Loja Física ou outra definida pelo administrador.

## Validações

- Compra deve possuir pelo menos um item.
- Quantidade deve ser maior que zero.

## Casos de Erro

- Produto inexistente.
- Recebimento superior ao solicitado.

## Informações Gerenciais

- Compras por período.
- Compras por fornecedor.
- Histórico de preços.
- Última compra de cada produto.

## Justificativas das Decisões

O fluxo foi mantido semelhante ao processo atual da Campo Forte para facilitar a adoção do sistema pelos usuários.

## Possíveis Evoluções

- Pedido de compra.
- Aprovação de compras.
- Integração com fornecedores.

## Dependências

**Depende de:**

- Produtos.
- Fornecedores.

**Utilizado por:**

- Estoque.
- Contas a Pagar.
- Relatórios.

---

# 9. Módulo de Clientes

## Objetivo

Gerenciar o cadastro de clientes e controlar seu relacionamento comercial com a empresa.

## Objetivos do Negócio

- Identificar clientes.
- Controlar vendas fiadas.
- Manter histórico de compras.
- Facilitar cobranças.

## Funcionalidades

- Cadastrar cliente.
- Editar cadastro.
- Consultar cliente.
- Visualizar histórico de compras.
- Visualizar histórico de fiados.
- Consultar saldo devedor.

## Fluxo Funcional

Cadastrar cliente

↓

Realizar compras

↓

Caso venda fiada

↓

Gerar Conta a Receber

↓

Registrar pagamentos

↓

Atualizar saldo devedor

## Experiência da Tela (UX)

Ao pesquisar um cliente, o sistema exibirá:

- Nome.
- Telefone.
- Situação.
- Saldo devedor.

Além disso, haverá a opção **"Ver mais"**, exibindo:

- Histórico completo de compras.
- Histórico de vendas fiadas.
- Pagamentos realizados.
- Endereço.
- Observações.

## Regras Funcionais

- Cliente não pode ser excluído.
- Cliente não pode ser desativado.
- Cliente é obrigatório apenas para vendas fiadas.
- Clientes inadimplentes terão novas vendas fiadas bloqueadas até regularização.

## Validações

- Nome obrigatório.
- Não permitir venda fiada para cliente bloqueado.

## Casos de Erro

- Cliente inexistente.
- Cliente bloqueado para compras fiadas.

## Informações Gerenciais

- Clientes com maior volume de compras.
- Clientes inadimplentes.
- Histórico de compras.
- Histórico de pagamentos.

## Justificativas das Decisões

O sistema manterá o histórico completo do cliente, substituindo gradualmente o controle manual realizado atualmente em papel.

## Possíveis Evoluções

- Programa de fidelidade.
- Cashback.
- Limite de crédito.
- Cadastro de dependentes.

## Dependências

**Depende de:**

- Usuários e Permissões.

**Utilizado por:**

- Vendas.
- Contas a Receber.
- Relatórios.

---

# 10. Módulo de Fornecedores

## Objetivo

Gerenciar o cadastro dos fornecedores da Campo Forte e manter o histórico das compras realizadas.

## Objetivos do Negócio

- Centralizar os fornecedores da empresa.
- Registrar o histórico de compras.
- Facilitar futuras negociações.
- Permitir análise de preços entre fornecedores.

## Funcionalidades

- Cadastrar fornecedor.
- Editar fornecedor.
- Desativar fornecedor.
- Consultar fornecedores.
- Visualizar histórico de compras.
- Visualizar produtos fornecidos.
- Consultar histórico de preços.

## Fluxo Funcional

Cadastrar fornecedor

↓

Realizar compra

↓

Atualizar histórico

↓

Disponibilizar informações para consultas futuras

## Experiência da Tela (UX)

Ao consultar um fornecedor o sistema deverá apresentar:

- Nome.
- Telefone.
- Situação.
- Última compra.

Botão **"Ver mais"** contendo:

- Histórico completo de compras.
- Produtos fornecidos.
- Histórico de preços.
- Observações.

## Regras Funcionais

- Fornecedores não podem ser excluídos.
- Apenas desativados.
- O histórico deve permanecer mesmo após desativação.
- Um fornecedor pode fornecer diversos produtos.
- Um produto pode possuir diversos fornecedores.

## Validações

- Nome obrigatório.
- Não permitir duplicidade de cadastro quando possível.

## Casos de Erro

- Fornecedor inexistente.
- Fornecedor inativo.

## Informações Gerenciais

- Total comprado por fornecedor.
- Histórico de preços.
- Última compra.
- Produtos fornecidos.
- Comparativo de preços entre fornecedores.

## Justificativas das Decisões

Mesmo em compras avulsas, manter o conceito de fornecedor permite consultas futuras e análises de custos, sem alterar o fluxo operacional atual.

## Possíveis Evoluções

- Avaliação de fornecedores.
- Prazo médio de entrega.
- Integração com distribuidores.

## Dependências

**Depende de:**

- Usuários e Permissões.

**Utilizado por:**

- Compras.
- Contas a Pagar.
- Relatórios.

---

# 11. Módulo de Usuários e Permissões

## Objetivo

Controlar o acesso ao sistema e registrar todas as operações realizadas pelos usuários.

## Objetivos do Negócio

- Garantir segurança.
- Controlar permissões.
- Manter rastreabilidade.
- Evitar alterações indevidas.

## Funcionalidades

- Cadastrar usuário.
- Editar usuário.
- Ativar e desativar usuário.
- Definir permissões.
- Alterar senha.
- Trocar operador.
- Consultar histórico de operações.

## Fluxo Funcional

Cadastrar usuário

↓

Definir permissões

↓

Usuário acessa o sistema

↓

Operações registradas automaticamente

## Experiência da Tela (UX)

Tela simples contendo:

- Nome.
- Usuário.
- Situação.
- Lista de permissões.

As permissões serão exibidas através de opções de seleção, facilitando a configuração.

## Regras Funcionais

- Todo usuário possui login individual.
- Todas as operações devem registrar o usuário responsável.
- Apenas administradores podem alterar permissões.
- Usuários podem ser desativados, nunca excluídos.

## Validações

- Usuário único.
- Senha obrigatória.
- Permissões obrigatórias.

## Casos de Erro

- Usuário inativo.
- Senha incorreta.
- Permissão insuficiente.

## Informações Gerenciais

- Último acesso.
- Histórico de operações.
- Usuários ativos.
- Usuários inativos.

## Justificativas das Decisões

Foi adotado um modelo baseado em permissões individuais para oferecer maior flexibilidade e permitir adequar o sistema ao crescimento da empresa.

## Possíveis Evoluções

- Perfis pré-configurados.
- Autenticação em dois fatores.
- Registro de dispositivos.

## Dependências

**Depende de:**

- Nenhum.

**Utilizado por:**

- Todo o sistema.

---

# 12. Módulo de Contas a Pagar

## Objetivo

Controlar todas as obrigações financeiras da empresa.

## Objetivos do Negócio

- Controlar despesas.
- Registrar pagamentos.
- Organizar vencimentos.
- Integrar com o Caixa.

## Funcionalidades

- Registrar conta manualmente.
- Gerar contas através das compras.
- Registrar pagamento parcial.
- Registrar pagamento total.
- Consultar contas em aberto.
- Consultar contas pagas.

## Fluxo Funcional

Criar Conta

↓

Definir vencimento

↓

Registrar pagamento

↓

Atualizar saldo

↓

Registrar saída no Caixa

## Experiência da Tela (UX)

Tela inicial contendo:

- Contas vencidas.
- Contas a vencer.
- Próximos vencimentos.

Ao selecionar uma conta:

- Histórico.
- Pagamentos.
- Juros.
- Multa.
- Desconto.

## Regras Funcionais

- Contas podem ser criadas manualmente.
- Compras podem gerar Contas a Pagar automaticamente.
- Pagamentos parciais são permitidos.
- Juros, multa e desconto serão informados manualmente.
- Todo pagamento gera movimentação no Caixa.

## Validações

- Valor maior que zero.
- Não permitir pagamento superior ao saldo.

## Casos de Erro

- Conta inexistente.
- Conta já quitada.

## Informações Gerenciais

- Total em aberto.
- Total pago.
- Contas vencidas.
- Despesas por período.

## Justificativas das Decisões

Foi mantido um fluxo simples, permitindo controlar tanto compras quanto despesas operacionais da empresa.

## Possíveis Evoluções

- Pagamentos automáticos.
- Integração bancária.
- Boletos.

## Dependências

**Depende de:**

- Compras.
- Caixa.

**Utilizado por:**

- Relatórios.

---

# 13. Módulo de Relatórios

## Objetivo

Disponibilizar informações para auxiliar a tomada de decisão do gestor.

## Objetivos do Negócio

- Facilitar análises.
- Acompanhar resultados.
- Auxiliar decisões.

## Funcionalidades

- Relatórios de vendas.
- Relatórios de compras.
- Relatórios financeiros.
- Relatórios de estoque.
- Relatórios de clientes.
- Relatórios de fornecedores.

## Fluxo Funcional

Selecionar relatório

↓

Definir período

↓

Gerar relatório

↓

Visualizar

↓

Exportar PDF

## Experiência da Tela (UX)

Interface simples contendo:

- Tipo do relatório.
- Período.
- Botão Gerar.
- Botão Exportar PDF.

## Regras Funcionais

- Todos os relatórios podem ser filtrados por período.
- Apenas usuários autorizados poderão acessar relatórios financeiros.
- Os relatórios devem refletir sempre os dados atualizados do sistema.

## Validações

- Período obrigatório.
- Relatório disponível apenas para usuários autorizados.

## Casos de Erro

- Nenhum registro encontrado.
- Período inválido.

## Informações Gerenciais

### Vendas

- Vendas por período.
- Produtos mais vendidos.
- Produtos menos vendidos.
- Ticket médio.
- Formas de pagamento.

### Compras

- Compras por período.
- Compras por fornecedor.
- Histórico de preços.

### Estoque

- Estoque atual.
- Produtos sem estoque.
- Movimentações.

### Financeiro

- Contas a Receber.
- Contas a Pagar.
- Clientes inadimplentes.
- Fluxo financeiro.

### Clientes

- Clientes que mais compram.
- Clientes inadimplentes.

### Fornecedores

- Histórico de compras.
- Comparativo de preços.

## Justificativas das Decisões

Os relatórios foram definidos para fornecer informações objetivas ao gestor, evitando excesso de indicadores e priorizando dados realmente úteis para a operação diária.

## Possíveis Evoluções

- Dashboard com gráficos.
- Indicadores (KPIs).
- Exportação para Excel.
- Agendamento automático de relatórios.

## Dependências

**Depende de:**

- Todos os módulos operacionais.

**Utilizado por:**

- Gestão da empresa.

---

# Considerações Finais

O ERP Campo Forte foi especificado priorizando simplicidade, rapidez de operação e aderência ao processo atual da empresa.

Sempre que possível, o sistema deverá adaptar-se ao modo de trabalho da Campo Forte, reduzindo a necessidade de mudanças na rotina dos usuários.

A filosofia do projeto é:

> **Substituir o papel sem alterar a forma de trabalhar da empresa.**

Todas as futuras implementações deverão respeitar este princípio, evitando complexidade desnecessária e priorizando uma experiência intuitiva para operadores e gestores.
