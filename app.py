elif pagina == "Rafinha":
    st.title("🧠 Rafinha — Cérebro Interno da MSSP")
    st.caption("Sou seu parceiro, guardião e resolvedor. Falo direto, aprendo rápido e protejo a MSSP.")

    # CSS para caixa de input fixa na parte inferior
    st.markdown(
        """
        <style>
        .input-sticky {
            position: sticky;
            bottom: 0;
            background-color: white;
            padding: 16px 0;
            margin-top: 20px;
            border-top: 1px solid #e0e0e0;
            z-index: 100;
        }
        .chat-bubble {
            max-width: 800px;
            margin: 0 auto;
            padding: 12px;
            border-radius: 12px;
            margin-bottom: 12px;
            font-size: 15px;
            line-height: 1.5;
        }
        .user-bubble {
            background-color: #e3f2fd;
            color: #0d47a1;
            text-align: right;
            border-left: 4px solid #1976d2;
        }
        .rafinha-bubble {
            background-color: #f1f8e9;
            color: #1b5e20;
            text-align: left;
            border-left: 4px solid #388e3c;
        }
        .alert-error { color: #d32f2f !important; font-weight: bold; }
        .alert-warning { color: #ed6c02 !important; font-weight: bold; }
        .alert-success { color: #2e7d32 !important; font-weight: bold; }
        </style>
        """,
        unsafe_allow_html=True
    )

    historico = st.session_state.rafael_historico

    # Exibir mensagens
    chat_container = st.container()
    with chat_container:
        if historico:
            for msg in historico[-20:]:
                usuario_msg = msg.get("usuario", "").strip()
                resposta_msg = msg.get("resposta", "").strip()
                
                if usuario_msg:
                    st.markdown(
                        f'<div class="chat-bubble user-bubble">Você: {usuario_msg}</div>',
                        unsafe_allow_html=True
                    )
                if resposta_msg:
                    if "❌" in resposta_msg:
                        resposta_msg = f'<span class="alert-error">{resposta_msg}</span>'
                    elif "⚠️" in resposta_msg:
                        resposta_msg = f'<span class="alert-warning">{resposta_msg}</span>'
                    elif "✅" in resposta_msg:
                        resposta_msg = f'<span class="alert-success">{resposta_msg}</span>'
                    st.markdown(
                        f'<div class="chat-bubble rafinha-bubble">Rafinha: {resposta_msg}</div>',
                        unsafe_allow_html=True
                    )
        else:
            st.markdown(
                '<div style="text-align:center; padding:20px; color:#757575;">💬 Me fala o que tá rolando, parceiro!</div>',
                unsafe_allow_html=True
            )

    # Caixa de entrada fixa na parte inferior
    st.markdown('<div class="input-sticky">', unsafe_allow_html=True)
    col1, col2 = st.columns([4, 1])
    with col1:
        entrada_usuario = st.text_input(
            "Sua mensagem para o Rafinha:",
            placeholder="Ex: Tem erro? O que falta? Tá lindo?",
            key="input_rafinha",
            label_visibility="collapsed"
        )
    with col2:
        if st.button("Enviar", key="btn_enviar_rafinha", use_container_width=True):
            if entrada_usuario.strip():
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

                nova_msg = {
                    "usuario": entrada_usuario.strip(),
                    "resposta": resposta,
                    "data_hora": datetime.now().isoformat()
                }
                historico.append(nova_msg)
                st.session_state.rafael_historico = historico
                salvar_rafael_historico(historico)
                
                # Força scroll automático para o final
                st.components.v1.html(
                    """
                    <script>
                    setTimeout(() => {
                        const messages = document.querySelectorAll('.chat-bubble');
                        if (messages.length > 0) {
                            messages[messages.length - 1].scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                        }
                    }, 100);
                    </script>
                    """,
                    height=0
                )
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Status sidebar
    st.sidebar.markdown("### 📊 Status da MSSP")
    estado = st.session_state.estado_mssp
    st.sidebar.write(f"**Versão:** {estado.get('versao', 'Desconhecida')}")
    st.sidebar.write(f"**Automação:** {estado.get('status_automacao', 'Desconhecido')}")
    st.sidebar.write(f"**Módulos ativos:** {sum(1 for v in estado.get('modulos', {}).values() if v)}")
