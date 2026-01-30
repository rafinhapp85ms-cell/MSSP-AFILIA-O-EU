import streamlit as st
import json
import os

st.set_page_config(page_title="MSSP Afiliado", layout="wide")

# Tenta carregar state.json — se falhar, usa padrão
def load_state():
    for name in ["state.json", "estado.json"]:
        if os.path.exists(name):
            try:
                with open(name, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                pass
    # Se nenhum existir, retorna padrão
    return {
        "versao": "1.0",
        "modulos": {"pesquisa_produtos": True, "ideias_anuncio": True, "postar": True, "colaboradores": True},
        "status_automacao": "desativada"
    }

if "estado_mssp" not in st.session_state:
    st.session_state.estado_mssp = load_state()

# Sidebar
st.sidebar.title("MSSP Afiliado")
pagina = st.sidebar.radio("Seções", ["Início", "Postar", "Rafinha"], index=0)

if pagina == "Início":
    st.title("✅ MSSP está funcionando")

elif pagina == "Postar":
    st.title("📤 Postar")
    st.text_input("YouTube - Usuário:", "")
    st.text_input("YouTube - Senha:", type="password")
    if st.button("Salvar"): st.success("OK")

elif pagina == "Rafinha":
    st.title("🧠 Rafinha")
    st.text_input("Mensagem:", key="msg")
    if st.button("Enviar"): st.info("Resposta: Tá lindo, parceiro!")
