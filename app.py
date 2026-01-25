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
        classificacao =
