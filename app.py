# ==============================
# Rafinha - Caixa de Mensagens Fixa
# ==============================
import streamlit as st
import json
import os
from datetime import datetime

RAFAEL_HISTORICO_ARQUIVO = "rafael_historico.json"

# ==============================
# Funções de persistência do histórico
# ==============================
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
# Inicialização
# ==============================
if "rafinha_historico" not in st.session_state:
    st.session_state.rafinha_historico = carregar_rafael_historico()

if "rafinha_input" not in st.session_state:
    st.session_state.rafinha_input = ""

# ==============================
# Caixa de mensagem fixa no topo
# ==============================
st.markdown("""
<style>
.rafinha-box {
    position: fixed;
    top: 10px;
    left: 50%;
    transform: translateX(-50%);
    width: 80%;
    max-width: 700px;
    background-color: #f7f7f7;
    border: 2px solid #333;
    border-radius: 10px;
    padding: 10px;
    z-index: 9999;
}
.rafinha-messages {
    max-height: 300px;
    overflow-y: auto;
    padding: 5px;
    border-top: 1px solid #ccc;
    margin-top: 5px;
}
.rafinha-message-user {
    text-align: right;
    color: white;
    background-color: #007bff;
    padding: 5px 10px;
    border-radius: 8px;
    margin-bottom: 5px;
    display: inline-block;
}
.rafinha-message-rafinha {
    text-align: left;
    color: white;
    background-color: #28a745;
    padding: 5px 10px;
    border-radius: 8px;
    margin-bottom: 5px;
    display: inline-block;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="rafinha-box">', unsafe_allow_html=True)

# Mensagens
st.markdown('<div class="rafinha-messages" id="rafinha-messages">', unsafe_allow_html=True)
for msg in st.session_state.rafinha_historico:
    if msg["autor"] == "user":
        st.markdown(f'<div class="rafinha-message-user">{msg["texto"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="rafinha-message-rafinha">{msg["texto"]}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Input para enviar mensagem
rafinha_input = st.text_input("💬 Enviar mensagem para Rafinha:", st.session_state.rafinha_input, key="rafinha_input_box")
enviar = st.button("Enviar")

if enviar and rafinha_input.strip():
    # Adiciona mensagem do usuário
    st.session_state.rafinha_historico.append({
        "autor": "user",
        "texto": rafinha_input.strip(),
        "data": datetime.now().isoformat()
    })
    
    # Simula resposta do Rafinha (pode ser substituído pela lógica real dele)
    resposta_rafinha = f"Rafinha recebeu: {rafinha_input.strip()} — tudo certo, caralho!"
    
    st.session_state.rafinha_historico.append({
        "autor": "rafinha",
        "texto": resposta_rafinha,
        "data": datetime.now().isoformat()
    })
    
    st.session_state.rafinha_input = ""  # limpa input
    salvar_rafael_historico(st.session_state.rafinha_historico)
    st.experimental_rerun()  # rerun para atualizar a caixa e rolagem

st.markdown('</div>', unsafe_allow_html=True)

# Script para rolagem automática
st.markdown("""
<script>
var messagesDiv = window.parent.document.getElementById('rafinha-messages');
if(messagesDiv){
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}
</script>
""", unsafe_allow_html=True)
