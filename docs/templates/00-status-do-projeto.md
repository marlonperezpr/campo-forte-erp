# Status do Projeto

## Projeto

**Nome:** ERP Campo Forte

**Status:** 🟡 Em Desenvolvimento

**Fase Atual:** Projeto (Arquitetura)

---

# SDLC

- [x] Planejamento
- [x] Análise
- [x] Projeto (Modelagem de Dados)
- [ ] Projeto (Arquitetura)
- [ ] Testes
- [ ] Entrega

---

# Documentação

- [x] 01-visao-geral.md
- [x] 02-especificacao-funcional.md
- [x] 03-regras-de-negocio.md
- [x] 04-modelagem-do-dominio.md
- [x] 05-banco.md
- [x] 06-arquitetura.md
- [x] AI_CONTEXT.md

---

# Funcionalidades do MVP

- [ ] Usuários
- [ ] Produtos
- [ ] Clientes
- [ ] Fornecedores
- [ ] Compras
- [ ] Estoque
- [ ] Vendas
- [ ] Caixa
- [ ] Contas a Receber
- [ ] Contas a Pagar
- [ ] Relatórios

---

# Próximo Passo

Modelar a Arquitetura do Sistema.

---

# Pendências

- Definir a arquitetura do projeto Django.
- Organizar os módulos da aplicação.
- Definir a comunicação entre os módulos.
- Iniciar a implementação do projeto.

---

# Decisões Importantes

- Produtos por peso serão cadastrados separadamente.
- Produtos não serão excluídos, apenas desativados.
- Fiado gera uma Conta a Receber.
- Pagamento do fiado gera movimentações na Conta a Receber.
- Caixa e Financeiro são módulos separados.
- Produtos podem ser fornecidos por múltiplos fornecedores.
- O custo do produto será calculado por custo médio.
- O DER foi concluído e aprovado.

---

# Observações

- A Modelagem de Dados foi concluída.
- O DER será utilizado como base para implementação no Django ORM.
