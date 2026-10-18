import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ----------------------------------------------------
# 1. CONFIGURAÇÃO DA PÁGINA & TEMA IMPERIAL
# ----------------------------------------------------
st.set_page_config(
    page_title="Imperial Health Analytics | Enterprise",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização CSS refinada para eliminar os pontos e estilizar a barra lateral
st.markdown("""
    <style>
    .stApp {
        background-color: #05050A !important;
        color: #FFFFFF;
        font-family: 'Inter', -apple-system, sans-serif;
    }
    
    /* Barra Lateral Imperial */
    section[data-testid="stSidebar"] {
        background-color: #0A1128 !important;
        border-right: 1px solid rgba(255, 215, 0, 0.15);
        padding-top: 10px;
    }
    
    /* Remover pontos e formatar os botões de rádio do menu lateral */
    div[data-testid="stSidebar"] .stRadio > label {
        display: none !important;
    }
    div[data-testid="stSidebar"] .stRadio [role="radiogroup"] {
        gap: 5px;
    }
    div[data-testid="stSidebar"] .stRadio [role="radio"] {
        background-color: rgba(255, 215, 0, 0.03);
        border-radius: 8px;
        padding: 8px 12px;
        border: 1px solid rgba(255, 215, 0, 0.08);
        transition: all 0.3s ease;
    }
    div[data-testid="stSidebar"] .stRadio [role="radio"]:hover {
        background-color: rgba(255, 215, 0, 0.1);
        border-color: #FFD700;
    }
    div[data-testid="stSidebar"] .stRadio [aria-checked="true"] {
        background-color: rgba(255, 215, 0, 0.15) !important;
        border-color: #FFD700 !important;
    }

    /* Card Destacado Dourado Imperial */
    .metric-card-primary {
        background: linear-gradient(135deg, #0A1128 0%, #101F42 100%);
        border: 1px solid #FFD700;
        border-radius: 16px;
        padding: 24px;
        color: white;
        box-shadow: 0 8px 25px rgba(255, 215, 0, 0.15);
        margin-bottom: 15px;
    }
    
    /* Cards Secundários Cyan */
    .metric-card-secondary {
        background-color: #0A1128;
        border: 1px solid #00B4D8;
        border-radius: 16px;
        padding: 24px;
        color: white;
        margin-bottom: 15px;
    }
    
    h1, h2, h3 {
        color: #FFD700 !important;
        font-weight: 700;
    }
    
    .stButton>button {
        background-color: #00B4D8 !important;
        color: #05050A !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: 700 !important;
    }
    .stButton>button:hover {
        background-color: #FFD700 !important;
        color: #05050A !important;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# 2. AUTENTICAÇÃO (user@gmail.com / user123)
# ----------------------------------------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
            <div style="background-color: #0A1128; padding: 35px; border-radius: 16px; border: 1px solid #FFD700; text-align: center;">
                <h1 style="color: #FFD700 !important; margin:0;">👑 Imperial Health</h1>
                <p style="color: #00B4D8; font-size: 0.9rem;">Imperial Health Analytics · ODS 3 (FMU)</p>
                <hr style="border-color: rgba(255,215,0,0.2); margin: 20px 0;">
            </div>
        """, unsafe_allow_html=True)
        
        email = st.text_input("E-mail:", value="user@gmail.com")
        senha = st.text_input("Palavra-passe:", type="password", value="user123")
        
        if st.button("Aceder ao Hub Imperial", use_container_width=True):
            if email == "user@gmail.com" and senha == "user123":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Credenciais incorretas. Utilize: user@gmail.com / user123")
    st.stop()

# ----------------------------------------------------
# 3. DADOS EPIDEMIOLÓGICOS SIMULADOS
# ----------------------------------------------------
@st.cache_data
def load_data():
    np.random.seed(42)
    datas = pd.date_range(start="2026-01-01", periods=180, freq="D")
    regioes = ["Zona Norte", "Zona Sul", "Zona Leste", "Zona Oeste", "Centro"]
    
    data = []
    for d in datas:
        for r in regioes:
            casos = int(np.random.poisson(lam=45) * (1.2 if r in ["Zona Leste", "Zona Sul"] else 0.9))
            internacoes = int(casos * np.random.uniform(0.12, 0.22))
            risco = "Alto" if internacoes > 12 else ("Médio" if internacoes > 7 else "Baixo")
            data.append({
                "Data": d,
                "Região": r,
                "Casos Notificados": casos,
                "Internações Hospitalares": internacoes,
                "Nível de Risco Preditivo": risco
            })
    return pd.DataFrame(data)

df = load_data()

# ----------------------------------------------------
# 4. BARRA LATERAL (ESTILO IMPERIAL HEALTH REFINADO)
# ----------------------------------------------------
st.sidebar.markdown("""
    <div style="padding: 5px 0px 15px 0px; border-bottom: 1px solid rgba(255,215,0,0.15); margin-bottom: 15px;">
        <h3 style="color: #FFD700 !important; margin: 0; font-size: 1.2rem;">👑 Imperial Health</h3>
        <p style="color: #00B4D8 !important; font-size: 0.75rem; margin: 0; text-transform: uppercase; letter-spacing: 1px;">Enterprise Analytics</p>
    </div>
    <p style="color: #A0AEC0; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; margin-bottom: 8px;">MENU PRINCIPAL</p>
""", unsafe_allow_html=True)

menu = st.sidebar.radio("", [
    "📊 Painel Geral", 
    "🔮 Modelagem Preditiva", 
    "💬 Chatbot IA", 
    "⚙️ Gestão de Recursos", 
    "🛠️ Configurações"
])

st.sidebar.markdown("<br>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='color: #A0AEC0; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; margin-bottom: 5px;'>Filtros Globais</p>", unsafe_allow_html=True)

regiao_unica_filtro = st.sidebar.selectbox("Filtrar por Região:", options=["Todas as Regiões"] + list(df["Região"].unique()))

if regiao_unica_filtro == "Todas as Regiões":
    regiao_sel = df["Região"].unique()
else:
    regiao_sel = [regiao_unica_filtro]

df_filtrado = df[df["Região"].isin(regiao_sel)]

total_casos = int(df_filtrado["Casos Notificados"].sum())
total_intern = int(df_filtrado["Internações Hospitalares"].sum())
taxa_intern = (total_intern / total_casos * 100) if total_casos > 0 else 0.0

st.sidebar.markdown("---")
if st.sidebar.button("🚪 Terminar Sessão", use_container_width=True):
    st.session_state.authenticated = False
    st.rerun()

# Header Superior
st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; padding-bottom: 15px;">
        <div>
            <h2 style="margin:0;">Imperial Health Analytics</h2>
            <p style="color: #00B4D8; margin:0;">Painel Preditivo de Indicadores Epidemiológicos · ODS 3</p>
        </div>
        <div style="text-align: right;">
            <strong style="color: #FFD700;">Gustavo Lima Silva</strong><br>
            <span style="font-size: 0.8rem; color: #00B4D8;">user@gmail.com</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# 5. PAINEL GERAL
# ----------------------------------------------------
if menu == "📊 Painel Geral":
    col_m1, col_m2, col_m3 = st.columns([1.5, 1, 1])
    
    with col_m1:
        st.markdown(f"""
            <div class="metric-card-primary">
                <p style="margin:0; font-size: 0.9rem; color: #00B4D8;">Total de Casos Notificados</p>
                <h1 style="margin: 5px 0; font-size: 2.5rem; color: #FFD700 !important;">{total_casos:,}</h1>
                <p style="margin:0; font-size: 0.85rem; color: #00B4D8;">↗ 12.5% este mês</p>
            </div>
        """, unsafe_allow_html=True)
        
    with col_m2:
        st.markdown(f"""
            <div class="metric-card-secondary">
                <p style="margin:0; font-size: 0.9rem; color: #A0AEC0;">Internações Pendentes</p>
                <h1 style="margin: 5px 0; font-size: 2.2rem; color: #FFD700 !important;">{total_intern:,}</h1>
                <p style="margin:0; font-size: 0.85rem; color: #00B4D8;">Taxa: {taxa_intern:.1f}%</p>
            </div>
        """, unsafe_allow_html=True)
        
    with col_m3:
        st.markdown(f"""
            <div class="metric-card-secondary">
                <p style="margin:0; font-size: 0.9rem; color: #A0AEC0;">Regiões Monitorizadas</p>
                <h1 style="margin: 5px 0; font-size: 2.2rem; color: #00B4D8 !important;">{len(regiao_sel)}</h1>
                <p style="margin:0; font-size: 0.85rem; color: #00B4D8;">Status: Ativo</p>
            </div>
        """, unsafe_allow_html=True)

    col_g1, col_g2 = st.columns([1, 1.2])
    
    with col_g1:
        st.markdown("### Distribuição de Riscos Regional")
        fig_pie = px.pie(
            df_filtrado, names="Nível de Risco Preditivo", values="Casos Notificados",
            color_discrete_map={"Alto": "#E63946", "Médio": "#FFD700", "Baixo": "#00B4D8"},
            hole=0.4, template="plotly_dark"
        )
        fig_pie.update_layout(paper_bgcolor="#0A1128", plot_bgcolor="#0A1128")
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with col_g2:
        st.markdown("### Evolução Mensal de Notificações")
        fig_bar = px.bar(
            df_filtrado.groupby("Região")[["Casos Notificados", "Internações Hospitalares"]].sum().reset_index(),
            x="Região", y=["Casos Notificados", "Internações Hospitalares"],
            barmode="group", color_discrete_sequence=["#00B4D8", "#FFD700"],
            template="plotly_dark"
        )
        fig_bar.update_layout(paper_bgcolor="#0A1128", plot_bgcolor="#0A1128")
        st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("### Extrato de Notificações Recentes")
    st.dataframe(df_filtrado[["Data", "Região", "Casos Notificados", "Internações Hospitalares", "Nível de Risco Preditivo"]].tail(8), use_container_width=True)

# ----------------------------------------------------
# 6. MODELAGEM PREDITIVA
# ----------------------------------------------------
elif menu == "🔮 Modelagem Preditiva":
    st.title("Modelagem Preditiva de Risco Hospitalar")
    fig_hist = px.histogram(df_filtrado, x="Região", y="Internações Hospitalares", color="Nível de Risco Preditivo", template="plotly_dark")
    fig_hist.update_layout(paper_bgcolor="#0A1128", plot_bgcolor="#0A1128")
    st.plotly_chart(fig_hist, use_container_width=True)

# ----------------------------------------------------
# 7. CHATBOT IA
# ----------------------------------------------------
elif menu == "💬 Chatbot IA":
    st.title("Imperial Copilot (Assistente Virtual)")
    
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Olá! Sou o assistente virtual do Imperial Health Analytics. Como posso ajudar hoje?"}]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Digite a sua mensagem..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        resp = f"Análise Imperial: O total de casos filtrados é de **{total_casos:,}** com **{total_intern:,} internações**."
        with st.chat_message("assistant"):
            st.markdown(resp)
        st.session_state.messages.append({"role": "assistant", "content": resp})

# ----------------------------------------------------
# 8. GESTÃO DE RECURSOS
# ----------------------------------------------------
elif menu == "⚙️ Gestão de Recursos":
    st.title("Gestão de Recursos Hospitalares")
    capacidade = st.slider("Capacidade de Leitos:", 100, 2000, 500)
    st.progress(min(int((total_intern / capacidade) * 10), 100))

# ----------------------------------------------------
# 9. CONFIGURANDO CONFIGURAÇÕES
# ----------------------------------------------------
else:
    st.title("Configurações do Perfil")
    st.markdown("""
        **Nome:** Gustavo Lima Silva  
        **E-mail:** user@gmail.com  
        **Cargo:** Cientista de Dados / Analytics Sênior  
        **Instituição:** Centro Universitário FMU · Projeto Integrador (ODS 3)
    """)