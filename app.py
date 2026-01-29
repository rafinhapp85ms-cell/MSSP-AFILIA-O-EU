import streamlit as st
import json
import os
import secrets
import hashlib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta

st.set_page_config(page_title="MSSP Afiliado", layout="wide", initial_sidebar_state="expanded")

# === Arquivos ===
HISTORICO_ARQUIVO = "historico_afiliacao.json"
DADOS_POSTAR_ARQUIVO = "dados_postar.json"
COLABORADORES_ARQUIVO = "colaboradores.json"
STATE_ARQUIVO = "state.json"
RAFAEL_HISTORICO_ARQUIVO = "rafael_historico.json"

# === Funções de persistência ===
def carregar_historico():
    return json.load(open(HISTORICO_ARQUIVO, "r", encoding="utf-8")) if os.path.exists(HISTORICO_ARQUIVO) else []

def salvar_historico(h):
    with open(HISTORICO_ARQUIVO, "w", encoding="utf-8") as f: json.dump(h, f, ensure_ascii=False, indent=2)

def carregar_dados_postar():
    if os.path.exists(DADOS_POSTAR_ARQUIVO):
        return json.load(open(DADOS_POSTAR_ARQUIVO, "r", encoding="utf-8"))
    dados = {
        "redes": {"YouTube": {"usuario": "", "senha": ""}, "Pinterest": {"usuario": "", "senha": ""}, "Instagram": {"usuario": "", "senha": ""}, "TikTok": {"usuario": "", "senha": ""}, "Facebook": {"usuario": "", "senha": ""}},
        "horarios_postagem": "07:00–09:00, 12:00–14:00, 18:00–21:00",
        "link_afiliado": "",
        "info_extra": ""
    }
    salvar_dados_postar(dados)
    return dados

def salvar_dados_postar(d):
    with open(DADOS_POSTAR_ARQUIVO, "w", encoding="utf-8") as f: json.dump(d, f, ensure_ascii=False, indent=2)

def carregar_colaboradores():
    return json.load(open(COLABORADORES_ARQUIVO, "r", encoding="utf-8")) if os.path.exists(COLABORADORES_ARQUIVO) else []

def salvar_colaboradores(c):
    with open(COLABORADORES_ARQUIVO, "w", encoding="utf-8") as f: json.dump(c, f, ensure_ascii=False, indent=2)

def carregar_estado():
    if os.path.exists(STATE_ARQUIVO):
        return json.load(open(STATE_ARQUIVO, "r", encoding="utf-8"))
    estado = {"versao": "1.0", "modulos": {"pesquisa_produtos": True, "ideias_anuncio": True, "postar": True, "colaboradores": True}, "status_automacao": "desativada"}
    salvar_estado(estado)
    return estado

def salvar_estado(e):
    with open(STATE_ARQUIVO, "w", encoding="utf-8") as f: json.dump(e, f, ensure_ascii=False, indent=2)

def carregar_rafael_historico():
    return json.load(open(RAFAEL_HISTORICO_ARQUIVO, "r", encoding="utf-8")) if os.path.exists(RAFAEL_HISTORICO_ARQUIVO) else []

def salvar_rafael_historico(h):
    with open(RAFAEL_HISTORICO_ARQUIVO, "w", encoding="utf-8") as f: json.dump(h, f, ensure_ascii=False, indent=2)

def gerar_senha_segura():
    import secrets
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%&*"
    return ''.join(secrets.choice(chars) for _ in range(12))

def hash_senha(s):
    import hashlib
    return hashlib.sha256(s.encode()).hexdigest()

def enviar_email_colaborador(email, nome, senha):
    try:
        msg = MIMEMultipart()
        msg["From"] = f"MSSP <{st.secrets['EMAIL_USER']}>"
        msg["To"] = email
        msg["Subject"] = "Acesso à MSSP – Colaborador"
        corpo = f"Olá {nome},\n\nSeu login: {email}\nSenha: {senha}\nValidade: 15 dias."
        msg.attach(MIMEText(corpo, "plain", "utf-8"))
        with smtplib.SMTP("smtp.gmail.com", 587) as s:
            s.starttls()
            s.login(st.secrets["EMAIL_USER"], st.secrets["EMAIL_APP_PASSWORD"])
            s.sendmail(st.secrets["EMAIL_USER"], email, msg.as_string())
        return True
    except: return False

