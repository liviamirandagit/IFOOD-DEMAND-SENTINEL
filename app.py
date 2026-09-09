import streamlit as st
import pandas as pd
import psycopg2
import folium
from streamlit_folium import st_folium
import h3

st.set_page_config(
    page_title="iFood Demand Sentinel",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Estilização CSS Cyberpunk / Tech
st.markdown("""
    <style>
    /* Fundo da Aplicação */
    .stApp {
        background-color: #08080a;
        background-image: 
            radial-gradient(circle at 50% 0%, rgba(234, 29, 44, 0.25) 0%, transparent 60%),
            linear-gradient(90deg, rgba(234, 29, 44, 0.05) 1px, transparent 1px),
            linear-gradient(rgba(234, 29, 44, 0.05) 1px, transparent 1px);
        background-size: 100% 100%, 45px 45px, 45px 45px;
        color: #e0e0e0;
    }

    /* Título GIGANTE */
    .main-title {
        color: #ffffff !important;
        font-size: 4.2rem !important;
        font-weight: 900 !important;
        line-height: 1.1 !important;
        letter-spacing: -1px !important;
        text-transform: uppercase !important;
        margin-bottom: 4px !important;
        margin-top: -15px !important;
        text-shadow: 
            0 0 15px rgba(234, 29, 44, 0.9),
            0 0 30px rgba(234, 29, 44, 0.7),
            0 0 60px rgba(234, 29, 44, 0.4);
        font-family: 'Inter', sans-serif !important;
    }
    
    .title-red {
        color: #ea1d2c !important;
    }

    /* Subtítulo */
    .title-subtitle-tech {
        color: #d1d1db !important;
        font-size: 1.3rem !important;
        font-weight: 700 !important;
        letter-spacing: 2px !important;
        text-transform: uppercase !important;
        margin-top: 4px !important;
        margin-bottom: 12px !important;
        text-shadow: 0 0 10px rgba(234, 29, 44, 0.4);
    }

    /* Descrição do Projeto */
    .sub-title {
        color: #a0a0b2 !important;
        font-size: 1.05rem !important;
        font-weight: 400 !important;
        line-height: 1.5 !important;
        letter-spacing: 0.3px !important;
        margin-bottom: 25px !important;
        max-width: 1000px !important;
    }

    /* Cards KPI */
    div[data-testid="stMetric"] {
        background: rgba(18, 18, 24, 0.85);
        border: 1px solid rgba(234, 29, 44, 0.35);
        border-radius: 12px;
        padding: 18px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.6), 0 0 15px rgba(234, 29, 44, 0.18);
        backdrop-filter: blur(8px);
        transition: all 0.3s ease;
    }

    div[data-testid="stMetric"]:hover {
        border-color: #ea1d2c;
        box-shadow: 0 0 22px rgba(234, 29, 44, 0.5);
    }

    div[data-testid="stMetricLabel"] {
        color: #8f8f9d !important;
        font-size: 0.95rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    div[data-testid="stMetricValue"] {
        color: #ea1d2c !important;
        font-size: 2.1rem !important;
        font-weight: 900;
        text-shadow: 0 0 12px rgba(234, 29, 44, 0.6);
    }

    /* Títulos de Seção */
    .section-header {
        color: #ffffff;
        font-size: 1.6rem !important;
        font-weight: 800 !important;
        margin-bottom: 15px;
        border-left: 4px solid #ea1d2c;
        padding-left: 10px;
        letter-spacing: 0.5px;
    }

    /* Estilização da Tabela */
    div[data-testid="stDataFrame"] {
        font-size: 1.2rem !important;
    }

    div[data-testid="stDataFrame"] td {
        font-size: 1.15rem !important;
        padding: 10px !important;
    }

    div[data-testid="stDataFrame"] th {
        font-size: 1.1rem !important;
        font-weight: 700 !important;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_resource
def get_connection():
    return psycopg2.connect(
        host="localhost",
        port=5432,
        dbname="ifood_db",
        user="ifood_user",
        password="ifood_password"
    )

def fetch_data():
    conn = get_connection()
    query = """
    SELECT id, user_id, search_query, latitude, longitude, h3_index, created_at 
    FROM search_events 
    ORDER BY created_at DESC;
    """
    return pd.read_sql(query, conn)

# Título Principal Gigante
st.markdown('<p class="main-title" translate="no"><span class="title-red">IFOOD</span> DEMAND SENTINEL</p>', unsafe_allow_html=True)

# Subtítulo
st.markdown('<p class="title-subtitle-tech" translate="no">INTELIGÊNCIA GEOSPACIAL & MAPEAMENTO DE DEMANDA</p>', unsafe_allow_html=True)

# Descrição do projeto
st.markdown(
    '<p class="sub-title">'
    'Plataforma de inteligência espacial para mapeamento de demanda por tipo de culinária em tempo real. '
    'Utilizando a indexação hexagonal H3, o dashboard identifica áreas de alto volume de pesquisas para orientar '
    'a expansão estratégica de novos parceiros e otimizar a cobertura da rede no ecossistema iFood.'
    '</p>', 
    unsafe_allow_html=True
)

try:
    df = fetch_data()
except Exception as e:
    st.error(f"Erro ao conectar no PostgreSQL: {e}")
    st.stop()

if df.empty:
    st.info("Aguardando eventos de busca no pipeline...")
    st.stop()

# --- Cálculos para os KPIs e Tabela ---
total_buscas = len(df)

if not df.empty:
    top_search = df["search_query"].mode()[0]
    top_count = (df["search_query"] == top_search).sum()
    top_pct = (top_count / total_buscas) * 100
    top_display = f"{top_search} ({top_pct:.1f}%)"
else:
    top_display = "-"

# --- Painel de Métricas (KPIs) ---
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total de Buscas", f"{total_buscas:,}")
c2.metric("Usuários Ativos", df["user_id"].nunique())
c3.metric("Item Mais Buscado", top_display)
c4.metric("Hexágonos Atingidos", df["h3_index"].nunique())

st.write("")

col_left, col_right = st.columns([2, 1])

with col_left:
    st.markdown('<p class="section-header">Análise Geospacial (Hexágonos H3)</p>', unsafe_allow_html=True)
    
    avg_lat = df["latitude"].mean()
    avg_lng = df["longitude"].mean()
    
    # Mapa claro OpenStreetMap
    m = folium.Map(
        location=[avg_lat, avg_lng], 
        zoom_start=13, 
        tiles="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        max_zoom=19
    )
    
    h3_counts = df["h3_index"].value_counts().to_dict()

    for h3_hex, count in h3_counts.items():
        try:
            boundary = h3.cell_to_boundary(h3_hex)
        except AttributeError:
            boundary = h3.h3_to_geo_boundary(h3_hex)
            
        geo_json = [list(pt) for pt in boundary]

        folium.Polygon(
            locations=geo_json,
            color="#EA1D2C",
            weight=2.5,
            fill=True,
            fill_color="#EA1D2C",
            fill_opacity=min(0.4 + (count * 0.1), 0.85),
            popup=f"<b>Hexágono:</b> {h3_hex}<br><b>Demanda:</b> {count} buscas"
        ).add_to(m)

    st_folium(m, width=None, use_container_width=True, height=480)

with col_right:
    st.markdown('<p class="section-header">Rank de Demandas</p>', unsafe_allow_html=True)
    
    # Tabela com cálculo de Porcentagem
    rank_df = df["search_query"].value_counts().reset_index()
    rank_df.columns = ["Categoria", "Qtd Buscas"]
    rank_df["% Total"] = ((rank_df["Qtd Buscas"] / total_buscas) * 100).map("{:.1f}%".format)
    
    st.dataframe(
        rank_df, 
        use_container_width=True,
        hide_index=True,
        height=350
    )

    if st.button("🔄 Atualizar Painel de Controle", use_container_width=True, type="primary"):
        st.rerun()