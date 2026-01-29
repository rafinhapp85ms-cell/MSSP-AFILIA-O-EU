elif pagina == "Rafinha":
    st.title("🧠 Rafinha — Cérebro Interno da MSSP")
    st.caption("Sou seu parceiro, guardião e resolvedor.")
    
    # Carregar histórico
    hist = st.session_state.rafael_historico
    
    # Mostrar mensagens
    for m in hist[-10:]:
        u = m.get("usuario", "").strip()
        r = m.get("resposta", "").strip()
        if u:
            st.markdown(f'<div style="text-align:right; background:#e3f2fd; padding:8px; margin:4px 0; border-radius:6px;">Você: {u}</div>', unsafe_allow_html=True)
        if r:
            st.markdown(f'<div style="background:#f1f8e9; padding:8px; margin:4px 0; border-radius:6px;">Rafinha: {r}</div>', unsafe_allow_html=True)
    
    # Form com limpeza automática
    with st.form(key="rafinha_form", clear_on_submit=True):
        msg = st.text_input("Sua mensagem:", key="msg_input", label_visibility="collapsed")
        if st.form_submit_button("Enviar"):
            if msg.strip():
                resp = "✅ Tá lindo, parceiro!" if "tá lindo" in msg.lower() else "❌ Caralho, deu ruim?"
                hist.append({"usuario": msg.strip(), "resposta": resp, "data_hora": datetime.now().isoformat()})
                st.session_state.rafael_historico = hist
                salvar_rafael_historico(hist)
                st.rerun()