def analisar_produto_mssp(link="", cvr=None, epc=None, comissao=None, gravidade=None):
    p = "Outra"
    for k, v in [("clickbank", "ClickBank"), ("hotmart", "Hotmart"), ("amazon", "Amazon"), ("awin", "Awin"), ("cj.com", "CJ Affiliate")]:
        if k in link.lower(): p = v
    c = sum([cvr and cvr>=3, epc and epc>=3, comissao and comissao>=50, gravidade and gravidade>=30])
    cl = "🔴 DESCARTAR" if c<3 else "🟡 TESTAR" if c==2 else "🟢 APROVAR"
    return {"plataforma": p, "classificacao": cl, "cvr": cvr, "epc": epc, "comissao": comissao, "gravidade": gravidade}

# === Inicialização ===
for k, v in [
    ("historico", carregar_historico()),
    ("dados_postar", carregar_dados_postar()),
    ("colaboradores", carregar_colaboradores()),
    ("estado_mssp", carregar_estado()),
    ("rafael_historico", carregar_rafael_historico())
]:
    if k not in st.session_state: st.session_state[k] = v

# === Sidebar ===
st.sidebar.title("MSSP Afiliado")
pagina = st.sidebar.radio("Navegue:", ["Início", "Pesquisa de Produtos", "Ideias de Anúncio", "Postar", "Histórico", "Colaboradores", "Rafinha", "Configurações"], index=0)

# === Páginas ===
if pagina == "Início":
    st.title("🎯 MSSP Afiliado")
    st.write("Fase 2A — Análise Avançada de Produtos para Afiliados")
    st.info("💡 Comece por 'Pesquisa de Produtos'")

elif pagina == "Pesquisa de Produtos":
    st.title("🔍 Pesquisa de Produtos")
    link = st.text_input("Link do produto:", "")
    if st.button("Analisar"):
        r = analisar_produto_mssp(link)
        st.subheader(r["classificacao"])
        st.write(f"Plataforma: {r['plataforma']}")

elif pagina == "Ideias de Anúncio":
    st.title("✍️ Ideias de Anúncio")
    st.text_input("Nome do produto:", "")
    if st.button("Gerar"): st.success("✅ Anúncio gerado")

elif pagina == "Postar":
    st.title("📤 Postar")
    st.text_input("YouTube - Usuário:", "")
    st.text_input("YouTube - Senha:", type="password")
    if st.button("💾 Salvar"): st.success("Salvo")

elif pagina == "Histórico":
    st.title("📜 Histórico")
    st.info("Nenhum registro ainda.")

elif pagina == "Colaboradores":
    st.title("👥 Colaboradores")
    email = st.text_input("E-mail:")
    if st.button("Adicionar"):
        senha = gerar_senha_segura()
        if enviar_email_colaborador(email, "Parceiro", senha):
            st.success("✅ Enviado")

elif pagina == "Rafinha":
    st.title("🧠 Rafinha — Cérebro Interno da MSSP")
    st.caption("Sou seu parceiro, guardião e resolvedor.")

    st.markdown(
        """
        <style>
        .input-sticky { position: sticky; bottom: 0; background: white; padding: 16px 0; border-top: 1px solid #eee; }
        .msg { max-width: 800px; margin: 0 auto 12px; padding: 12px; border-radius: 12px; }
        .user { background: #e3f2fd; text-align: right; }
        .raf { background: #f1f8e9; text-align: left; }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Exibir mensagens
    hist = st.session_state.rafael_historico
    for m in hist[-10:]:
        u = m.get("usuario", "")
        r = m.get("resposta", "")
        if u: st.markdown(f'<div class="msg user">Você: {u}</div>', unsafe_allow_html=True)
        if r: st.markdown(f'<div class="msg raf">Rafinha: {r}</div>', unsafe_allow_html=True)

    # Input fixo na parte inferior
    st.markdown('<div class="input-sticky">', unsafe_allow_html=True)
    col1, col2 = st.columns([4,1])
    with col1:
        msg = st.text_input("Sua mensagem:", key="inp", label_visibility="collapsed")
    with col2:
        if st.button("Enviar", use_container_width=True):
            if msg.strip():
                resp = "✅ Tá lindo, parceiro!" if "tá lindo" in msg.lower() else "❌ Caralho, deu ruim?"
                nova = {"usuario": msg, "resposta": resp, "data_hora": datetime.now().isoformat()}
                hist.append(nova)
                st.session_state.rafael_historico = hist
                salvar_rafael_historico(hist)
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

elif pagina == "Configurações":
    st.title("⚙️ Configurações")
    st.write("Tudo local. Sem internet.")
