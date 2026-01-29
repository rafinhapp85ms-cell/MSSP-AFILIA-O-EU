import streamlit as st
import json
import os

# Funções de persistência para redes sociais
def carregar_dados_postar():
    if os.path.exists("dados_postar.json"):
        try:
            with open("dados_postar.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    else:
        dados_vazios = {
            "redes": {
                "YouTube": {"usuario": "", "senha": ""},
                "Pinterest": {"usuario": "", "senha": ""},
                "Instagram": {"usuario": "", "senha": ""},
                "TikTok": {"usuario": "", "senha": ""},
                "Facebook": {"usuario": "", "senha": ""}
            },
            "horarios_postagem": "07:00–09:00, 12:00–14:00, 18:00–21:00",
            "link_afiliado": "",
            "info_extra": ""
        }
        salvar_dados_postar(dados_vazios)
        return dados_vazios

def salvar_dados_postar(dados):
    with open("dados_postar.json", "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

# Inicializar estado da sessão
if "dados_postar" not in st.session_state:
    st.session_state.dados_postar = carregar_dados_postar()

# Estilo CSS para fixar o topo
st.markdown(
    """
    <style>
    .sticky-top {
        position: sticky;
        top: 0;
        background-color: white;
        z-index: 100;
        padding: 20px 0;
        margin-bottom: 20px;
        border-bottom: 1px solid #e0e0e0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Página: Postar
st.title("📤 Postar")
st.caption("Configure suas credenciais e horários para postagens automáticas.")

# Container fixo no topo
st.markdown('<div class="sticky-top">', unsafe_allow_html=True)
st.subheader("📱 Redes Sociais")

dados = st.session_state.dados_postar
redes = ["YouTube", "Pinterest", "Instagram", "TikTok", "Facebook"]
dados_atualizados = {}

for rede in redes:
    col1, col2 = st.columns(2)
    with col1:
        valor_usuario = dados.get("redes", {}).get(rede, {}).get("usuario", "")
        usuario = st.text_input(f"{rede} - Usuário/Login:", value=valor_usuario, key=f"{rede}_usuario")
    with col2:
        valor_senha = dados.get("redes", {}).get(rede, {}).get("senha", "")
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
    dados_completos = {
        "redes": dados_atualizados,
        "horarios_postagem": horarios,
        "link_afiliado": link_afiliado,
        "info_extra": info_extra
    }
    st.session_state.dados_postar = dados_completos
    salvar_dados_postar(dados_completos)
    st.success("✅ Todas as configurações foram salvas com sucesso! Os dados permanecerão após fechar e reabrir o app.")

st.markdown('</div>', unsafe_allow_html=True)
