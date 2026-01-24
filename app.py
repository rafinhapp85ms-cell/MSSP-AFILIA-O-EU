import streamlit as st
import json
import os
from datetime import datetime
from pathlib import Path

# ==============================
# Configuração inicial da página
# ==============================
st.set_page_config(
    page_title="MSSP-AFILIAÇÃO-EU",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================
# Arquivos de dados
# ==============================
HISTORICO_ARQUIVO = "historico_afiliacao.json"

# ==============================
# Funções de persistência
# ==============================
def carregar_historico():
    """Carrega o histórico de pesquisas e anúncios do arquivo JSON."""
    if os.path.exists(HISTORICO_ARQUIVO):
        try:
            with open(HISTORICO_ARQUIVO, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def salvar_historico(historico):
    """Salva o histórico no arquivo JSON."""
    with open(HISTORICO_ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(historico, f, ensure_ascii=False, indent=2)

# ==============================
# Inicializar estado da sessão
# ==============================
if "historico" not in st.session_state:
    st.session_state.historico = carregar_historico()

# ==============================
# Menu lateral
# ==============================
st.sidebar.title("MSSP-AFILIAÇÃO-EU")
pagina = st.sidebar.radio(
    "Navegue pelas seções:",
    ("Início", "Pesquisa de Produtos", "Ideias de Anúncio", "Histórico", "Configurações"),
    index=0
)

# ==============================
# Página: Início
# ==============================
if pagina == "Início":
    st.title("🎯 MSSP-AFILIAÇÃO-EU")
    st.subheader("Fase 1 — Pesquisa e Anúncios para Afiliados na Europa")
    st.write("""
    Este app foi criado para ajudar afiliados a:
    - Pesquisar produtos por palavra-chave, país e plataforma
    - Gerar ideias de anúncios em português europeu
    - Manter um histórico organizado das suas atividades
    
    Tudo é salvo localmente e pode ser editado a qualquer momento.
    """)
    st.info("💡 Dica: Comece pela página **'Pesquisa de Produtos'** para registrar sua primeira busca.")

# ==============================
# Página: Pesquisa de Produtos
# ==============================
elif pagina == "Pesquisa de Produtos":
    st.title("🔍 Pesquisa de Produtos")
    
    # Formulário de pesquisa
    st.subheader("Registre uma nova pesquisa")
    
    palavra_chave = st.text_input(
        "Palavra-chave do produto:",
        placeholder="Ex: fone bluetooth, relógio smart"
    )
    
    pais = st.selectbox(
        "País:",
        ["Portugal", "Espanha", "França", "Alemanha", "Itália"]
    )
    
    plataforma = st.selectbox(
        "Tipo de plataforma:",
        ["Amazon", "AliExpress", "Awin", "CJ", "Outras"]
    )
    
    if st.button("✅ Pesquisar"):
        if not palavra_chave.strip():
            st.warning("⚠️ Por favor, digite uma palavra-chave.")
        else:
            # Criar registro
            novo_registro = {
                "tipo": "pesquisa",
                "palavra_chave": palavra_chave.strip(),
                "pais": pais,
                "plataforma": plataforma,
                "data_hora": datetime.now().isoformat()
            }
            
            # Salvar no histórico
            st.session_state.historico.append(novo_registro)
            salvar_historico(st.session_state.historico)
            
            # Mostrar confirmação
            st.success("✅ Pesquisa registrada com sucesso!")
            st.markdown(f"""
            **Detalhes da pesquisa:**
            - Palavra-chave: `{novo_registro['palavra_chave']}`
            - País: `{novo_registro['pais']}`
            - Plataforma: `{novo_registro['plataforma']}`
            - Data/hora: `{datetime.fromisoformat(novo_registro['data_hora']).strftime('%d/%m/%Y %H:%M:%S')}`
            """)

# ==============================
# Página: Ideias de Anúncio
# ==============================
elif pagina == "Ideias de Anúncio":
    st.title("✍️ Ideias de Anúncio")
    
    st.subheader("Gere um anúncio fictício")
    
    nome_produto = st.text_input(
        "Nome do produto:",
        placeholder="Ex: Fone Bluetooth Pro"
    )
    
    if st.button("✨ Gerar anúncio"):
        if not nome_produto.strip():
            st.warning("⚠️ Por favor, digite o nome do produto.")
        else:
            # Gerar anúncio simulado
            anuncio = (
                f"🔥 **Descubra o {nome_produto}!**\n\n"
                f"✅ Qualidade premium garantida\n"
                f"✅ Entrega rápida em todo o país\n"
                f"✅ Preço especial por tempo limitado\n\n"
                f"👉 **Não perca esta oportunidade! Clique no link abaixo para saber mais.**\n"
                f"[LINK DE AFILIADO AQUI]\n\n"
                f"#afiliado #promoção"
            )
            
            # Salvar no histórico
            novo_registro = {
                "tipo": "anuncio",
                "nome_produto": nome_produto.strip(),
                "anuncio": anuncio,
                "data_hora": datetime.now().isoformat()
            }
            st.session_state.historico.append(novo_registro)
            salvar_historico(st.session_state.historico)
            
            # Mostrar anúncio
            st.success("✅ Anúncio gerado com sucesso!")
            st.text_area("Seu anúncio:", value=anuncio, height=180)

# ==============================
# Página: Histórico
# ==============================
elif pagina == "Histórico":
    st.title("📜 Histórico")
    
    if st.session_state.historico:
        # Ordenar do mais recente para o mais antigo
        historico_ordenado = sorted(
            st.session_state.historico,
            key=lambda x: x["data_hora"],
            reverse=True
        )
        
        for item in historico_ordenado:
            data_fmt = datetime.fromisoformat(item["data_hora"]).strftime("%d/%m/%Y %H:%M:%S")
            
            if item["tipo"] == "pesquisa":
                st.markdown(f"**🔍 Pesquisa** • {data_fmt}")
                st.write(f"- Palavra-chave: {item['palavra_chave']}")
                st.write(f"- País: {item['pais']}")
                st.write(f"- Plataforma: {item['plataforma']}")
                
            elif item["tipo"] == "anuncio":
                st.markdown(f"**✍️ Anúncio** • {data_fmt}")
                st.write(f"- Produto: {item['nome_produto']}")
                st.text_area("", value=item["anuncio"], height=120, key=f"anuncio_{item['data_hora']}")
            
            # Botão de exclusão
            if st.button("🗑️ Apagar", key=f"del_{item['data_hora']}"):
                st.session_state.historico.remove(item)
                salvar_historico(st.session_state.historico)
                st.rerun()
            
            st.markdown("---")
    else:
        st.info("Nenhum registro ainda. Faça uma pesquisa ou gere um anúncio para começar!")

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
