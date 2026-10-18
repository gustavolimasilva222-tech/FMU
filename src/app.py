import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ----------------------------------------------------
# CONFIGURAÇÃO DA PÁGINA & TEMA VISUAL (AZUL, PRETO, DOURADO)
# ----------------------------------------------------
st.set_page_config(
    page_title="Imperial Health Analytics",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização CSS personalizada (Padrão Imperial)
st.markdown("""
    <style>
    .main {
        background-color: #05050A;
        color: #FFFFFF;
    }
    .stApp {
        background-color: #05050A;
    }
    h1, h2, h3 {
        color: #FFD700 !important;
        font-family: 'Arial', sans-serif;
    }
    .stMetric {
        background-color: #0A1128;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #00B4D8;
    }
    div[data-testid="stMetricValue"] {
        color: #FFD700 !important;
    }
    .stButton>button {
        background-color: #00B4D8;
        color: #05050A;
        font-weight: bold;
        border-radius: 5px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #FFD700;
        color: #05050A;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# SIMULAÇÃO E CARREGAMENTO DE DADOS EPIDEMIOLÓGICOS
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
# BARRA LATERAL (NAVEGAÇÃO E FILTROS)
# ----------------------------------------------------
st.sidebar.title("Painel de Controlo")
st.sidebar.markdown("---")

menu = st.sidebar.radio("Navegação Principal", [
    "Visão Geral Epidemiológica", 
    "Modelagem Preditiva", 
    "Gestão de Recursos", 
    "Documentação & Sobre"
])

regiao_sel = st.sidebar.multiselect("Filtrar por Região:", options=df["Região"].unique(), default=df["Região"].unique())
df_filtrado = df[df["Região"].isin(regiao_sel)]

# ----------------------------------------------------
# 1. VISÃO GERAL EPIDEMIOLÓGICA
# ----------------------------------------------------
if menu == "Visão Geral Epidemiológica":
    st.title("Imperial Health Analytics")
    st.caption("Painel Preditivo de Indicadores Epidemiológicos · ODS 3 (Saúde e Bem-Estar)")
    st.markdown("---")
    
    col1, col2, col3, col4 = st.columns(4)
    total_casos = df_filtrado["Casos Notificados"].sum()
    total_intern = df_filtrado["Internações Hospitalares"].sum()
    taxa_intern = (total_intern / total_casos * 100) if total_casos > 0 else 0
    
    col1.metric("Total de Casos", f"{total_casos:,}")
    col2.metric("Total de Internações", f"{total_intern:,}")
    col3.metric("Taxa de Internação", f"{taxa_intern:.1f}%")
    col4.metric("Regiões Monitorizadas", len(regiao_sel))
    
    st.markdown("### 📈 Evolução Temporal de Notificações")
    fig_line = px.line(
        df_filtrado.groupby("Data")[["Casos Notificados", "Internações Hospitalares"]].sum().reset_index(),
        x="Data", y=["Casos Notificados", "Internações Hospitalares"],
        color_discrete_sequence=["#00B4D8", "#FFD700"],
        template="plotly_dark"
    )
    fig_line.update_layout(paper_bgcolor="#05050A", plot_bgcolor="#0A1128")
    st.plotly_chart(fig_line, width='stretch')

# ----------------------------------------------------
# 2. MODELAGEM PREDITIVA DE RISCO
# ----------------------------------------------------
elif menu == "Modelagem Preditiva":
    st.title("Modelagem Preditiva de Risco")
    st.markdown("Previsão e classificação de risco populacional para apoio à decisão clínica e epidemiológica.")
    st.markdown("---")
    
    fig_bar = px.histogram(
        df_filtrado, x="Região", y="Internações Hospitalares", color="Nível de Risco Preditivo",
        barmode="group",
        color_discrete_map={"Alto": "#E63946", "Médio": "#FFD700", "Baixo": "#00B4D8"},
        template="plotly_dark"
    )
    fig_bar.update_layout(paper_bgcolor="#05050A", plot_bgcolor="#0A1128")
    st.plotly_chart(fig_bar, width='stretch')

# ----------------------------------------------------
# 3. GESTÃO DE RECURSOS
# ----------------------------------------------------
elif menu == "Gestão de Recursos":
    st.title("Simulação e Gestão de Recursos Hospitalares")
    st.markdown("---")
    
    capacidade = st.slider("Capacidade Hospitalar Simultânea (Leitos):", 100, 1000, 500)
    intern_atuais = df_filtrado["Internações Hospitalares"].iloc[-15:].sum()
    
    st.progress(min(int((intern_atuais / capacidade) * 100), 100))
    st.write(f"Ocupação estimada nos últimos 15 dias: **{intern_atuais} / {capacidade} leitos** ({intern_atuais/capacidade*100:.1f}%)")

# ----------------------------------------------------
# 4. DOCUMENTAÇÃO E SOBRE
# ----------------------------------------------------
else:
    st.title("Documentação do Projeto")
    st.markdown("""
    ### Projeto Integrador FMU Tech Inovação (ODS 3)
    **Título:** Imperial Health Analytics - Painel Preditivo de Indicadores Epidemiológicos  
    **Autores:** Gustavo Lima Silva, Thiago Araújo, Juan Luccas, Melany Kauane, Rodrigo Viana.
    """)
