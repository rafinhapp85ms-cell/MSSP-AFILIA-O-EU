ATENÇÃO: responda APENAS com código funcional.
NÃO explique nada fora do código.
NÃO use comentários longos.
NÃO escreva texto antes ou depois do código.
Somente código Python completo.

CONTEXTO:
Tenho um app em Streamlit chamado "MSSP Afiliado".
Ele já possui:
- Menu lateral com: Início, Pesquisa de Produtos, Ideias de Anúncio, Histórico, Configurações
- Um único arquivo app.py
- Uso de st.session_state
- Salvamento local em JSON
- Tudo em português europeu
- Sem APIs externas
- Sem internet
- Código simples e limpo

OBJETIVO DESTA ETAPA (FASE 2A):
EVOLUIR a opção "Pesquisa de Produtos" sem quebrar nada existente.

O QUE DEVE SER IMPLEMENTADO:

1) Na página "Pesquisa de Produtos", adicionar novos campos:
- Plataforma (texto livre)
- Tipo de produto (Digital ou Físico)
- Comissão (valor numérico)
- País alvo (texto)
- Tipo de pagamento:
  - Normal
  - Pagamento na entrega (explicar no texto como "pagamento no ato da entrega")

2) Criar uma análise automática local do produto:
- Gerar um SCORE de 0 a 100
- Classificar como:
  - Fraco
  - Médio
  - Forte
- A análise deve considerar:
  - Comissão
  - Tipo de produto
  - Tipo de pagamento
  - País informado

3) Mostrar ao utilizador:
- O score
- A classificação
- Um texto explicativo simples dizendo POR QUE recebeu essa classificação

4) Salvar tudo no histórico (JSON), incluindo:
- Data e hora
- Todos os campos preenchidos
- Score
- Classificação
- Texto explicativo

5) NÃO aprovar nada automaticamente.
O app apenas analisa e sugere.

REGRAS OBRIGATÓRIAS:
- NÃO criar novos menus
- NÃO remover funcionalidades existentes
- NÃO usar inglês na interface
- NÃO usar APIs, requests, scraping ou internet
- Código deve rodar no Streamlit Cloud gratuito
- Tudo deve continuar em um único app.py

FINAL OBRIGATÓRIO:
No FINAL do código, incluir uma função ou texto visível no app que explique, em português, o PASSO A PASSO de:
- Onde colar o código
- Como executar o app
- O que o utilizador deve fazer após a análise do produto
