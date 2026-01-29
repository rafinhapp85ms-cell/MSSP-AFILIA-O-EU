elif pagina == "Rafinha":
    st.title("🧠 Rafinha — Cérebro Interno da MSSP")
    st.caption("Sou seu parceiro, guardião e resolvedor. Falo direto, aprendo rápido e protejo a MSSP.")

    # Carregar histórico
    historico = st.session_state.rafael_historico

    # Exibir mensagens (acima da caixa de input)
    for msg in historico[-20:]:
        usuario_msg = msg.get("usuario", "").strip()
        resposta_msg = msg.get("resposta", "").strip()
        if usuario_msg:
            st.markdown(f"<div style='text-align:right; background:#e3f2fd; padding:8px; border-radius:8px; margin:5px 0; max-width:80%; margin-left:auto;'>Você: {usuario_msg}</div>", unsafe_allow_html=True)
        if resposta_msg:
            st.markdown(f"<div style='background:#f1f8e9; padding:8px; border-radius:8px; margin:5px 0; max-width:80%;'>Rafinha: {resposta_msg}</div>", unsafe_allow_html=True)

    # Caixa de input na parte inferior — limpa após envio
    with st.form(key="form_rafinha", clear_on_submit=True):
        entrada = st.text_input(
            "Sua mensagem para o Rafinha:",
            placeholder="Ex: Tem erro? O que falta? Tá lindo?",
            key="input_rafinha"
        )
        submitted = st.form_submit_button("Enviar")

        if submitted and entrada.strip():
            # Gerar resposta
            modulos = st.session_state.estado_mssp.get("modulos", {})
            automacao = st.session_state.estado_mssp.get("status_automacao", "desativada")
            
            if "erro" in entrada.lower() or "falhou" in entrada.lower():
                resposta = "❌ Caralho, deu ruim? Me mostra o erro que eu resolvo na hora."
            elif "tá lindo" in entrada.lower() or "bom" in entrada.lower():
                resposta = "✅ Tá lindo, parceiro! Bora resolver o próximo desafio?"
            else:
                resposta = "**Minha análise atual:**\n\n✅ Feito: Módulo de Colaboradores ativo\n⚠️ Falta fazer: Automação externa\n\nQuer que eu resolva agora ou só registre?"

            # Salvar
            nova_msg = {
                "usuario": entrada.strip(),
                "resposta": resposta,
                "data_hora": datetime.now().isoformat()
            }
            historico.append(nova_msg)
            st.session_state.rafael_historico = historico
            salvar_rafael_historico(historico)

            # ✅ O form já limpa o campo automaticamente (gracias a `clear_on_submit=True`)
            st.rerun()
