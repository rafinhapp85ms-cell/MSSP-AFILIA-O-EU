import streamlit as st
import json
import os
import datetime

st.set_page_config(page_title="MSSP Afiliado", layout="wide", initial_sidebar_state="expanded")

# Arquivos
HISTORICO = "historico_afiliacao.json"
RAFAEL_HIST = "rafael_historico.json"
DADOS_POSTAR = "dados_postar.json"
STATE = "state.json"
COLAB = "colaboradores.json"

def safe_load(f):
    return json.load(open(f, "r", encoding="utf-8")) if os.path.exists(f) else []

if "historico" not in st.session_state:
    st.session_state.historico = safe_load(HISTORICO)
if "rafael_historico" not in st.session_state:
    st.session_state.rafael_historico = safe_load(RAFAEL_HIST)

# Sidebar
st.sidebar.title("MSSP Afiliado")
pagina = st.sidebar.radio("Seções", ["Início", "Postar", "Rafinha"], index=0)

if pagina == "Início":
    st.title("🎯 MSSP Afiliado")
    st.info("Funcionando.")

elif pagina == "Postar":
    st.title("📤 Postar")
    st.text_input("YouTube - Usuário:", "")
    st.text_input("YouTube - Senha:", type="password")
    if st.button("Salvar"): st.success("OK")

elif pagina == "Rafinha":
    st.title("🧠 Rafinha")
    st.caption("Cérebro interno.")
    
    hist = st.session_state.rafael_historico
    for m in hist[-5:]:
        u = m.get("usuario", "").strip()
        r = m.get("resposta", "").strip()
        if u: st.markdown(f'<div style="text-align:right; background:#e3f2fd; padding:6px;">Você: {u}</div>', unsafe_allow_html=True)
        if r: st.markdown(f'<div style="background:#f1f8e9; padding:6px;">Rafinha: {r}</div>', unsafe_allow_html=True)
    
    with st.form(key="rf", clear_on_submit=True):
        msg = st.text_input("Mensagem:", key="msg", label_visibility="collapsed")
        if st.form_submit_button("Enviar"):
            if msg.strip():
                resp = "Tá lindo, parceiro!" if "tá lindo" in msg.lower() else "Caralho, deu ruim?"
                hist.append({"usuario": msg, "resposta": resp, "data_hora": datetime.datetime.now().isoformat()})
                st.session_state.rafael_historico = hist
                st.rerun()
