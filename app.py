import streamlit as st
import json
import os
import datetime

# Configuração
st.set_page_config(page_title="MSSP Afiliado", layout="wide", initial_sidebar_state="expanded")

# Arquivos
HISTORICO = "historico_afiliacao.json"
RAFAEL_HIST = "rafael_historico.json"

def load(f):
    return json.load(open(f, "r", encoding="utf-8")) if os.path.exists(f) else []

def save(f, data):
    with open(f, "w", encoding="utf-8") as fp:
        json.dump(data, fp, ensure_ascii=False, indent=2)

# Inicializar sessão
if "historico" not in st.session_state:
    st.session_state.historico = load(HISTORICO)
if "rafael_historico" not in st.session_state:
    st.session_state.rafael_historico = load(RAFAEL_HIST)

# Sidebar
st.sidebar.title("MSSP Afiliado")
pagina = st.sidebar.radio("Seções", ["Início", "Pesquisa de Produtos", "Ideias de Anúncio", "Postar", "Histórico", "Colaboradores", "Rafinha", "Configurações"], index=0)

# Início
if pagina == "Início":
    st.title("🎯 MSSP Afiliado")
    st.write("Fase 2A — Análise Avançada de Produtos")
    st.info("Comece por 'Pesquisa de Produtos'")

# Rafinha — CORREÇÃO FINAL, SEM ERROS
elif pagina == "Rafinha":
    st.title("🧠 Rafinha — Cérebro Interno da MSSP")
    st.caption("Sou seu parceiro, guardião e resolvedor.")

    hist = st.session_state.rafael_historico

    # Exibir mensagens (sem KeyError)
    for msg in hist[-15:]:
        u = msg.get("usuario", "").strip()
        r = msg.get("resposta", "").strip()
        if u:
            st.markdown(f'<div style="text-align:right; background:#e3f2fd; padding:8px; margin:4px 0; border-radius:6px;">Você: {u}</div>', unsafe_allow_html=True)
        if r:
            st.markdown(f'<div style="background:#f1f8e9; padding:8px; margin:4px 0; border-radius:6px;">Rafinha: {r}</div>', unsafe_allow_html=True)

    # Form com limpeza automática
    with st.form(key="rf_form", clear_on_submit=True):
        texto = st.text_input("Sua mensagem:", key="inp_rf", label_visibility="collapsed")
        if st.form_submit_button("Enviar"):
            if texto.strip():
                resp = "✅ Tá lindo, parceiro!" if "tá lindo" in texto.lower() else "❌ Caralho, deu ruim?"
                nova = {"usuario": texto.strip(), "resposta": resp, "data_hora": datetime.datetime.now().isoformat()}
                hist.append(nova)
                st.session_state.rafael_historico = hist
                save(RAFAEL_HIST, hist)
                st.rerun()

# Outras páginas mínimas (só para não quebrar)
elif pagina == "Pesquisa de Produtos":
    st.title("🔍 Pesquisa de Produtos")
    st.text_input("Link do produto:", "")
    if st.button("Analisar"): st.success("Pronto")

elif pagina == "Ideias de Anúncio":
    st.title("✍️ Ideias de Anúncio")
    st.text_input("Nome do produto:", "")
    if st.button("Gerar"): st.success("Feito")

elif pagina == "Postar":
    st.title("📤 Postar")
    st.text_input("YouTube - Usuário:", "")
    if st.button("Salvar"): st.success("Salvo")

elif pagina == "Histórico":
    st.title("📜 Histórico")
    st.info("Vazio")

elif pagina == "Colaboradores":
    st.title("👥 Colaboradores")
    st.text_input("E-mail:", "")
    if st.button("Adicionar"): st.success("Enviado")

elif pagina == "Configurações":
    st.title("⚙️ Configurações")
    st.write("Tudo local. Sem internet.")

else:
    st.title("Início")
