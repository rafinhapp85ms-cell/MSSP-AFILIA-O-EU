import streamlit as st
import json
import os
from datetime import datetime

# ==============================
# Configuração da página
# ==============================
st.set_page_config(
    page_title="Rafinha Teste",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================
# Arquivo histórico Rafinha
# ==============================
RAFAEL_HISTORICO_ARQUIVO = "rafael_historico.json"

def carregar_rafael_historico():
    if os.path.exists(RAFAEL_HISTORICO_ARQUIVO):
        try:
            with open(RAFAEL_HISTORICO_ARQUIVO, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def salvar_rafael_historico(historico):
    with open(RAFAEL_HISTORICO_ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(historico, f, ensure_ascii=False, indent=2)

# ==============================
# Inicializa histórico na sessão
# ==============================
if "rafael_historico" not in st.session_state:
    st.session_state.rafael_historico = carregar_rafael_historico()

# ==============================
# Caixa fixa de mensagens
# ==============================
st.markdown("""
<style>
#mensagens-fixas {
    position: fixed;
    top: 80px;
    left: 50%;
    transform: translateX(-50%);
    width: 70%;
    max-height: 400px;
    overflow-y: auto;
    border: 2px solid #444;
    border-radius: 8px;
    padding: 10px;
    background-color: #f8f8f8;
    z-index: 9999;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div id="mensagens-fixas"></div>', unsafe_allow_html=True)

# ==============================
# Função para renderizar mensagens
# ==============================
def renderizar_mensagens():
    mensagens_html = ""
    for msg in st.session_state.rafael_historico:
        if msg["autor"] == "user":
            mensagens_html += f'<div style="text-align:left; margin-bottom:5px;"><b>Você:</b> {msg["texto"]}</div>'
        else:
            mensagens_html += f'<div style="text-align:right; margin-bottom:5px; color:blue;"><b>Rafinha:</b> {msg["texto"]}</div>'
    js_scroll = """
        <script>
        var objDiv = document.getElementById("mensagens-fixas");
        objDiv.scrollTop = objDiv.scrollHeight;
        </script>
    """
    st.markdown(f'<div id="mensagens-fixas">{mensagens_html}</div>{js_scroll}', unsafe_allow_html=True)

# ==============================
# Input de mensagem
# ==============================
mensagem_usuario = st.text_input("💬 Escreva sua mensagem para Rafinha:")

if st.button("Enviar") and mensagem_usuario.strip():
    st.session_state.rafael_historico.append({
        "autor": "user",
        "texto": mensagem_usuario.strip(),
        "data": datetime.now().isoformat()
    })
    # Simulação de resposta automática de Rafinha
    resposta_rafinha = f"Recebido: {mensagem_usuario.strip()} (Rafinha processou)"
    st.session_state.rafael_historico.append({
        "autor": "rafinha",
        "texto": resposta_rafinha,
        "data": datetime.now().isoformat()
    })
    salvar_rafael_historico(st.session_state.rafael_historico)
    st.experimental_rerun()

# Renderiza mensagens
renderizar_mensagens()
