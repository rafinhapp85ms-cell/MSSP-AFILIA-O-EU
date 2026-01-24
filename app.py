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
# Página: Pesquisa de Produtos
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
            palavras_lista = [p.strip() for p in palavras_chave_input.split(",") if p.strip()]
            if len(palavras_lista) == 0:
                st.warning("⚠️ Insira pelo menos uma palavra-chave.")
            elif len(palavras_lista) > 7:
                st.warning("⚠️ Limite máximo: 7 palavras-chave. Remova algumas para continuar.")
            else:
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
# Página: Ideias de Anúncio (ATUALIZADA)
# ==============================
elif pagina == "Ideias de Anúncio":
    st.title("✍️ Ideias de Anúncio")
    
    nome_produto = st.text_input(
        "Nome do produto:",
        placeholder="Ex: Curso de Dropshipping"
    )
    
    grau_anuncio = st.selectbox(
        "Grau do anúncio:",
        ["Conservador", "Equilibrado", "Agressivo", "Curto", "Longo"]
    )
    
    plataformas_anuncio = [
        "Instagram Post",
        "Instagram Reels",
        "TikTok",
        "Facebook",
        "Pinterest",
        "Descrição de página de vendas",
        "Outra"
    ]
    plataforma_anuncio = st.selectbox(
        "Tipo de plataforma:",
        options=plataformas_anuncio
    )
    if plataforma_anuncio == "Outra":
        plataforma_anuncio_manual = st.text_input("Digite a plataforma:", key="plataforma_anuncio_manual")
        if plataforma_anuncio_manual.strip():
            plataforma_anuncio = plataforma_anuncio_manual.strip()
    
    ctas = [
        "Comprar agora",
        "Ver oferta",
        "Frete grátis na Europa",
        "Pagamento na entrega",
        "Últimas unidades"
    ]
    cta_selecionado = st.multiselect(
        "Chamada para ação (CTA):",
        options=ctas,
        default=["Comprar agora"]
    )
    
    if st.button("✨ Gerar anúncio"):
        if not nome_produto.strip():
            st.warning("⚠️ Por favor, digite o nome do produto.")
        else:
            # Definir tom com base no grau
            if grau_anuncio == "Conservador":
                tom_pt = "Descubra o"
                tom_en = "Discover the"
            elif grau_anuncio == "Equilibrado":
                tom_pt = "Não perca o"
                tom_en = "Don't miss the"
            elif grau_anuncio == "Agressivo":
                tom_pt = "🔥 CORRA! O"
                tom_en = "🔥 HURRY! The"
            elif grau_anuncio == "Curto":
                tom_pt = "Conheça"
                tom_en = "Meet"
            else:  # Longo
                tom_pt = "Apresentamos com orgulho o incrível"
                tom_en = "We proudly present the amazing"
            
            # Montar CTA
            cta_texto_pt = " | ".join(cta_selecionado)
            cta_texto_en = " | ".join([
                "Buy now" if c == "Comprar agora" else
                "See offer" if c == "Ver oferta" else
                "Free shipping in Europe" if c == "Frete grátis na Europa" else
                "Cash on delivery" if c == "Pagamento na entrega" else
                "Last units available"
                for c in cta_selecionado
            ])
            
            # Anúncio em português
            anuncio_pt = (
                f"{tom_pt} {nome_produto}!\n\n"
                f"✅ Qualidade premium garantida\n"
                f"✅ Entrega rápida\n"
                f"✅ Preço especial por tempo limitado\n\n"
                f"👉 {cta_texto_pt}\n"
                f"[LINK DE AFILIADO AQUI]\n\n"
                f"#afiliado #{plataforma_anuncio.replace(' ', '').lower()}"
            )
            
            # Anúncio em inglês
            anuncio_en = (
                f"{tom_en} {nome_produto}!\n\n"
                f"✅ Premium quality guaranteed\n"
                f"✅ Fast delivery\n"
                f"✅ Special price for a limited time\n\n"
                f"👉 {cta_texto_en}\n"
                f"[AFFILIATE LINK HERE]\n\n"
                f"#affiliate #{plataforma_anuncio.replace(' ', '').lower()}"
            )
            
            # Salvar no histórico
            novo_registro = {
                "tipo": "anuncio_v2",
                "nome_produto": nome_produto.strip(),
                "grau": grau_anuncio,
                "plataforma": plataforma_anuncio,
                "ctas": cta_selecionado,
                "anuncio_pt": anuncio_pt,
                "anuncio_en": anuncio_en,
                "data_hora": datetime.now().isoformat()
            }
            st.session_state.historico.append(novo_registro)
            salvar_historico(st.session_state.historico)
            
            # Mostrar os anúncios
            st.success("✅ Anúncios gerados com sucesso!")
            
            st.subheader("🇵🇹 Português")
            st.text_area("", value=anuncio_pt, height=180, key="anuncio_pt")
            
            st.subheader("🇬🇧 Inglês")
            st.text_area("", value=anuncio_en, height=180, key="anuncio_en")

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
                
            elif item["tipo"] == "anuncio_v2":
                st.markdown(f"**✍️ Anúncio Bilingue** • {data_fmt}")
                st.write(f"- Produto: {item['nome_produto']}")
                st.write(f"- Grau: {item['grau']}")
                st.write(f"- Plataforma: {item['plataforma']}")
                st.write(f"- CTA: {', '.join(item['ctas'])}")
                st.subheader("🇵🇹 Português")
                st.text_area("", value=item["anuncio_pt"], height=120, key=f"pt_{item['data_hora']}")
                st.subheader("🇬🇧 Inglês")
                st.text_area("", value=item["anuncio_en"], height=120, key=f"en_{item['data_hora']}")
            
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
