import streamlit as st
import json
import os
from datetime import datetime

# Caminho do arquivo de histórico
RAFAEL_HISTORICO_ARQUIVO = "rafael_historico.json"

def carregar_historico_rafinha():
    """Carrega o histórico do Rafinha do arquivo JSON. Cria estrutura mínima se não existir."""
    if os.path.exists(RAFAEL_HISTORICO_ARQUIVO):
        try:
            with open(RAFAEL_HISTORICO_ARQUIVO, "r", encoding="utf-8") as f:
                dados = json.load(f)
                # Garante que a estrutura tenha 'mensagens'
                if "mensagens" not in dados:
                    dados["mensagens"] = []
                return dados
        except (json.JSONDecodeError, IOError):
            pass
    # Estrutura padrão se o arquivo não existir ou estiver corrompido
    return {"mensagens": []}

def salvar_historico_rafinha(mensagens):
    """Salva a lista de mensagens no arquivo JSON."""
    try:
        with open(RAFAEL_HISTORICO_ARQUIVO, "w", encoding="utf-8") as f:
            json.dump({"mensagens": mensagens}, f, ensure_ascii=False, indent=2)
        return True
    except IOError:
        return False

# Inicializa o estado da sessão com o histórico carregado
if "rafael_historico" not in st.session_state:
    dados_iniciais = carregar_historico_rafinha()
    st.session_state.rafael_historico = dados_iniciais["mensagens"]

# Renderização da página Rafinha
st.title("🧠 Rafinha — Cérebro Interno da MSSP")
st.caption("Sou seu parceiro, guardião e resolvedor.")

# Exibe o histórico de mensagens
for msg in st.session_state.rafael_historico:
    autor = msg.get("autor", "")
    conteudo = msg.get("conteudo", "")
    if autor == "user":
        st.markdown(
            f'<div style="text-align:right; background:#e3f2fd; padding:10px; margin:6px 0; border-radius:8px;">Você: {conteudo}</div>',
            unsafe_allow_html=True
        )
    elif autor == "Rafinha":
        st.markdown(
            f'<div style="background:#f1f8e9; padding:10px; margin:6px 0; border-radius:8px;">Rafinha: {conteudo}</div>',
            unsafe_allow_html=True
        )

# Formulário para nova mensagem
with st.form(key="form_rafinha", clear_on_submit=True):
    entrada_usuario = st.text_input(
        "Sua mensagem para o Rafinha:",
        placeholder="Ex: Tem erro? O que falta? Tá lindo?",
        key="input_rafinha"
    )
    submitted = st.form_submit_button("Enviar")

    if submitted and entrada_usuario.strip():
        # Adiciona mensagem do usuário
        msg_usuario = {
            "autor": "user",
            "conteudo": entrada_usuario.strip(),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        st.session_state.rafael_historico.append(msg_usuario)

        # Gera resposta do Rafinha
        if "erro" in entrada_usuario.lower() or "falhou" in entrada_usuario.lower():
            resposta = "Caralho, deu ruim? Me mostra o erro que eu resolvo na hora."
        elif "tá lindo" in entrada_usuario.lower() or "bom" in entrada_usuario.lower():
            resposta = "Tá lindo, parceiro! Bora resolver o próximo desafio?"
        else:
            resposta = "Minha análise atual: modulo colaboradores ativo. state.json configurado. automacao externa ainda nao iniciada. Quer que eu resolva agora ou so registro por enquanto?"

        # Adiciona resposta do Rafinha
        msg_rafinha = {
            "autor": "Rafinha",
            "conteudo": resposta,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        st.session_state.rafael_historico.append(msg_rafinha)

        # Salva no arquivo JSON
        sucesso = salvar_historico_rafinha(st.session_state.rafael_historico)
        if sucesso:
            st.success("✅ Mensagem salva com sucesso!")
        else:
            st.error("❌ Falha ao salvar a mensagem.")

        st.rerun()
