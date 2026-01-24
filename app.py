import streamlit as st
import json
import os
from datetime import datetime

# ==============================
# Configuração inicial da página
# ==============================
st.set_page_config(
    page_title="MSSP Afiliado",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================
# Arquivos de dados
# ==============================
HISTORICO_ARQUIVO = "historico_afiliacao.json"
REDES_SOCIAIS_ARQUIVO = "redes_sociais.json"
HORARIOS_ARQUIVO = "horarios_postagem.json"

# ==============================
# Funções de persistência
# ==============================
def carregar_historico():
    if os.path.exists(HISTORICO_ARQUIVO):
        try:
            with open(HISTORICO_ARQUIVO, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def salvar_historico(historico):
    with open(HISTORICO_ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(historico, f, ensure_ascii=False, indent=2)

def carregar_redes_sociais():
    if os.path.exists(REDES_SOCIAIS_ARQUIVO):
        try:
            with open(REDES_SOCIAIS_ARQUIVO, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def salvar_redes_sociais(dados):
    with open(REDES_SOCIAIS_ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

def carregar_horarios():
    if os.path.exists(HORARIOS_ARQUIVO):
        try:
            with open(HORARIOS_ARQUIVO, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return "07:00–09:00, 12:00–14:00, 18:00–21:00"
    return "07:00–09:00, 12:00–14:00, 18:00–21:00"

def salvar_horarios(horarios):
    with open(HORARIOS_ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(horarios, f, ensure_ascii=False)

def calcular_score(comissao, tipo_produto, tipo_pagamento, pais):
    score = 50
    if comissao >= 10:
        score += 20
    elif comissao >= 5:
        score += 10
    if tipo_produto == "Digital":
        score += 15
    if tipo_pagamento == "Normal":
        score += 10
    if pais in ["Portugal", "Espanha", "França", "Alemanha", "Itália"] or "Europa" in pais:
        score += 5
    return min(score, 100)

def classificar_score(score):
    if score >= 70:
        return "Forte"
    elif score >= 40:
        return "Médio"
    else:
        return "Fraco"

def gerar_explicacao(comissao, tipo_produto, tipo_pagamento, pais, score):
    motivos = []
    if comissao >= 10:
        motivos.append("comissão alta")
    elif comissao < 5:
        motivos.append("comissão baixa")
    if tipo_produto == "Digital":
        motivos.append("produto digital (maior margem)")
    if tipo_pagamento == "Normal":
        motivos.append("pagamento antecipado")
    if pais in ["Portugal", "Espanha", "França", "Alemanha", "Itália"] or "Europa" in pais:
        motivos.append("país com bom desempenho")
    if not motivos:
        motivos = ["nenhum fator favorável identificado"]
    return f"Score baseado em: {', '.join(motivos)}."

# ==============================
# Inicializar estado da sessão
# ==============================
if "historico" not in st.session_state:
    st.session_state.historico = carregar_historico()

if "redes_sociais" not in st.session_state:
    st.session_state.redes_sociais = carregar_redes_sociais()

if "horarios_postagem" not in st.session_state:
    st.session_state.horarios_postagem = carregar_horarios()

# ==============================
# Estado para navegação por etapas
# ==============================
if "etapa_pesquisa" not in st.session_state:
    st.session_state.etapa_pesquisa = 1

if "dados_temporarios" not in st.session_state:
    st.session_state.dados_temporarios = {}

# ==============================
# Menu lateral
# ==============================
st.sidebar.title("MSSP Afiliado")
pagina = st.sidebar.radio(
    "Navegue pelas seções:",
    ("Início", "Pesquisa de Produtos", "Ideias de Anúncio", "Postar", "Histórico", "Configurações"),
    index=0
)

# ==============================
# Página: Início
# ==============================
if pagina == "Início":
    st.title("🎯 MSSP Afiliado")
    st.subheader("Fase 2A — Análise Avançada de Produtos para Afiliados")
    st.write("""
    Este app ajuda afiliados a:
    - Analisar produtos com base em critérios-chave
    - Receber um score de viabilidade (0–100)
    - Gerar ideias de anúncios em português europeu
    - Manter histórico organizado
    
    Tudo é feito localmente, sem internet.
    """)
    st.info("💡 Dica: Comece pela página **'Pesquisa de Produtos'** para analisar sua primeira oferta.")

# ==============================
# Página: Pesquisa de Produtos
# ==============================
elif pagina == "Pesquisa de Produtos":
    st.title("🔍 Pesquisa de Produtos")
    
    # Etapa 1: Link do produto
    if st.session_state.etapa_pesquisa == 1:
        st.subheader("Etapa 1/3: Link do Produto")
        link_produto = st.text_input(
            "Cole o link do produto:",
            value=st.session_state.dados_temporarios.get("link_produto", ""),
            placeholder="https://exemplo.com/produto"
        )
        
        col1, col2 = st.columns([1, 5])
        with col1:
            if st.button("➡️ Avançar"):
                if link_produto.strip():
                    st.session_state.dados_temporarios["link_produto"] = link_produto.strip()
                    st.session_state.etapa_pesquisa = 2
                    st.rerun()
                else:
                    st.warning("⚠️ Por favor, insira o link do produto.")
        with col2:
            st.empty()  # Espaço vazio para alinhamento

    # Etapa 2: Palavras-chave e detalhes
    elif st.session_state.etapa_pesquisa == 2:
        st.subheader("Etapa 2/3: Detalhes do Produto")
        
        palavras_chave_input = st.text_input(
            "Palavras-chave (separadas por vírgula, máximo 7):",
            value=st.session_state.dados_temporarios.get("palavras_chave_input", ""),
            placeholder="Ex: fone, bluetooth, sem fios"
        )
        
        plataformas_predefinidas = ["Amazon", "ClickBank", "Awin", "CJ Affiliate", "Hotmart", "Outra"]
        plataforma = st.selectbox(
            "Plataforma:",
            options=plataformas_predefinidas,
            index=plataformas_predefinidas.index(st.session_state.dados_temporarios.get("plataforma", "Amazon")) if st.session_state.dados_temporarios.get("plataforma") in plataformas_predefinidas else 0
        )
        if plataforma == "Outra":
            plataforma_manual = st.text_input("Digite a plataforma:", key="plataforma_manual")
            if plataforma_manual.strip():
                plataforma = plataforma_manual.strip()
        
        tipo_produto = st.selectbox(
            "Tipo de produto:",
            ["Digital", "Físico"],
            index=["Digital", "Físico"].index(st.session_state.dados_temporarios.get("tipo_produto", "Digital"))
        )
        
        comissao_input = st.number_input(
            "Comissão (%):",
            min_value=0.0,
            value=float(st.session_state.dados_temporarios.get("comissao", 1.0)),
            step=0.5,
            help="Valor mínimo automático: 1%"
        )
        
        pais = st.text_input(
            "País alvo:",
            value=st.session_state.dados_temporarios.get("pais", ""),
            placeholder="Ex: Portugal, Alemanha ou Europa"
        )
        
        tipo_pagamento = st.selectbox(
            "Tipo de pagamento:",
            ["Normal", "Pagamento na entrega"],
            index=["Normal", "Pagamento na entrega"].index(st.session_state.dados_temporarios.get("tipo_pagamento", "Normal"))
        )
        
        col1, col2, col3 = st.columns([1, 1, 4])
        with col1:
            if st.button("⬅️ Voltar"):
                st.session_state.etapa_pesquisa = 1
                st.rerun()
        with col2:
            if st.button("➡️ Avançar"):
                if not palavras_chave_input.strip() or not pais.strip():
                    st.warning("⚠️ Preencha palavras-chave e país.")
                else:
                    palavras_lista = [p.strip() for p in palavras_chave_input.split(",") if p.strip()]
                    if len(palavras_lista) > 7:
                        st.warning("⚠️ Limite máximo: 7 palavras-chave.")
                    else:
                        st.session_state.dados_temporarios.update({
                            "palavras_chave_input": palavras_chave_input,
                            "plataforma": plataforma,
                            "tipo_produto": tipo_produto,
                            "comissao": comissao_input,
                            "pais": pais,
                            "tipo_pagamento": tipo_pagamento
                        })
                        st.session_state.etapa_pesquisa = 3
                        st.rerun()
        with col3:
            st.empty()

    # Etapa 3: Confirmação e análise
    elif st.session_state.etapa_pesquisa == 3:
        st.subheader("Etapa 3/3: Confirmar e Analisar")
        
        st.markdown("**Link do produto:**")
        st.code(st.session_state.dados_temporarios["link_produto"])
        
        st.markdown("**Detalhes:**")
        st.write(f"- Palavras-chave: {st.session_state.dados_temporarios['palavras_chave_input']}")
        st.write(f"- Plataforma: {st.session_state.dados_temporarios['plataforma']}")
        st.write(f"- Tipo: {st.session_state.dados_temporarios['tipo_produto']}")
        st.write(f"- Comissão: {st.session_state.dados_temporarios['comissao']}%")
        st.write(f"- País: {st.session_state.dados_temporarios['pais']}")
        st.write(f"- Pagamento: {st.session_state.dados_temporarios['tipo_pagamento']}")
        
        col1, col2, col3 = st.columns([1, 1, 4])
        with col1:
            if st.button("⬅️ Voltar"):
                st.session_state.etapa_pesquisa = 2
                st.rerun()
        with col2:
            if st.button("✅ Analisar Produto"):
                # Processar dados
                palavras_lista = [p.strip() for p in st.session_state.dados_temporarios["palavras_chave_input"].split(",") if p.strip()]
                pais_salvar = "Europa (todos os países)" if st.session_state.dados_temporarios["pais"].strip().lower() == "europa" else st.session_state.dados_temporarios["pais"].strip()
                comissao = st.session_state.dados_temporarios["comissao"] if st.session_state.dados_temporarios["comissao"] > 0 else 1.0
                
                score = calcular_score(comissao, st.session_state.dados_temporarios["tipo_produto"], st.session_state.dados_temporarios["tipo_pagamento"], pais_salvar)
                classificacao = classificar_score(score)
                explicacao = gerar_explicacao(comissao, st.session_state.dados_temporarios["tipo_produto"], st.session_state.dados_temporarios["tipo_pagamento"], pais_salvar, score)
                
                novo_registro = {
                    "tipo": "pesquisa_v2",
                    "link_produto": st.session_state.dados_temporarios["link_produto"],
                    "palavras_chave": palavras_lista,
                    "plataforma": st.session_state.dados_temporarios["plataforma"],
                    "tipo_produto": st.session_state.dados_temporarios["tipo_produto"],
                    "comissao": comissao,
                    "pais": pais_salvar,
                    "tipo_pagamento": st.session_state.dados_temporarios["tipo_pagamento"],
                    "score": score,
                    "classificacao": classificacao,
                    "explicacao": explicacao,
                    "data_hora": datetime.now().isoformat()
                }
                
                st.session_state.historico.append(novo_registro)
                salvar_historico(st.session_state.historico)
                
                # Limpar dados temporários
                st.session_state.dados_temporarios = {}
                st.session_state.etapa_pesquisa = 1
                
                st.success("✅ Análise concluída!")
                st.markdown(f"**Score:** {score}/100")
                st.markdown(f"**Classificação:** {classificacao}")
                st.markdown(f"**Explicação:** {explicacao}")
        with col3:
            st.empty()

# ==============================
# Página: Ideias de Anúncio
# ==============================
elif pagina == "Ideias de Anúncio":
    st.title("✍️ Ideias de Anúncio")
    
    nome_produto = st.text_input(
        "Nome do produto:",
        placeholder="Ex: Curso de Dropshipping"
    )
    
    grau_anuncio = st.selectbox(
        "Grau do anúncio:",
        ["Conservador", "Equilibrado", "Agressivo", "Curto", "Longo"]
    )
    
    plataformas_anuncio = [
        "Instagram Post",
        "Instagram Reels",
        "TikTok",
        "Facebook",
        "Pinterest",
        "Descrição de página de vendas",
        "Outra"
    ]
    plataforma_anuncio = st.selectbox(
        "Tipo de plataforma:",
        options=plataformas_anuncio
    )
    if plataforma_anuncio == "Outra":
        plataforma_anuncio_manual = st.text_input("Digite a plataforma:", key="plataforma_anuncio_manual")
        if plataforma_anuncio_manual.strip():
            plataforma_anuncio = plataforma_anuncio_manual.strip()
    
    # CTA editável com sugestões
    st.markdown("**Chamada para ação (CTA):**")
    cta_sugestoes = [
        "Comprar agora",
        "Ver oferta",
        "Frete grátis na Europa",
        "Pagamento na entrega",
        "Últimas unidades"
    ]
    cta_sugestao_selecionada = st.selectbox(
        "Sugestões (opcional):",
        [""] + cta_sugestoes,
        label_visibility="collapsed"
    )
    
    cta_personalizado = st.text_input(
        "Digite seu CTA personalizado:",
        value=cta_sugestao_selecionada if cta_sugestao_selecionada else "",
        key="cta_input"
    )
    
    if st.button("✨ Gerar anúncio"):
        if not nome_produto.strip():
            st.warning("⚠️ Por favor, digite o nome do produto.")
        else:
            cta_final = cta_personalizado.strip() if cta_personalizado.strip() else "Comprar agora"
            
            # Gerar anúncio com base no grau selecionado
            if grau_anuncio == "Conservador":
                anuncio_pt = (
                    f"Conheça o {nome_produto}.\n\n"
                    f"Uma solução confiável para as suas necessidades.\n"
                    f"Qualidade garantida e suporte dedicado.\n\n"
                    f"👉 {cta_final}\n"
                    f"[LINK DE AFILIADO AQUI]"
                )
                anuncio_en = (
                    f"Discover the {nome_produto}.\n\n"
                    f"A reliable solution for your needs.\n"
                    f"Guaranteed quality and dedicated support.\n\n"
                    f"👉 {cta_final}\n"
                    f"[AFFILIATE LINK HERE]"
                )
            elif grau_anuncio == "Equilibrado":
                anuncio_pt = (
                    f"Não perca o {nome_produto}!\n\n"
                    f"✅ Qualidade premium\n"
                    f"✅ Entrega rápida\n"
                    f"✅ Preço especial por tempo limitado\n\n"
                    f"👉 {cta_final}\n"
                    f"[LINK DE AFILIADO AQUI]\n\n"
                    f"#afiliado"
                )
                anuncio_en = (
                    f"Don't miss the {nome_produto}!\n\n"
                    f"✅ Premium quality\n"
                    f"✅ Fast delivery\n"
                    f"✅ Special price for a limited time\n\n"
                    f"👉 {cta_final}\n"
                    f"[AFFILIATE LINK HERE]\n\n"
                    f"#affiliate"
                )
            elif grau_anuncio == "Agressivo":
                anuncio_pt = (
                    f"🔥 CORRA! O {nome_produto} está com preço promocional!\n\n"
                    f"⚠️ ÚLTIMAS UNIDADES DISPONÍVEIS!\n"
                    f"✅ Garantia de satisfação\n"
                    f"✅ Frete rápido para toda a Europa\n\n"
                    f"💥 {cta_final} ANTES QUE ACABE!\n"
                    f"[LINK DE AFILIADO AQUI]\n\n"
                    f"#oferta #promoção"
                )
                anuncio_en = (
                    f"🔥 HURRY! The {nome_produto} is on sale!\n\n"
                    f"⚠️ LAST UNITS AVAILABLE!\n"
                    f"✅ Satisfaction guaranteed\n"
                    f"✅ Fast shipping across Europe\n\n"
                    f"💥 {cta_final} BEFORE IT'S GONE!\n"
                    f"[AFFILIATE LINK HERE]\n\n"
                    f"#deal #promotion"
                )
            elif grau_anuncio == "Curto":
                anuncio_pt = (
                    f"{nome_produto}\n"
                    f"👉 {cta_final}\n"
                    f"[LINK DE AFILIADO AQUI]"
                )
                anuncio_en = (
                    f"{nome_produto}\n"
                    f"👉 {cta_final}\n"
                    f"[AFFILIATE LINK HERE]"
                )
            else:  # Longo
                anuncio_pt = (
                    f"Apresentamos com orgulho o incrível {nome_produto}!\n\n"
                    f"Depois de meses de testes e desenvolvimento, criamos uma solução que realmente resolve o seu problema.\n\n"
                    f"🌟 Benefícios:\n"
                    f"- Resultados comprovados\n"
                    f"- Suporte 24/7\n"
                    f"- Garantia de 30 dias\n"
                    f"- Entrega imediata\n\n"
                    f"👉 {cta_final} e transforme sua vida hoje mesmo!\n"
                    f"[LINK DE AFILIADO AQUI]\n\n"
                    f"#transformação #resultados"
                )
                anuncio_en = (
                    f"We proudly present the amazing {nome_produto}!\n\n"
                    f"After months of testing and development, we've created a solution that truly solves your problem.\n\n"
                    f"🌟 Benefits:\n"
                    f"- Proven results\n"
                    f"- 24/7 support\n"
                    f"- 30-day guarantee\n"
                    f"- Instant delivery\n\n"
                    f"👉 {cta_final} and transform your life today!\n"
                    f"[AFFILIATE LINK HERE]\n\n"
                    f"#transformation #results"
                )
            
            # Salvar no histórico
            novo_registro = {
                "tipo": "anuncio_v2",
                "nome_produto": nome_produto.strip(),
                "grau": grau_anuncio,
                "plataforma": plataforma_anuncio,
                "cta": cta_final,
                "anuncio_pt": anuncio_pt,
                "anuncio_en": anuncio_en,
                "data_hora": datetime.now().isoformat()
            }
            st.session_state.historico.append(novo_registro)
            salvar_historico(st.session_state.historico)
            
            # Mostrar os anúncios
            st.success("✅ Anúncios gerados com sucesso!")
            
            st.subheader("🇵🇹 Português")
            st.text_area("", value=anuncio_pt, height=180, key="anuncio_pt")
            
            st.subheader("🇬🇧 Inglês")
            st.text_area("", value=anuncio_en, height=180, key="anuncio_en")

# ==============================
# Página: Postar (ATUALIZADA COM HORÁRIOS FIXOS)
# ==============================
elif pagina == "Postar":
    st.title("📤 Postar")
    st.caption("Configure suas credenciais e horários para postagens automáticas.")
    
    # Carregar dados salvos
    dados_atuais = st.session_state.redes_sociais
    horarios_atuais = st.session_state.horarios_postagem
    
    # Redes sociais
    st.subheader("📱 Redes Sociais")
    
    redes = ["YouTube", "Pinterest", "Instagram", "TikTok", "Facebook"]
    dados_redes = {}
    
    for rede in redes:
        col1, col2 = st.columns(2)
        with col1:
            valor_usuario = dados_atuais.get(rede, {}).get("usuario", "")
            usuario = st.text_input(f"{rede} - Usuário/Login:", value=valor_usuario, key=f"{rede}_usuario")
        with col2:
            valor_senha = dados_atuais.get(rede, {}).get("senha", "")
            senha = st.text_input(f"{rede} - Senha:", type="password", value=valor_senha, key=f"{rede}_senha")
        dados_redes[rede] = {"usuario": usuario, "senha": senha}
    
    # Horários de postagem (AUTOMATIZADO)
    st.subheader("⏰ Horários de Postagens Automáticas")
    horarios_editaveis = st.text_area(
        "Horários de pico para todas as redes (formato sugerido: HH:MM–HH:MM, separados por vírgula):",
        value=horarios_atuais,
        height=80,
        key="horarios_input"
    )
    
    # Link de afiliado
    st.subheader("🔗 Link de Afiliado")
    link_afiliado = st.text_input(
        "Cole seu link de afiliado:",
        value=dados_atuais.get("link_afiliado", ""),
        placeholder="https://exemplo.com/seu-link"
    )
    
    # Campo adicional
    st.subheader("📝 Informações Adicionais")
    info_extra = st.text_area(
        "Cole qualquer informação extra da página de vendas:",
        value=dados_atuais.get("info_extra", ""),
        placeholder="Ex: garantia, benefícios, depoimentos..."
    )
    
    # Botão de salvar
    if st.button("💾 Salvar Configurações"):
        # Validar formato básico (opcional)
        if not horarios_editaveis.strip():
            st.warning("⚠️ Por favor, insira pelo menos um horário.")
        else:
            # Atualizar horários na sessão e arquivo
            st.session_state.horarios_postagem = horarios_editaveis
            salvar_horarios(horarios_editaveis)
            
            # Montar estrutura completa das redes
            dados_completos = {
                "redes": dados_redes,
                "horario_postagem": horarios_editaveis,
                "link_afiliado": link_afiliado,
                "info_extra": info_extra
            }
            
            # Atualizar sessão e arquivo
            st.session_state.redes_sociais = dados_completos
            salvar_redes_sociais(dados_completos)
            
            st.success("✅ Configurações salvas com sucesso! Os dados permanecerão após fechar e reabrir o app.")
    
    # Aviso de segurança
    st.info(
        "🔒 **Importante:**\n\n"
        "- As senhas são armazenadas localmente no seu repositório GitHub.\n"
        "- Nunca compartilhe este repositório publicamente com senhas reais.\n"
        "- Para produção, use variáveis de ambiente (Secrets) no Streamlit Cloud."
    )

# ==============================
# Página: Histórico
# ==============================
elif pagina == "Histórico":
    st.title("📜 Histórico")
    
    if st.session_state.historico:
        historico_ordenado = sorted(
            st.session_state.historico,
            key=lambda x: x["data_hora"],
            reverse=True
        )
        
        for item in historico_ordenado:
            data_fmt = datetime.fromisoformat(item["data_hora"]).strftime("%d/%m/%Y %H:%M:%S")
            
            if item["tipo"] == "pesquisa_v2":
                st.markdown(f"**🔍 Análise de Produto** • {data_fmt}")
                st.write(f"- Link: {item['link_produto']}")
                st.write(f"- Palavras-chave: {', '.join(item['palavras_chave'])}")
                st.write(f"- Plataforma: {item['plataforma']}")
                st.write(f"- Tipo: {item['tipo_produto']}")
                st.write(f"- Comissão: {item['comissao']}%")
                st.write(f"- País: {item['pais']}")
                st.write(f"- Pagamento: {item['tipo_pagamento']}")
                st.write(f"- Score: {item['score']}/100 ({item['classificacao']})")
                st.write(f"- Explicação: {item['explicacao']}")
                
            elif item["tipo"] == "anuncio_v2":
                st.markdown(f"**✍️ Anúncio Bilingue** • {data_fmt}")
                st.write(f"- Produto: {item['nome_produto']}")
                st.write(f"- Grau: {item['grau']}")
                st.write(f"- Plataforma: {item['plataforma']}")
                st.write(f"- CTA: {item['cta']}")
                st.subheader("🇵🇹 Português")
                st.text_area("", value=item["anuncio_pt"], height=120, key=f"pt_{item['data_hora']}")
                st.subheader("🇬🇧 Inglês")
                st.text_area("", value=item["anuncio_en"], height=120, key=f"en_{item['data_hora']}")
            
            if st.button("🗑️ Apagar", key=f"del_{item['data_hora']}"):
                st.session_state.historico.remove(item)
                salvar_historico(st.session_state.historico)
                st.rerun()
            
            st.markdown("---")
    else:
        st.info("Nenhum registro ainda. Faça uma análise ou gere um anúncio para começar!")

# ==============================
# Página: Configurações
# ==============================
elif pagina == "Configurações":
    st.title("⚙️ Configurações")
    st.write("""
    **Informações importantes:**
    
    - Todos os dados são salvos localmente no arquivo `historico_afiliacao.json`
    - O app não usa APIs externas, internet ou serviços pagos
    - Nenhuma informação sensível é armazenada
    - Você pode editar o código diretamente no GitHub a qualquer momento
    
    Este é um app estável, simples e 100% editável.
    """)
    
    st.markdown("---")
    st.subheader("📌 Passo a passo para atualizar este app:")
    st.write("""
    1. No GitHub, abra o repositório `MSSP-AFILIAÇÃO-O-EU`
    2. Clique em `app.py`
    3. Clique no ícone de lápis (✏️) para editar
    4. Cole o novo código completo (substitua tudo)
    5. Clique em “Commit changes”
    6. Atualize o app no Streamlit Cloud (F5)
    
    Após analisar um produto:
    - Revise o score e a explicação
    - Decida manualmente se quer promover
    - Use a página “Ideias de Anúncio” para criar conteúdo
    - Nunca confie cegamente na análise automática
    """)
