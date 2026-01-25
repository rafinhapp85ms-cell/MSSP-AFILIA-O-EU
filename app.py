import streamlit as st
import json
import os
import secrets
import hashlib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta

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
DADOS_POSTAR_ARQUIVO = "dados_postar.json"
COLABORADORES_ARQUIVO = "colaboradores.json"
STATE_ARQUIVO = "state.json"
RAFAEL_HISTORICO_ARQUIVO = "rafael_historico.json"

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

def carregar_dados_postar():
    if os.path.exists(DADOS_POSTAR_ARQUIVO):
        try:
            with open(DADOS_POSTAR_ARQUIVO, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def salvar_dados_postar(dados):
    with open(DADOS_POSTAR_ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

def carregar_colaboradores():
    if os.path.exists(COLABORADORES_ARQUIVO):
        try:
            with open(COLABORADORES_ARQUIVO, "r", encoding="utf-8") as f:
                dados = json.load(f)
                for colab in dados:
                    colab["criado_em"] = datetime.fromisoformat(colab["criado_em"])
                    colab["expira_em"] = datetime.fromisoformat(colab["expira_em"])
                return dados
        except Exception:
            return []
    return []

def salvar_colaboradores(colaboradores):
    dados_para_salvar = []
    for colab in colaboradores:
        colab_copy = colab.copy()
        colab_copy["criado_em"] = colab["criado_em"].isoformat()
        colab_copy["expira_em"] = colab["expira_em"].isoformat()
        dados_para_salvar.append(colab_copy)
    
    with open(COLABORADORES_ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(dados_para_salvar, f, ensure_ascii=False, indent=2)

def carregar_estado():
    if os.path.exists(STATE_ARQUIVO):
        try:
            with open(STATE_ARQUIVO, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            estado_padrao = {
                "versao": "1.0",
                "modulos": {
                    "pesquisa_produtos": True,
                    "ideias_anuncio": True,
                    "postar": True,
                    "colaboradores": True
                },
                "tarefas_pendentes": [],
                "logs": [],
                "status_automacao": "desativada",
                "ultimo_acesso": None
            }
            salvar_estado(estado_padrao)
            st.error("❌ Caralho, o state.json sumiu! Relaxa, já recriei tudo certinho.")
            return estado_padrao
    else:
        estado_padrao = {
            "versao": "1.0",
            "modulos": {
                "pesquisa_produtos": True,
                "ideias_anuncio": True,
                "postar": True,
                "colaboradores": True
            },
            "tarefas_pendentes": [],
            "logs": [],
            "status_automacao": "desativada",
            "ultimo_acesso": None
        }
        salvar_estado(estado_padrao)
        st.warning("⚠️ Opa! state.json não existia. Já criei pra você, parceiro.")
        return estado_padrao

def salvar_estado(estado):
    with open(STATE_ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(estado, f, ensure_ascii=False, indent=2)

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

def gerar_senha_segura(tamanho=12):
    letras = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    numeros = "0123456789"
    simbolos = "!@#$%&*"
    todos = letras + numeros + simbolos
    senha = [
        secrets.choice(letras.upper()),
        secrets.choice(letras.lower()),
        secrets.choice(numeros),
        secrets.choice(simbolos)
    ]
    for _ in range(tamanho - 4):
        senha.append(secrets.choice(todos))
    secrets.SystemRandom().shuffle(senha)
    return ''.join(senha)

def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

def enviar_email_colaborador(email_destino, nome_colab, senha_gerada):
    try:
        EMAIL_USER = st.secrets["EMAIL_USER"]
        EMAIL_APP_PASSWORD = st.secrets["EMAIL_APP_PASSWORD"]
        EMAIL_FROM_NAME = st.secrets.get("EMAIL_FROM_NAME", "MSSP")
        
        msg = MIMEMultipart()
        msg["From"] = f"{EMAIL_FROM_NAME} <{EMAIL_USER}>"
        msg["To"] = email_destino
        msg["Subject"] = "Acesso à MSSP – Colaborador"
        
        corpo = f"""Olá {nome_colab},

Você foi adicionado à MSSP como colaborador por Rafael Peixoto Pires.  
Seu login é: {email_destino}  
Sua senha é: {senha_gerada}  
Validade do acesso: 15 dias.  

IMPORTANTE:  
- Seus dados e histórico serão privados.  
- Você não terá acesso aos dados ou históricos de outros colaboradores.  
- Para continuar, confirme que leu e aceita as regras de segurança no app.

Atenciosamente,  
MSSP"""
        
        msg.attach(MIMEText(corpo, "plain", "utf-8"))
        
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_APP_PASSWORD)
            server.sendmail(EMAIL_USER, email_destino, msg.as_string())
        
        return True
    except Exception as e:
        st.error(f"❌ Falha ao enviar e-mail: {str(e)}")
        return False

def analisar_produto_mssp(link="", cvr=None, epc=None, comissao=None, gravidade=None):
    link_lower = link.lower() if link else ""
    if "clickbank" in link_lower:
        plataforma = "ClickBank"
    elif "hotmart" in link_lower or "pay.hotmart" in link_lower:
        plataforma = "Hotmart"
    elif "amazon" in link_lower:
        plataforma = "Amazon"
    elif "awin" in link_lower:
        plataforma = "Awin"
    elif "cj.com" in link_lower or "commissionjunction" in link_lower:
        plataforma = "CJ Affiliate"
    else:
        plataforma = "Outra / Não identificada"
    
    criterios_aprovados = 0
    cvr_aprovado = cvr is not None and cvr >= 3
    epc_aprovado = epc is not None and epc >= 3
    comissao_aprovado = comissao is not None and comissao >= 50
    gravidade_aprovado = gravidade is not None and gravidade >= 30
    
    if cvr_aprovado: criterios_aprovados += 1
    if epc_aprovado: criterios_aprovados += 1
    if comissao_aprovado: criterios_aprovados += 1
    if gravidade_aprovado: criterios_aprovados += 1
    
    if criterios_aprovados >= 3:
        classificacao = "🟢 APROVAR"
    elif criterios_aprovados == 2:
        classificacao = "🟡 TESTAR"
    else:
        classificacao = "🔴 DESCARTAR"
    
    pontos_fortes = []
    pontos_fracos = []
    
    if cvr_aprovado:
        pontos_fortes.append("Alta taxa de conversão (≥3%)")
    else:
        pontos_fracos.append("Baixa taxa de conversão (<3%)")
    
    if epc_aprovado:
        pontos_fortes.append("Bom ganho por clique (≥$3)")
    else:
        pontos_fracos.append("Ganho por clique baixo (<$3)")
    
    if comissao_aprovado:
        pontos_fortes.append("Comissão alta (≥$50)")
    else:
        pontos_fracos.append("Comissão baixa (<$50)")
    
    if gravidade_aprovado:
        pontos_fortes.append("Alta demanda (gravidade ≥30)")
    else:
        pontos_fracos.append("Baixa demanda ou difícil de vender (gravidade <30)")
    
    if epc_aprovado and comissao_aprovado:
        trafego_indicado = "Pago (Meta Ads, Google)"
    else:
        trafego_indicado = "Orgânico (YouTube, blogs, grupos)"
    
    if plataforma in ["Hotmart", "ClickBank"]:
        redes_adequadas = ["Instagram", "TikTok", "Facebook"]
        restricoes = [
            "Meta Ads: bloqueia promessas financeiras e saúde não comprovada",
            "TikTok: restringe suplementos e relacionamentos 'milagrosos'"
        ]
    elif plataforma == "Amazon":
        redes_adequadas = ["Pinterest", "YouTube", "Facebook"]
        restricoes = [
            "Não pode usar marca 'Amazon' sem autorização",
            "Evitar falsa escassez ('Última unidade!')"
        ]
    else:
        redes_adequadas = ["Instagram", "Facebook", "YouTube"]
        restricoes = ["Ver políticas da plataforma antes de anunciar"]
    
    if classificacao == "🟢 APROVAR":
        conclusao = "Vale a pena seguir com este produto. Alto potencial de lucro com risco controlado."
    elif classificacao == "🟡 TESTAR":
        conclusao = "Teste com orçamento limitado. O produto tem potencial, mas exige validação real."
    else:
        conclusao = "Não recomendo neste momento. Risco alto e retorno incerto."
    
    return {
        "plataforma": plataforma,
        "classificacao": classificacao,
        "criterios_aprovados": criterios_aprovados,
        "pontos_fortes": pontos_fortes,
        "pontos_fracos": pontos_fracos,
        "trafego_indicado": trafego_indicado,
        "redes_adequadas": redes_adequadas,
        "restricoes": restricoes,
        "conclusao": conclusao,
        "cvr": cvr,
        "epc": epc,
        "comissao": comissao,
        "gravidade": gravidade
    }

# ==============================
# Inicializar estado da sessão
# ==============================
if "historico" not in st.session_state:
    st.session_state.historico = carregar_historico()

if "dados_postar" not in st.session_state:
    st.session_state.dados_postar = carregar_dados_postar()

if "colaboradores" not in st.session_state:
    st.session_state.colaboradores = carregar_colaboradores()

if "etapa_pesquisa" not in st.session_state:
    st.session_state.etapa_pesquisa = 1

if "dados_temporarios" not in st.session_state:
    st.session_state.dados_temporarios = {}

if "estado_mssp" not in st.session_state:
    st.session_state.estado_mssp = carregar_estado()

if "rafael_historico" not in st.session_state:
    st.session_state.rafael_historico = carregar_rafael_historico()

# ==============================
# Menu lateral
# ==============================
st.sidebar.title("MSSP Afiliado")
pagina = st.sidebar.radio(
    "Navegue pelas seções:",
    ("Início", "Pesquisa de Produtos", "Ideias de Anúncio", "Postar", "Histórico", "Colaboradores", "Rafinha", "Configurações"),
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
    
    if st.session_state.etapa_pesquisa == 1:
        st.subheader("Etapa 1/3: Link do Produto")
        link_produto = st.text_input(
            "Cole o link do produto:",
            value=st.session_state.dados_temporarios.get("link_produto", ""),
            placeholder="https://exemplo.com/produto"
        )
        
        st.markdown("### (Opcional) Métricas avançadas:")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            cvr_input = st.number_input("CVR (%)", min_value=0.0, max_value=100.0, value=0.0, step=0.1)
        with col2:
            epc_input = st.number_input("EPC ($)", min_value=0.0, value=0.0, step=0.1)
        with col3:
            comissao_input = st.number_input("Comissão ($)", min_value=0.0, value=0.0, step=1.0)
        with col4:
            gravidade_input = st.number_input("Gravidade", min_value=0, value=0, step=1)
        
        if link_produto.strip() or any([cvr_input > 0, epc_input > 0, comissao_input > 0, gravidade_input > 0]):
            cvr_val = cvr_input if cvr_input > 0 else None
            epc_val = epc_input if epc_input > 0 else None
            comissao_val = comissao_input if comissao_input > 0 else None
            gravidade_val = gravidade_input if gravidade_input > 0 else None
            
            with st.spinner("🧠 Analisando com o Motor Lógico da MSSP..."):
                resultado = analisar_produto_mssp(
                    link=link_produto.strip(),
                    cvr=cvr_val,
                    epc=epc_val,
                    comissao=comissao_val,
                    gravidade=gravidade_val
                )
            
            st.markdown("---")
            st.subheader("📊 Relatório Inteligente da MSSP")
            
            st.markdown("🔹 **Plataforma identificada:**")
            st.write(resultado["plataforma"])
            
            st.markdown("🔹 **Classificação automática:**")
            st.subheader(resultado["classificacao"])
            
            st.markdown("🔹 **Critérios analisados:**")
            st.write(f"- CVR: {resultado['cvr']}% {'✅' if resultado['cvr'] and resultado['cvr'] >= 3 else '❌'}")
            st.write(f"- EPC: ${resultado['epc']} {'✅' if resultado['epc'] and resultado['epc'] >= 3 else '❌'}")
            st.write(f"- Comissão: ${resultado['comissao']} {'✅' if resultado['comissao'] and resultado['comissao'] >= 50 else '❌'}")
            st.write(f"- Gravidade: {resultado['gravidade']} {'✅' if resultado['gravidade'] and resultado['gravidade'] >= 30 else '❌'}")
            
            if resultado["pontos_fortes"]:
                st.markdown("🔹 **Pontos fortes:**")
                for p in resultado["pontos_fortes"]:
                    st.write(f"- {p}")
            
            if resultado["pontos_fracos"]:
                st.markdown("🔹 **Pontos fracos:**")
                for p in resultado["pontos_fracos"]:
                    st.write(f"- {p}")
            
            st.markdown("🔹 **Tipo de tráfego mais indicado:**")
            st.write(resultado["trafego_indicado"])
            
            st.markdown("🔹 **Redes sociais mais adequadas:**")
            st.write(", ".join(resultado["redes_adequadas"]))
            
            st.markdown("🔹 **Possíveis restrições de anúncios:**")
            for r in resultado["restricoes"]:
                st.write(f"- {r}")
            
            st.markdown("🔹 **Conclusão final da MSSP (sua parceira de negócios):**")
            st.write(f"**{resultado['conclusao']}**")
            
            st.markdown("---")
        
        col1, col2 = st.columns([1, 5])
        with col1:
            if st.button("➡️ Avançar"):
                if link_produto.strip():
                    st.session_state.dados_temporarios["link_produto"] = link_produto.strip()
                    st.session_state.dados_temporarios.update({
                        "cvr": cvr_input if cvr_input > 0 else None,
                        "epc": epc_input if epc_input > 0 else None,
                        "comissao": comissao_input if comissao_input > 0 else None,
                        "gravidade": gravidade_input if gravidade_input > 0 else None
                    })
                    st.session_state.etapa_pesquisa = 2
                    st.rerun()
                else:
                    st.warning("⚠️ Por favor, insira o link do produto.")
        with col2:
            st.empty()

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
            value=float(st.session_state.dados_temporarios.get("comissao_percentual", 1.0)),
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
                            "comissao_percentual": comissao_input,
                            "pais": pais,
                            "tipo_pagamento": tipo_pagamento
                        })
                        st.session_state.etapa_pesquisa = 3
                        st.rerun()
        with col3:
            st.empty()

    elif st.session_state.etapa_pesquisa == 3:
        st.subheader("Etapa 3/3: Confirmar e Analisar")
        
        st.markdown("**Link do produto:**")
        st.code(st.session_state.dados_temporarios["link_produto"])
        
        st.markdown("**Detalhes:**")
        st.write(f"- Palavras-chave: {st.session_state.dados_temporarios['palavras_chave_input']}")
        st.write(f"- Plataforma: {st.session_state.dados_temporarios['plataforma']}")
        st.write(f"- Tipo: {st.session_state.dados_temporarios['tipo_produto']}")
        st.write(f"- Comissão: {st.session_state.dados_temporarios['comissao_percentual']}%")
        st.write(f"- País: {st.session_state.dados_temporarios['pais']}")
        st.write(f"- Pagamento: {st.session_state.dados_temporarios['tipo_pagamento']}")
        
        col1, col2, col3 = st.columns([1, 1, 4])
        with col1:
            if st.button("⬅️ Voltar"):
                st.session_state.etapa_pesquisa = 2
                st.rerun()
        with col2:
            if st.button("✅ Analisar Produto"):
                palavras_lista = [p.strip() for p in st.session_state.dados_temporarios["palavras_chave_input"].split(",") if p.strip()]
                pais_salvar = "Europa (todos os países)" if st.session_state.dados_temporarios["pais"].strip().lower() == "europa" else st.session_state.dados_temporarios["pais"].strip()
                comissao = st.session_state.dados_temporarios["comissao_percentual"] if st.session_state.dados_temporarios["comissao_percentual"] > 0 else 1.0
                
                novo_registro = {
                    "tipo": "pesquisa_v2",
                    "link_produto": st.session_state.dados_temporarios["link_produto"],
                    "palavras_chave": palavras_lista,
                    "plataforma": st.session_state.dados_temporarios["plataforma"],
                    "tipo_produto": st.session_state.dados_temporarios["tipo_produto"],
                    "comissao": comissao,
                    "pais": pais_salvar,
                    "tipo_pagamento": st.session_state.dados_temporarios["tipo_pagamento"],
                    "cvr": st.session_state.dados_temporarios.get("cvr"),
                    "epc": st.session_state.dados_temporarios.get("epc"),
                    "comissao_valor": st.session_state.dados_temporarios.get("comissao"),
                    "gravidade": st.session_state.dados_temporarios.get("gravidade"),
                    "data_hora": datetime.now().isoformat()
                }
                
                st.session_state.historico.append(novo_registro)
                salvar_historico(st.session_state.historico)
                
                st.session_state.dados_temporarios = {}
                st.session_state.etapa_pesquisa = 1
                
                st.success("✅ Análise concluída!")
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
                    f"# affiliate"
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
            else:
                anuncio_pt = (
                    f"Apresentamos com orgulho o incrível {nome_produto}!\n\n"
                    f"Depois de meses de testes e desenvolvimento, criamos uma solução que realmente resolve o seu problema.\n\n"
                    f"🌟 Benefícios:\n"
                    f"- Resultados comprovados\n"
                    f"- Suporte 24/7\n"
                    f"- Garantia de 30 dias\n"
                    f"- Entrega imediata\n\n"
                    f"👉 {cta_final} e transforme sua vida hoje mesmo!\n"
                    f"[LINK DE✅ **Código atualizado com a caixa de mensagens fixa do Rafinha — exatamente conforme suas regras.**

---

### 📦 **Substitua TODO o conteúdo do `app.py` por este código:**

```python
import streamlit as st
import json
import os
import secrets
import hashlib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta

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
DADOS_POSTAR_ARQUIVO = "dados_postar.json"
COLABORADORES_ARQUIVO = "colaboradores.json"
STATE_ARQUIVO = "state.json"
RAFAEL_HISTORICO_ARQUIVO = "rafael_historico.json"

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

def carregar_dados_postar():
    if os.path.exists(DADOS_POSTAR_ARQUIVO):
        try:
            with open(DADOS_POSTAR_ARQUIVO, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def salvar_dados_postar(dados):
    with open(DADOS_POSTAR_ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

def carregar_colaboradores():
    if os.path.exists(COLABORADORES_ARQUIVO):
        try:
            with open(COLABORADORES_ARQUIVO, "r", encoding="utf-8") as f:
                dados = json.load(f)
                for colab in dados:
                    colab["criado_em"] = datetime.fromisoformat(colab["criado_em"])
                    colab["expira_em"] = datetime.fromisoformat(colab["expira_em"])
                return dados
        except Exception:
            return []
    return []

def salvar_colaboradores(colaboradores):
    dados_para_salvar = []
    for colab in colaboradores:
        colab_copy = colab.copy()
        colab_copy["criado_em"] = colab["criado_em"].isoformat()
        colab_copy["expira_em"] = colab["expira_em"].isoformat()
        dados_para_salvar.append(colab_copy)
    
    with open(COLABORADORES_ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(dados_para_salvar, f, ensure_ascii=False, indent=2)

def carregar_estado():
    if os.path.exists(STATE_ARQUIVO):
        try:
            with open(STATE_ARQUIVO, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            estado_padrao = {
                "versao": "1.0",
                "modulos": {
                    "pesquisa_produtos": True,
                    "ideias_anuncio": True,
                    "postar": True,
                    "colaboradores": True
                },
                "tarefas_pendentes": [],
                "logs": [],
                "status_automacao": "desativada",
                "ultimo_acesso": None
            }
            salvar_estado(estado_padrao)
            st.error("❌ Caralho, o state.json sumiu! Relaxa, já recriei tudo certinho.")
            return estado_padrao
    else:
        estado_padrao = {
            "versao": "1.0",
            "modulos": {
                "pesquisa_produtos": True,
                "ideias_anuncio": True,
                "postar": True,
                "colaboradores": True
            },
            "tarefas_pendentes": [],
            "logs": [],
            "status_automacao": "desativada",
            "ultimo_acesso": None
        }
        salvar_estado(estado_padrao)
        st.warning("⚠️ Opa! state.json não existia. Já criei pra você, parceiro.")
        return estado_padrao

def salvar_estado(estado):
    with open(STATE_ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(estado, f, ensure_ascii=False, indent=2)

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

def gerar_senha_segura(tamanho=12):
    letras = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    numeros = "0123456789"
    simbolos = "!@#$%&*"
    todos = letras + numeros + simbolos
    senha = [
        secrets.choice(letras.upper()),
        secrets.choice(letras.lower()),
        secrets.choice(numeros),
        secrets.choice(simbolos)
    ]
    for _ in range(tamanho - 4):
        senha.append(secrets.choice(todos))
    secrets.SystemRandom().shuffle(senha)
    return ''.join(senha)

def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

def enviar_email_colaborador(email_destino, nome_colab, senha_gerada):
    try:
        EMAIL_USER = st.secrets["EMAIL_USER"]
        EMAIL_APP_PASSWORD = st.secrets["EMAIL_APP_PASSWORD"]
        EMAIL_FROM_NAME = st.secrets.get("EMAIL_FROM_NAME", "MSSP")
        
        msg = MIMEMultipart()
        msg["From"] = f"{EMAIL_FROM_NAME} <{EMAIL_USER}>"
        msg["To"] = email_destino
        msg["Subject"] = "Acesso à MSSP – Colaborador"
        
        corpo = f"""Olá {nome_colab},

Você foi adicionado à MSSP como colaborador por Rafael Peixoto Pires.  
Seu login é: {email_destino}  
Sua senha é: {senha_gerada}  
Validade do acesso: 15 dias.  

IMPORTANTE:  
- Seus dados e histórico serão privados.  
- Você não terá acesso aos dados ou históricos de outros colaboradores.  
- Para continuar, confirme que leu e aceita as regras de segurança no app.

Atenciosamente,  
MSSP"""
        
        msg.attach(MIMEText(corpo, "plain", "utf-8"))
        
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_APP_PASSWORD)
            server.sendmail(EMAIL_USER, email_destino, msg.as_string())
        
        return True
    except Exception as e:
        st.error(f"❌ Falha ao enviar e-mail: {str(e)}")
        return False

def analisar_produto_mssp(link="", cvr=None, epc=None, comissao=None, gravidade=None):
    link_lower = link.lower() if link else ""
    if "clickbank" in link_lower:
        plataforma = "ClickBank"
    elif "hotmart" in link_lower or "pay.hotmart" in link_lower:
        plataforma = "Hotmart"
    elif "amazon" in link_lower:
        plataforma = "Amazon"
    elif "awin" in link_lower:
        plataforma = "Awin"
    elif "cj.com" in link_lower or "commissionjunction" in link_lower:
        plataforma = "CJ Affiliate"
    else:
        plataforma = "Outra / Não identificada"
    
    criterios_aprovados = 0
    cvr_aprovado = cvr is not None and cvr >= 3
    epc_aprovado = epc is not None and epc >= 3
    comissao_aprovado = comissao is not None and comissao >= 50
    gravidade_aprovado = gravidade is not None and gravidade >= 30
    
    if cvr_aprovado: criterios_aprovados += 1
    if epc_aprovado: criterios_aprovados += 1
    if comissao_aprovado: criterios_aprovados += 1
    if gravidade_aprovado: criterios_aprovados += 1
    
    if criterios_aprovados >= 3:
        classificacao = "🟢 APROVAR"
    elif criterios_aprovados == 2:
        classificacao = "🟡 TESTAR"
    else:
        classificacao = "🔴 DESCARTAR"
    
    pontos_fortes = []
    pontos_fracos = []
    
    if cvr_aprovado:
        pontos_fortes.append("Alta taxa de conversão (≥3%)")
    else:
        pontos_fracos.append("Baixa taxa de conversão (<3%)")
    
    if epc_aprovado:
        pontos_fortes.append("Bom ganho por clique (≥$3)")
    else:
        pontos_fracos.append("Ganho por clique baixo (<$3)")
    
    if comissao_aprovado:
        pontos_fortes.append("Comissão alta (≥$50)")
    else:
        pontos_fracos.append("Comissão baixa (<$50)")
    
    if gravidade_aprovado:
        pontos_fortes.append("Alta demanda (gravidade ≥30)")
    else:
        pontos_fracos.append("Baixa demanda ou difícil de vender (gravidade <30)")
    
    if epc_aprovado and comissao_aprovado:
        trafego_indicado = "Pago (Meta Ads, Google)"
    else:
        trafego_indicado = "Orgânico (YouTube, blogs, grupos)"
    
    if plataforma in ["Hotmart", "ClickBank"]:
        redes_adequadas = ["Instagram", "TikTok", "Facebook"]
        restricoes = [
            "Meta Ads: bloqueia promessas financeiras e saúde não comprovada",
            "TikTok: restringe suplementos e relacionamentos 'milagrosos'"
        ]
    elif plataforma == "Amazon":
        redes_adequadas = ["Pinterest", "YouTube", "Facebook"]
        restricoes = [
            "Não pode usar marca 'Amazon' sem autorização",
            "Evitar falsa escassez ('Última unidade!')"
        ]
    else:
        redes_adequadas = ["Instagram", "Facebook", "YouTube"]
        restricoes = ["Ver políticas da plataforma antes de anunciar"]
    
    if classificacao == "🟢 APROVAR":
        conclusao = "Vale a pena seguir com este produto. Alto potencial de lucro com risco controlado."
    elif classificacao == "🟡 TESTAR":
        conclusao = "Teste com orçamento limitado. O produto tem potencial, mas exige validação real."
    else:
        conclusao = "Não recomendo neste momento. Risco alto e retorno incerto."
    
    return {
        "plataforma": plataforma,
        "classificacao": classificacao,
        "criterios_aprovados": criterios_aprovados,
        "pontos_fortes": pontos_fortes,
        "pontos_fracos": pontos_fracos,
        "trafego_indicado": trafego_indicado,
        "redes_adequadas": redes_adequadas,
        "restricoes": restricoes,
        "conclusao": conclusao,
        "cvr": cvr,
        "epc": epc,
        "comissao": comissao,
        "gravidade": gravidade
    }

# ==============================
# Inicializar estado da sessão
# ==============================
if "historico" not in st.session_state:
    st.session_state.historico = carregar_historico()

if "dados_postar" not in st.session_state:
    st.session_state.dados_postar = carregar_dados_postar()

if "colaboradores" not in st.session_state:
    st.session_state.colaboradores = carregar_colaboradores()

if "etapa_pesquisa" not in st.session_state:
    st.session_state.etapa_pesquisa = 1

if "dados_temporarios" not in st.session_state:
    st.session_state.dados_temporarios = {}

if "estado_mssp" not in st.session_state:
    st.session_state.estado_mssp = carregar_estado()

if "rafael_historico" not in st.session_state:
    st.session_state.rafael_historico = carregar_rafael_historico()

# ==============================
# Menu lateral
# ==============================
st.sidebar.title("MSSP Afiliado")
pagina = st.sidebar.radio(
    "Navegue pelas seções:",
    ("Início", "Pesquisa de Produtos", "Ideias de Anúncio", "Postar", "Histórico", "Colaboradores", "Rafinha", "Configurações"),
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
    
    if st.session_state.etapa_pesquisa == 1:
        st.subheader("Etapa 1/3: Link do Produto")
        link_produto = st.text_input(
            "Cole o link do produto:",
            value=st.session_state.dados_temporarios.get("link_produto", ""),
            placeholder="https://exemplo.com/produto"
        )
        
        st.markdown("### (Opcional) Métricas avançadas:")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            cvr_input = st.number_input("CVR (%)", min_value=0.0, max_value=100.0, value=0.0, step=0.1)
        with col2:
            epc_input = st.number_input("EPC ($)", min_value=0.0, value=0.0, step=0.1)
        with col3:
            comissao_input = st.number_input("Comissão ($)", min_value=0.0, value=0.0, step=1.0)
        with col4:
            gravidade_input = st.number_input("Gravidade", min_value=0, value=0, step=1)
        
        if link_produto.strip() or any([cvr_input > 0, epc_input > 0, comissao_input > 0, gravidade_input > 0]):
            cvr_val = cvr_input if cvr_input > 0 else None
            epc_val = epc_input if epc_input > 0 else None
            comissao_val = comissao_input if comissao_input > 0 else None
            gravidade_val = gravidade_input if gravidade_input > 0 else None
            
            with st.spinner("🧠 Analisando com o Motor Lógico da MSSP..."):
                resultado = analisar_produto_mssp(
                    link=link_produto.strip(),
                    cvr=cvr_val,
                    epc=epc_val,
                    comissao=comissao_val,
                    gravidade=gravidade_val
                )
            
            st.markdown("---")
            st.subheader("📊 Relatório Inteligente da MSSP")
            
            st.markdown("🔹 **Plataforma identificada:**")
            st.write(resultado["plataforma"])
            
            st.markdown("🔹 **Classificação automática:**")
            st.subheader(resultado["classificacao"])
            
            st.markdown("🔹 **Critérios analisados:**")
            st.write(f"- CVR: {resultado['cvr']}% {'✅' if resultado['cvr'] and resultado['cvr'] >= 3 else '❌'}")
            st.write(f"- EPC: ${resultado['epc']} {'✅' if resultado['epc'] and resultado['epc'] >= 3 else '❌'}")
            st.write(f"- Comissão: ${resultado['comissao']} {'✅' if resultado['comissao'] and resultado['comissao'] >= 50 else '❌'}")
            st.write(f"- Gravidade: {resultado['gravidade']} {'✅' if resultado['gravidade'] and resultado['gravidade'] >= 30 else '❌'}")
            
            if resultado["pontos_fortes"]:
                st.markdown("🔹 **Pontos fortes:**")
                for p in resultado["pontos_fortes"]:
                    st.write(f"- {p}")
            
            if resultado["pontos_fracos"]:
                st.markdown("🔹 **Pontos fracos:**")
                for p in resultado["pontos_fracos"]:
                    st.write(f"- {p}")
            
            st.markdown("🔹 **Tipo de tráfego mais indicado:**")
            st.write(resultado["trafego_indicado"])
            
            st.markdown("🔹 **Redes sociais mais adequadas:**")
            st.write(", ".join(resultado["redes_adequadas"]))
            
            st.markdown("🔹 **Possíveis restrições de anúncios:**")
            for r in resultado["restricoes"]:
                st.write(f"- {r}")
            
            st.markdown("🔹 **Conclusão final da MSSP (sua parceira de negócios):**")
            st.write(f"**{resultado['conclusao']}**")
            
            st.markdown("---")
        
        col1, col2 = st.columns([1, 5])
        with col1:
            if st.button("➡️ Avançar"):
                if link_produto.strip():
                    st.session_state.dados_temporarios["link_produto"] = link_produto.strip()
                    st.session_state.dados_temporarios.update({
                        "cvr": cvr_input if cvr_input > 0 else None,
                        "epc": epc_input if epc_input > 0 else None,
                        "comissao": comissao_input if comissao_input > 0 else None,
                        "gravidade": gravidade_input if gravidade_input > 0 else None
                    })
                    st.session_state.etapa_pesquisa = 2
                    st.rerun()
                else:
                    st.warning("⚠️ Por favor, insira o link do produto.")
        with col2:
            st.empty()

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
            value=float(st.session_state.dados_temporarios.get("comissao_percentual", 1.0)),
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
                            "comissao_percentual": comissao_input,
                            "pais": pais,
                            "tipo_pagamento": tipo_pagamento
                        })
                        st.session_state.etapa_pesquisa = 3
                        st.rerun()
        with col3:
            st.empty()

    elif st.session_state.etapa_pesquisa == 3:
        st.subheader("Etapa 3/3: Confirmar e Analisar")
        
        st.markdown("**Link do produto:**")
        st.code(st.session_state.dados_temporarios["link_produto"])
        
        st.markdown("**Detalhes:**")
        st.write(f"- Palavras-chave: {st.session_state.dados_temporarios['palavras_chave_input']}")
        st.write(f"- Plataforma: {st.session_state.dados_temporarios['plataforma']}")
        st.write(f"- Tipo: {st.session_state.dados_temporarios['tipo_produto']}")
        st.write(f"- Comissão: {st.session_state.dados_temporarios['comissao_percentual']}%")
        st.write(f"- País: {st.session_state.dados_temporarios['pais']}")
        st.write(f"- Pagamento: {st.session_state.dados_temporarios['tipo_pagamento']}")
        
        col1, col2, col3 = st.columns([1, 1, 4])
        with col1:
            if st.button("⬅️ Voltar"):
                st.session_state.etapa_pesquisa = 2
                st.rerun()
        with col2:
            if st.button("✅ Analisar Produto"):
                palavras_lista = [p.strip() for p in st.session_state.dados_temporarios["palavras_chave_input"].split(",") if p.strip()]
                pais_salvar = "Europa (todos os países)" if st.session_state.dados_temporarios["pais"].strip().lower() == "europa" else st.session_state.dados_temporarios["pais"].strip()
                comissao = st.session_state.dados_temporarios["comissao_percentual"] if st.session_state.dados_temporarios["comissao_percentual"] > 0 else 1.0
                
                novo_registro = {
                    "tipo": "pesquisa_v2",
                    "link_produto": st.session_state.dados_temporarios["link_produto"],
                    "palavras_chave": palavras_lista,
                    "plataforma": st.session_state.dados_temporarios["plataforma"],
                    "tipo_produto": st.session_state.dados_temporarios["tipo_produto"],
                    "comissao": comissao,
                    "pais": pais_salvar,
                    "tipo_pagamento": st.session_state.dados_temporarios["tipo_pagamento"],
                    "cvr": st.session_state.dados_temporarios.get("cvr"),
                    "epc": st.session_state.dados_temporarios.get("epc"),
                    "comissao_valor": st.session_state.dados_temporarios.get("comissao"),
                    "gravidade": st.session_state.dados_temporarios.get("gravidade"),
                    "data_hora": datetime.now().isoformat()
                }
                
                st.session_state.historico.append(novo_registro)
                salvar_historico(st.session_state.historico)
                
                st.session_state.dados_temporarios = {}
                st.session_state.etapa_pesquisa = 1
                
                st.success("✅ Análise concluída!")
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
                    f"# affiliate"
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
            else:
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
            
            st.success("✅ Anúncios gerados com sucesso!")
            
            st.subheader("🇵🇹 Português")
            st.text_area("", value=anuncio_pt, height=180, key="anuncio_pt")
            
            st.subheader("🇬🇧 Inglês")
            st.text_area("", value=anuncio_en, height=180, key="anuncio_en")

# ==============================
# Página: Postar
# ==============================
elif pagina == "Postar":
    st.title("📤 Postar")
    st.caption("Configure suas credenciais e horários para postagens automáticas.")
    
    dados = st.session_state.dados_postar
    
    st.subheader("📱 Redes Sociais")
    
    redes = ["YouTube", "Pinterest", "Instagram", "TikTok", "Facebook"]
    dados_atualizados = {}
    
    for rede in redes:
        col1, col2 = st.columns(2)
        with col1:
            valor_usuario = dados.get(rede, {}).get("usuario", "")
            usuario = st.text_input(f"{rede} - Usuário/Login:", value=valor_usuario, key=f"{rede}_usuario")
        with col2:
            valor_senha = dados.get(rede, {}).get("senha", "")
            senha = st.text_input(f"{rede} - Senha:", type="password", value=valor_senha, key=f"{rede}_senha")
        dados_atualizados[rede] = {"usuario": usuario, "senha": senha}
    
    st.subheader("⏰ Horários de Postagens Automáticas")
    horarios_padrao = dados.get("horarios_postagem", "07:00–09:00, 12:00–14:00, 18:00–21:00")
    horarios = st.text_area(
        "Horários de pico para todas as redes (formato sugerido: HH:MM–HH:MM, separados por vírgula):",
        value=horarios_padrao,
        height=80,
        key="horarios_input"
    )
    dados_atualizados["horarios_postagem"] = horarios
    
    st.subheader("🔗 Link de Afiliado")
    link_afiliado_padrao = dados.get("link_afiliado", "")
    link_afiliado = st.text_input(
        "Cole seu link de afiliado:",
        value=link_afiliado_padrao,
        placeholder="https://exemplo.com/seu-link"
    )
    dados_atualizados["link_afiliado"] = link_afiliado
    
    st.subheader("📝 Informações Adicionais")
    info_extra_padrao = dados.get("info_extra", "")
    info_extra = st.text_area(
        "Cole qualquer informação extra da página de vendas:",
        value=info_extra_padrao,
        placeholder="Ex: garantia, benefícios, depoimentos..."
    )
    dados_atualizados["info_extra"] = info_extra
    
    if st.button("💾 Salvar Configurações"):
        st.session_state.dados_postar = dados_atualizados
        salvar_dados_postar(dados_atualizados)
        st.success("✅ Todas as configurações foram salvas com sucesso! Os dados permanecerão após fechar e reabrir o app.")
    
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
                link_produto = item.get("link_produto", "Não informado")
                st.write(f"- Link: {link_produto}")
                if item.get("cvr"):
                    st.write(f"- CVR: {item['cvr']}%")
                if item.get("epc"):
                    st.write(f"- EPC: ${item['epc']}")
                if item.get("comissao_valor"):
                    st.write(f"- Comissão: ${item['comissao_valor']}")
                if item.get("gravidade"):
                    st.write(f"- Gravidade: {item['gravidade']}")
                st.write(f"- Palavras-chave: {', '.join(item.get('palavras_chave', []))}")
                st.write(f"- Plataforma: {item.get('plataforma', 'Não identificada')}")
                st.write(f"- Tipo: {item.get('tipo_produto', 'Não identificado')}")
                st.write(f"- Comissão (%): {item.get('comissao', 0)}%")
                st.write(f"- País: {item.get('pais', 'Não informado')}")
                st.write(f"- Pagamento: {item.get('tipo_pagamento', 'Não informado')}")
                
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
# Página: Colaboradores
# ==============================
elif pagina == "Colaboradores":
    st.title("👥 Colaboradores")
    st.caption("Adicione colaboradores com acesso seguro e isolado por 15 dias.")

    if "colaboradores" not in st.session_state:
        st.session_state.colaboradores = []

    def extrair_nome(email):
        nome = email.split("@")[0]
        return nome.replace(".", " ").replace("_", " ").title()

    with st.form("form_colaborador"):
        email = st.text_input("E-mail do colaborador")
        submitted = st.form_submit_button("Adicionar colaborador")

        if submitted and email:
            if "@" not in email or "." not in email:
                st.warning("⚠️ Formato de e-mail inválido.")
            else:
                existe = any(colab["email"] == email for colab in st.session_state.colaboradores)
                if existe:
                    st.warning("⚠️ Este e-mail já está cadastrado.")
                else:
                    senha_gerada = gerar_senha_segura()
                    senha_hash = hash_senha(senha_gerada)
                    nome_colab = extrair_nome(email)

                    colaborador = {
                        "email": email,
                        "nome": nome_colab,
                        "senha_hash": senha_hash,
                        "criado_em": datetime.now(),
                        "expira_em": datetime.now() + timedelta(days=15),
                        "ativo": True,
                        "confirmado": False
                    }

                    if enviar_email_colaborador(email, nome_colab, senha_gerada):
                        st.success("✅ Colaborador adicionado e e-mail enviado com sucesso!")
                    else:
                        st.warning("⚠️ Colaborador adicionado, mas falha ao enviar e-mail. Verifique as credenciais no Secrets.")
                    
                    st.session_state.colaboradores.append(colaborador)
                    salvar_colaboradores(st.session_state.colaboradores)
                    st.rerun()

    st.subheader("📋 Colaboradores cadastrados")

    if st.session_state.colaboradores:
        for idx, colab in enumerate(st.session_state.colaboradores):
            if not colab["ativo"]:
                continue
                
            dias_restantes = (colab["expira_em"] - datetime.now()).days
            status = "Aguardando confirmação" if not colab.get("confirmado", False) else "Ativo"

            st.markdown(f"""
            **E-mail:** {colab['email']}  
            **Status:** {status}  
            **Dias restantes:** {max(dias_restantes, 0)}
            """)

            if dias_restantes <= 0 or not colab.get("confirmado", False):
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"🔄 Renovar – {colab['email']}", key=f"renovar_{idx}"):
                        colab["expira_em"] = datetime.now() + timedelta(days=15)
                        colab["confirmado"] = True
                        salvar_colaboradores(st.session_state.colaboradores)
                        st.success("✅ Acesso renovado e ativado.")
                        st.rerun()
                with col2:
                    if st.button(f"❌ Remover – {colab['email']}", key=f"remover_{idx}"):
                        colab["ativo"] = False
                        salvar_colaboradores(st.session_state.colaboradores)
                        st.warning("⚠️ Acesso removido.")
                        st.rerun()
            
            st.divider()
    else:
        st.info("Nenhum colaborador cadastrado ainda.")

# ==============================
# Página: Rafinha (CAIXA FIXA NO TOPO CENTRAL)
# ==============================
elif pagina == "Rafinha":
    st.title("🧠 Rafinha — Cérebro Interno da MSSP")
    st.caption("Sou seu parceiro, guardião e resolvedor. Falo direto, aprendo rápido e protejo a MSSP.")

    # === ESTILO CSS PARA CAIXA FIXA ===
    st.markdown(
        """
        <style>
        .fixed-chat-container {
            position: relative;
            background-color: #ffffff;
            border: 1px solid #e0e0e0;
            border-radius: 12px;
            padding: 20px;
           
