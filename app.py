# ==============================
# Página: Rafinha (CORRIGIDA)
# ==============================
elif pagina == "Rafinha":
    st.title("🧠 Rafinha — Cérebro Interno da MSSP")
    st.caption("Sou seu parceiro, guardião e resolvedor. Falo direto, aprendo rápido e protejo a MSSP.")

    # === ESTILO CSS PARA CAIXA FIXA NO TOPO CENTRAL ===
    st.markdown(
        """
        <style>
        .fixed-chat-container {
            position: relative;
            background-color: #ffffff;
            border: 1px solid #e0e0e0;
            border-radius: 12px;
            padding: 20px;
            margin: 20px auto;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            overflow: hidden;
            max-width: 800px;
            width: 95%;
        }
        .chat-messages {
            max-height: 400px;
            overflow-y: auto;
            padding-right: 8px;
        }
        .user-message {
            background-color: #e3f2fd;
            color: #0d47a1;
            padding: 12px;
            border-radius: 10px;
            margin: 10px 0;
            font-weight: 500;
            border-left: 4px solid #1976d2;
        }
        .rafinha-message {
            background-color: #f1f8e9;
            color: #1b5e20;
            padding: 12px;
            border-radius: 10px;
            margin: 10px 0;
            font-weight: 500;
            border-left: 4px solid #388e3c;
        }
        .alert-error {
            color: #d32f2f !important;
            font-weight: bold;
        }
        .alert-warning {
            color: #ed6c02 !important;
            font-weight: bold;
        }
        .alert-success {
            color: #2e7d32 !important;
            font-weight: bold;
        }
        @media (max-width: 768px) {
            .fixed-chat-container {
                margin: 15px auto;
                padding: 15px;
                width: 95%;
            }
            .chat-messages {
                max-height: 300px;
            }
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # === CAIXA DE ENTRADA FIXA NO TOPO CENTRAL ===
    st.markdown('<div class="fixed-chat-container">', unsafe_allow_html=True)
    
    # Campo de entrada fixo no topo
    entrada_usuario = st.text_input(
        "Sua mensagem para o Rafinha:",
        placeholder="Ex: Tem erro? O que falta? Tá lindo?",
        key="input_rafinha"
    )
    
    col1, col2 = st.columns([1, 5])
    with col1:
        enviar_btn = st.button("Enviar", key="btn_enviar_rafinha")
    with col2:
        st.empty()
    
    st.markdown('</div>', unsafe_allow_html=True)

    # === PROCESSAMENTO DO ENVIO ===
    if enviar_btn and entrada_usuario.strip():
        # Gerar resposta do Rafinha
        modulos = st.session_state.estado_mssp.get("modulos", {})
        automacao = st.session_state.estado_mssp.get("status_automacao", "desativada")
        
        if "erro" in entrada_usuario.lower() or "falhou" in entrada_usuario.lower():
            resposta = "❌ Caralho, deu ruim? Me mostra o erro que eu resolvo na hora."
        elif "tá lindo" in entrada_usuario.lower() or "bom" in entrada_usuario.lower():
            resposta = "✅ Tá lindo, parceiro! Bora resolver o próximo desafio?"
        else:
            progresso = []
            pendencias = []
            
            if modulos.get("colaboradores"):
                progresso.append("Módulo de Colaboradores: ativo com envio real de e-mail")
            else:
                pendencias.append("Módulo de Colaboradores desativado")
            
            if automacao == "desativada":
                pendencias.append("Automação externa ainda não iniciada")
            
            if os.path.exists("state.json"):
                progresso.append("state.json configurado")
            else:
                pendencias.append("state.json ausente — mas já recriei automaticamente")
            
            resposta = "**Minha análise atual:**\n\n"
            if progresso:
                resposta += "✅ **Feito:**\n" + "\n".join(f"- {p}" for p in progresso) + "\n\n"
            if pendencias:
                resposta += "⚠️ **Falta fazer:**\n" + "\n".join(f"- {p}" for p in pendencias) + "\n\n"
            resposta += "Quer que eu resolva agora ou só registre por enquanto?"

        # Salvar no histórico com estrutura correta
        nova_msg = {
            "usuario": entrada_usuario.strip(),
            "resposta": resposta,
            "data_hora": datetime.now().isoformat()
        }
        historico = st.session_state.rafael_historico
        historico.append(nova_msg)
        st.session_state.rafael_historico = historico
        salvar_rafael_historico(historico)
        st.rerun()

    # === EXIBIÇÃO DAS MENSAGENS (COM SEGURANÇA CONTRA KeyError) ===
    st.markdown('<div class="fixed-chat-container">', unsafe_allow_html=True)
    st.markdown('<div class="chat-messages">', unsafe_allow_html=True)
    
    historico = st.session_state.rafael_historico
    
    if historico:
        for msg in historico[-20:]:  # Mostrar últimas 20 mensagens
            # Verificação segura das chaves
            usuario_msg = msg.get("usuario", "")
            resposta_msg = msg.get("resposta", "")
            
            # Mensagem do usuário
            if usuario_msg:
                st.markdown(
                    f'<div class="user-message">Você: {usuario_msg}</div>',
                    unsafe_allow_html=True
                )
            # Resposta do Rafinha
            if resposta_msg:
                if "❌" in resposta_msg:
                    resposta_formatada = f'<span class="alert-error">{resposta_msg}</span>'
                elif "⚠️" in resposta_msg:
                    resposta_formatada = f'<span class="alert-warning">{resposta_msg}</span>'
                elif "✅" in resposta_msg:
                    resposta_formatada = f'<span class="alert-success">{resposta_msg}</span>'
                else:
                    resposta_formatada = resposta_msg
                
                st.markdown(
                    f'<div class="rafinha-message">Rafinha: {resposta_formatada}</div>',
                    unsafe_allow_html=True
                )
    else:
        st.markdown(
            '<div class="rafinha-message">Rafinha: 💬 Me fala o que tá rolando, parceiro!</div>',
            unsafe_allow_html=True
        )
    
    st.markdown('</div>', unsafe_allow_html=True)  # Fecha .chat-messages
    st.markdown('</div>', unsafe_allow_html=True)  # Fecha .fixed-chat-container

    # Status na sidebar
    st.sidebar.markdown("### 📊 Status da MSSP")
    estado = st.session_state.estado_mssp
    st.sidebar.write(f"**Versão:** {estado.get('versao', 'Desconhecida')}")
    st.sidebar.write(f"**Automação:** {estado.get('status_automacao', 'Desconhecido')}")
    st.sidebar.write(f"**Módulos ativos:** {sum(1 for v in estado.get('modulos', {}).values() if v)}")
