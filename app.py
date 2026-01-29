import streamlit as st
import json
import os
import datetime

# === Configuração básica ===
st.set_page_config(page_title="MSSP Afiliado", layout="wide", initial_sidebar_state="expanded")

# === Arquivos críticos ===
ARQ_POSTAR = "dados_postar.json"
ARQ_STATE = "state.json"
ARQ_HISTORICO = "historico_afiliacao.json"
ARQ_COLAB = "colaboradores.json"

# === Função de detecção e análise (SÓ DETECTA — NÃO CORRIGE) ===
def detectar_erros_persistencia():
    """
    Detecta e analisa erros de persistência nos arquivos críticos.
    Retorna dicionário com status, gravidade e impacto.
    NÃO modifica, apaga ou sobrescreve nenhum arquivo.
    """
    arquivos = {
        ARQ_POSTAR: "Redes sociais e configurações de postagem",
        ARQ_STATE: "Estado interno do sistema (módulos, automação)",
        ARQ_HISTORICO: "Histórico de análises e anúncios",
        ARQ_COLAB: "Colaboradores ativos"
    }
    
    relatorio = {}
    
    for arquivo, descricao in arquivos.items():
        status = {"arquivo": arquivo, "impacto": descricao, "status": "ok", "gravidade": "nenhum", "detalhes": ""}
        
        # 1. Arquivo ausente?
        if not os.path.exists(arquivo):
            status["status"] = "ausente"
            status["gravidade"] = "critico"
            status["detalhes"] = "Arquivo não encontrado."
            relatorio[arquivo] = status
            continue
        
        # 2. Tentar carregar JSON
        try:
            with open(arquivo, "r", encoding="utf-8") as f:
                dados = json.load(f)
        except json.JSONDecodeError:
            status["status"] = "corrompido"
            status["gravidade"] = "irreversivel"
            status["detalhes"] = "JSON inválido (sintaxe quebrada)."
            relatorio[arquivo] = status
            continue
        except Exception as e:
            status["status"] = "erro_leitura"
            status["gravidade"] = "critico"
            status["detalhes"] = f"Falha ao ler: {type(e).__name__}: {str(e)}"
            relatorio[arquivo] = status
            continue
        
        # 3. Conteúdo vazio ou estrutura inválida
        if dados is None or (isinstance(dados, dict) and len(dados) == 0) or (isinstance(dados, list) and len(dados) == 0):
            status["status"] = "vazio"
            status["gravidade"] = "recuperavel"
            status["detalhes"] = "Arquivo existe, mas está vazio ou com estrutura mínima vazia."
            relatorio[arquivo] = status
            continue
        
        # 4. Estrutura esperada (básica)
        if arquivo == ARQ_POSTAR and not isinstance(dados, dict):
            status["status"] = "estrutura_invalida"
            status["gravidade"] = "critico"
            status["detalhes"] = "Esperado dict, obtido outro tipo."
        elif arquivo == ARQ_STATE and not isinstance(dados, dict):
            status["status"] = "estrutura_invalida"
            status["gravidade"] = "critico"
            status["detalhes"] = "Esperado dict para state.json."
        elif arquivo == ARQ_HISTORICO and not isinstance(dados, list):
            status["status"] = "estrutura_invalida"
            status["gravidade"] = "critico"
            status["detalhes"] = "Esperado lista para histórico."
        elif arquivo == ARQ_COLAB and not isinstance(dados, list):
            status["status"] = "estrutura_invalida"
            status["gravidade"] = "critico"
            status["detalhes"] = "Esperado lista para colaboradores."
        else:
            status["detalhes"] = "Estrutura válida."
        
        relatorio[arquivo] = status
    
    return relatorio

# === Inicializar sessão ===
if "erros_persistencia" not in st.session_state:
    st.session_state.erros_persistencia = detectar_erros_persistencia()

# === Sidebar ===
st.sidebar.title("MSSP Afiliado")
pagina = st.sidebar.radio(
    "Navegue pelas seções:",
    ["Início", "Pesquisa de Produtos", "Ideias de Anúncio", "Postar", "Histórico", "Colaboradores", "Rafinha", "Configurações"],
    index=0
)

# === Páginas ===
if pagina == "Início":
    st.title("🎯 MSSP Afiliado")
    st.subheader("Fase 2A — Análise Avançada de Produtos")
    st.info("Comece por 'Pesquisa de Produtos'.")

elif pagina == "Rafinha":
    st.title("🧠 Rafinha — Cérebro Interno da MSSP")
    st.caption("Sou seu parceiro, guardião e resolvedor.")
    
    # Mostrar relatório de detecção (somente leitura)
    erros = st.session_state.erros_persistencia
    st.markdown("### 🔍 Relatório de Persistência (leitura apenas)")
    
    for arquivo, info in erros.items():
        cor = "🔴" if info["gravidade"] == "critico" else "🟠" if info["gravidade"] == "irreversivel" else "🟡" if info["gravidade"] == "recuperavel" else "🟢"
        st.markdown(f"{cor} **{arquivo}** → `{info['status']}` | Gravidade: `{info['gravidade']}`")
        st.caption(f"→ {info['detalhes']}")

    st.info("⚠️ Este relatório é apenas de detecção. Nenhum arquivo foi alterado.")

else:
    st.title("Seção em desenvolvimento")
    st.text("As demais páginas estão disponíveis, mas este exemplo foca na detecção do Rafinha.")
