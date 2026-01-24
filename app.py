import streamlit as st
import json
import os
from datetime import datetime

# ==============================
# Configuração inicial da página
# ==============================
st.set_page_config(
    page_title="MSSP Afiliado",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================
# Arquivos de dados
# ==============================
HISTORICO_ARQUIVO = "historico_afiliacao.json"

# ==============================
# Funções de persistência
# ==============================
def carregar_historico():
    if os.path.exists(HISTORICO_ARQUIVO):
        try:
            with open(HISTORICO_ARQUIVO, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def salvar_historico(historico):
    with open(HISTORICO_ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(historico, f, ensure_ascii=False, indent=2)

def calcular_score(comissao, tipo_produto, tipo_pagamento, pais):
    score = 50
    if comissao >= 10:
        score += 20
    elif comissao >= 5:
        score += 10
    if tipo_produto == "Digital":
        score += 15
    if tipo_pagamento == "Normal":
        score += 10
    if pais in ["Portugal", "Espanha", "França", "Alemanha", "Itália"] or "Europa" in pais:
        score += 5
    return min(score, 100)

def classificar_score(score):
    if score >= 70:
        return "Forte"
    elif score >= 40:
        return "Médio"
    else:
        return "Fraco"

def gerar_explicacao(comissao, tipo_produto, tipo_pagamento, pais, score):
    motivos = []
    if comissao >= 10:
        motivos.append("comissão alta")
    elif comissao < 5:
        motivos.append("comissão baixa")
    if tipo_produto == "Digital":
        motivos.append("produto digital (maior margem)")
    if tipo_pagamento == "Normal":
        motivos.append("pagamento antecipado")
    if pais in ["Portugal", "Espanha", "França", "Alemanha", "Itália"] or "Europa" in pais:
        motivos.append("país com bom desempenho")
    if not motivos:
        motivos = ["nenhum fator favorável identificado"]
    return f"Score baseado em: {', '.join(motivos)}."

# ==============================
# Inicializar estado da sessão
# ==============================
if "historico" not in st.session_state:
    st.session_state.historico = carregar_historico()

# ==============================
# Menu lateral
# ==============================
st.sidebar.title("MSSP Afiliado")
pagina = st.sidebar.radio(
    "Navegue pelas seções:",
    ("Início", "Pesquisa de Produtos", "Ideias de Anúncio", "Histórico", "Configurações"),
    index=0
)

# ==============================
# Página: Início
# ==============================
if pagina == "Início":
    st.title("🎯 MSSP Afiliado")
    st.subheader("Fase 2A — Análise Avançada de Produtos para Afiliados")
    st.write("""
    Este app ajuda afiliados a:
    - Analisar produtos com base em critérios-chave
    - Receber um score de viabilidade (0–100)
    - Gerar ideias de anúncios em português europeu
    - Manter histórico organizado
    
    Tudo é feito localmente, sem internet.
    """)
    st.info("💡 Dica: Comece pela página **'Pesquisa de Produtos'** para analisar sua primeira oferta.")

# ==============================
# Página: Pesquisa de Produtos (ATUALIZADA)
# ==============================
elif pagina == "Pesquisa de Produtos":
    st.title("🔍 Pesquisa de Produtos")
    
    st.subheader("Analise uma nova oferta")
    
    palavras_chave_input = st.text_input(
        "Palavras-chave (separadas por vírgula, máximo 7):",
        placeholder="Ex: fone, bluetooth, sem fios, wireless"
    )
    
    plataformas_predefinidas = ["Amazon", "ClickBank", "Awin", "CJ Affiliate", "Hotmart", "Outra"]
    plataforma = st.selectbox(
        "Plataforma:",
        options=plataformas_predefinidas,
        index=0
    )
    # Permitir digitação manual mesmo com selectbox
    if plataforma == "Outra":
        plataforma_manual = st.text_input("Digite a plataforma:", key="plataforma_manual")
        if plataforma_manual.strip():
            plataforma = plataforma_manual.strip()
    
    tipo_produto = st.selectbox(
        "Tipo de produto:",
        ["Digital", "Físico"]
    )
    
    comissao_input = st.number_input(
        "Comissão (%):",
        min_value=0.0,
        value=1.0,
        step=0.5,
        help="Valor mínimo automático: 1%"
    )
    comissao = comissao_input if comissao_input > 0 else 1.0
    
    pais = st.text_input(
        "País alvo:",
        placeholder="Ex: Portugal, Alemanha ou Europa"
    )
    
    tipo_pagamento = st.selectbox(
        "Tipo de pagamento:",
        ["Normal", "Pagamento na entrega"]
    )
    
    if st.button("✅ Analisar Produto"):
        if not palavras_chave_input.strip() or not pais.strip():
            st.warning("⚠️ Por favor, preencha palavras-chave e país.")
        else:
            # Processar palavras-chave
            palavras_lista = [p.strip() for p in palavras_chave_input.split(",") if p.strip()]
            if len(palavras_lista) == 0:
                st.warning("⚠️ Insira pelo menos uma palavra-chave.")
            elif len(palavras_lista) > 7:
                st.warning("⚠️ Limite máximo: 7 palavras-chave. Remova algumas para continuar.")
            else:
                # Processar país
                pais_salvar = "Europa (todos os países)" if pais.strip().lower() == "europa" else pais.strip()
                
                score = calcular_score(comissao, tipo_produto, tipo_pagamento, pais_salvar)
                classificacao = classificar_score(score)
                explicacao = gerar_explicacao(comissao, tipo_produto, tipo_pagamento, pais_salvar, score)
                
                novo_registro = {
                    "tipo": "pesquisa_v2",
                    "palavras_chave": palavras_lista,
                    "plataforma": plataforma,
                    "tipo_produto": tipo_produto,
                    "comissao": comissao,
                    "pais": pais_salvar,
                    "tipo_pagamento": tipo_pagamento,
                    "score": score,
                    "classificacao": classificacao,
                    "explicacao": explicacao,
                    "data_hora": datetime.now().isoformat()
                }
                
                st.session_state.historico.append(novo_registro)
                salvar_historico(st.session_state.historico)
                
                st.success("✅ Análise concluída!")
                st.markdown(f"**Score:** {score}/100")
                st.markdown(f"**Classificação:** {classificacao}")
                st.markdown(f"**Explicação:** {explicacao}")

# ==============================
# Página: Ideias de Anúncio
# ==============================
elif pagina == "Ideias de Anúncio":
    st.title("✍️ Ideias de Anúncio")
    
    nome_produto = st.text_input(
        "Nome do produto:",
        placeholder="Ex: Curso de Dropshipping"
    )
    
    if st.button("✨ Gerar anúncio"):
        if not nome_produto.strip():
            st.warning("⚠️ Por favor, digite o nome do produto.")
        else:
            anuncio = (
                f"🔥 **Descubra o {nome_produto}!**\n\n"
                f"✅ Qualidade premium garantida\n"
                f"✅ Entrega rápida em todo o país\n"
                f"✅ Preço especial por tempo limitado\n\n"
                f"👉 **Não perca esta oportunidade! Clique no link abaixo para saber mais.**\n"
                f"[LINK DE AFILIADO AQUI]\n\n"
                f"#afiliado #promoção"
            )
            
            novo_registro = {
                "tipo": "anuncio",
                "nome_produto": nome_produto.strip(),
                "anuncio": anuncio,
                "data_hora": datetime.now().isoformat()
            }
            st.session_state.historico.append(novo_registro)
            salvar_historico(st.session_state.historico)
            
            st.success("✅ Anúncio gerado com sucesso!")
            st.text_area("Seu anúncio:", value=anuncio, height=180)

# ==============================
# Página: Histórico
# ==============================
elif pagina == "Histórico":
    st.title("📜 Histórico")
    
    if st.session_state.historico:
        historico_ordenado = sorted(
            st.session_state.historico,
            key=lambda x: x["data_hora"],
            reverse=True
        )
        
        for item in historico_ordenado:
            data_fmt = datetime.fromisoformat(item["data_hora"]).strftime("%d/%m/%Y %H:%M:%S")
            
            if item["tipo"] == "pesquisa_v2":
                st.markdown(f"**🔍 Análise de Produto** • {data_fmt}")
                st.write(f"- Palavras-chave: {', '.join(item['palavras_chave'])}")
                st.write(f"- Plataforma: {item['plataforma']}")
                st.write(f"- Tipo: {item['tipo_produto']}")
                st.write(f"- Comissão: {item['comissao']}%")
                st.write(f"- País: {item['pais']}")
                st.write(f"- Pagamento: {item['tipo_pagamento']}")
                st.write(f"- Score: {item['score']}/100 ({item['classificacao']})")
                st.write(f"- Explicação: {item['explicacao']}")
                
            elif item["tipo"] == "anuncio":
                st.markdown(f"**✍️ Anúncio** • {data_fmt}")
                st.write(f"- Produto: {item['nome_produto']}")
                st.text_area("", value=item["anuncio"], height=120, key=f"anuncio_{item['data_hora']}")
            
            if st.button("🗑️ Apagar", key=f"del_{item['data_hora']}"):
                st.session_state.historico.remove(item)
                salvar_historico(st.session_state.historico)
                st.rerun()
            
            st.markdown("---")
    else:
        st.info("Nenhum registro ainda. Faça uma análise ou gere um anúncio para começar!")

# ==============================
# Página: Configurações
# ==============================
elif pagina == "Configurações":
    st.title("⚙️ Configurações")
    st.write("""
    **Informações importantes:**
    
    - Todos os dados são salvos localmente no arquivo `historico_afiliacao.json`
    - O app não usa APIs externas, internet ou serviços pagos
    - Nenhuma informação sensível é armazenada
    - Você pode editar o código diretamente no GitHub a qualquer momento
    
    Este é um app estável, simples e 100% editável.
    """)
    
    st.markdown("---")
    st.subheader("📌 Passo a passo para atualizar este app:")
    st.write("""
    1. No GitHub, abra o repositório `MSSP-AFILIAÇÃO-O-EU`
    2. Clique em `app.py`
    3. Clique no ícone de lápis (✏️) para editar
    4. Cole o novo código completo (substitua tudo)
    5. Clique em “Commit changes”
    6. Atualize o app no Streamlit Cloud (F5)
    
    Após analisar um produto:
    - Revise o score e a explicação
    - Decida manualmente se quer promover
    - Use a página “Ideias de Anúncio” para criar conteúdo
    - Nunca confie cegamente na análise automática
    """)

# ==============================
# INSTRUÇÕES FINAIS (para o utilizador)
# ==============================
# 1. Onde o código foi alterado:
#    - Apenas na página "Pesquisa de Produtos"
#    - Alterações: palavras-chave (máx 7), plataforma (selectbox + texto), comissão (mínimo 1%), país (aceita "Europa")
#
# 2. Como colar no app.py:
#    - Substitua TODO o conteúdo do ficheiro app.py por este código
#    - Salve com "Commit changes"
#
# 3. O que não deve ser testado ainda:
#    - Não teste com mais de 7 palavras-chave até confirmar que o aviso aparece
#    - Não tente integrar com APIs reais — este é um simulador
#    - Não espere execução automática — todas as ações requerem confirmação manual
