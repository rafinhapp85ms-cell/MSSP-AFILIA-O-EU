elif pagina == "Rafinha":
    st.title("💬 Rafinha — Cérebro da MSSP")
    
    # Caixa fixa no topo
    caixa_altura = 300
    caixa_css = f"""
    <style>
        #msg-box {{
            position: fixed;
            top: 80px;
            left: 50%;
            transform: translateX(-50%);
            width: 80%;
            max-width: 700px;
            height: {caixa_altura}px;
            overflow-y: auto;
            background: #f7f7f7;
            border: 2px solid #ccc;
            padding: 10px;
            border-radius: 10px;
            z-index: 9999;
        }}
        .mensagem-user {{ text-align: right; background:#e0f7fa; padding:5px; border-radius:5px; margin:2px 0; }}
        .mensagem-rafinha {{ text-align: left; background:#f1f8e9; padding:5px; border-radius:5px; margin:2px 0; }}
    </style>
    """
    st.markdown(caixa_css, unsafe_allow_html=True)
    
    # Inicializa histórico se não existir
    if "rafael_historico" not in st.session_state:
        st.session_state.rafael_historico = []
    
    # Exibe mensagens dentro da caixa
    st.markdown("<div id='msg-box'>", unsafe_allow_html=True)
    for msg in st.session_state.rafael_historico:
        autor = msg.get("autor", "desconhecido")
        texto = msg.get("texto", "")
        if autor == "user":
            st.markdown(f"<div class='mensagem-user'>{texto}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='mensagem-rafinha'>{texto}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Caixa de input fixa abaixo da caixa de mensagens
    user_input = st.text_input("Digite aqui para Rafinha:", key="input_rafinha")
    if st.button("Enviar", key="btn_rafinha") and user_input.strip():
        # Adiciona mensagem do usuário
        st.session_state.rafael_historico.append({"autor": "user", "texto": user_input.strip()})
        
        # Resposta do Rafinha (exemplo simples, depois podemos integrar lógica real)
        resposta = f"Rafinha recebeu: {user_input.strip()}"
        st.session_state.rafael_historico.append({"autor": "rafinha", "texto": resposta})
        
        st.experimental_rerun()  # Atualiza a tela para mostrar a rolagem
